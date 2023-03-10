import os
import joblib
from keras.layers import LSTM, Dense, Input
from keras.models import Model, load_model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model

import config

#loading cnn model

def model_cnn_load():
    model = VGG16(weights="imagenet", include_top=True, input_shape=(224, 224, 3))
    out = model.layers[-2].output
    model_final = Model(inputs=model.input, outputs=out)
    return model_final


def inference_model():
    """ This Returns the model that will be used for inference"""
    with open(
        os.path.join(
            config.save_model_path, "tokenizer" + str(config.num_decoder_tokens)
        ),
        "rb",
    ) as file:
        tokenizer = joblib.load(file)
    # encoder model loading. This remains the same..
    inf_encoder_model = load_model(
        os.path.join(config.save_model_path, "encoder_model.h5")
    )

    # loading inference decoder model....
    decoder_inputs = Input(shape=(None, config.num_decoder_tokens))
    decoder_dense = Dense(config.num_decoder_tokens, activation="softmax")
    decoder_lstm = LSTM(config.latent_dim, return_sequences=True, return_state=True)
    decoder_state_input_h = Input(shape=(config.latent_dim,))
    decoder_state_input_c = Input(shape=(config.latent_dim,))
    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
    decoder_outputs, state_h, state_c = decoder_lstm(
        decoder_inputs, initial_state=decoder_states_inputs
    )
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)
    inf_decoder_model = Model(
        [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states
    )
    inf_decoder_model.load_weights(
        os.path.join(config.save_model_path, "decoder_model_weights.h5")
    )
    return tokenizer, inf_encoder_model, inf_decoder_model
