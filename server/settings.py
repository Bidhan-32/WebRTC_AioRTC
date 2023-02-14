import model

def init():
    global tokenizer
    global cnn_model
    global inf_decoder_model
    global inf_encoder_model
    tokenizer, inf_encoder_model, inf_decoder_model = model.inference_model()
    cnn_model = model.model_cnn_load()
    print('Models loaded')


