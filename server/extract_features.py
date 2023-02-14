import numpy as np

def extract_features(model, images):
    """
    :param video: The video whose frames are to be extracted to convert into a numpy array
    :param model: the pretrained vgg16 model
    :return: numpy array of size 4096x80
    """
    fc_feats = model.predict(images, batch_size=128)
    img_feats = np.array(fc_feats)
    return img_feats
