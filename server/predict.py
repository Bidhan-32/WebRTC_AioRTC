import functools
import operator
import os
import cv2
import time

import numpy as np
import extract_features

import config
import settings

# tokenizer, inf_encoder_model, inf_decoder_model = model.inference_model()

def index_to_word(tokenizer):
        # inverts word tokenizer
        index_to_word = {value: key for key, value in tokenizer.word_index.items()}
        return index_to_word

def greedy_search(loaded_array):
        """

        :param f: the loaded numpy array after creating videos to frames and extracting features
        :return: the final sentence which has been predicted greedily
        """
        inf_encoder_model, inf_decoder_model, tokenizer = settings.inf_encoder_model, settings.inf_decoder_model, settings.tokenizer
        inv_map = index_to_word(tokenizer)
        states_value = inf_encoder_model.predict(loaded_array.reshape(-1, config.time_steps_encoder, config.num_encoder_tokens))
        target_seq = np.zeros((1, 1, config.num_decoder_tokens))
        final_sentence = ''
        target_seq[0, 0, tokenizer.word_index['bos']] = 1
        for i in range(15):
            output_tokens, h, c = inf_decoder_model.predict([target_seq] + states_value)
            states_value = [h, c]
            output_tokens = output_tokens.reshape(config.num_decoder_tokens)
            y_hat = np.argmax(output_tokens)
            if y_hat == 0:
                continue
            if inv_map[y_hat] is None:
                break
            if inv_map[y_hat] == 'eos':
                break
            else:
                final_sentence = final_sentence + inv_map[y_hat] + ' '
                target_seq = np.zeros((1, 1, config.num_decoder_tokens))
                target_seq[0, 0, y_hat] = 1
        return final_sentence

def get_test_data(images):
        #model = extract_features.model_cnn_load()
        model = settings.cnn_model
        f = extract_features.extract_features(model, images)
        return f

def test(images):
        X_test = get_test_data(images)
        # generate inference test outputs
        sentence_predicted = greedy_search(X_test.reshape((-1, config.time_steps_encoder, config.num_encoder_tokens)))
        # re-init max prob
        return sentence_predicted    #**********************send this as the response*****************************

# if __name__ == "__main__":
#     caption = test()
#     print(caption)

