import cv2
from av import VideoFrame
from aiortc import MediaStreamTrack
import numpy as np
from threading import Thread

import predict
        
class VideoCaptionTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track of frames with captions.
    """

    kind = "video"

    def __init__(self, track):
        super().__init__()  # don't forget this!
        self.track = track
        self.count = 0
        self.frames = []
        self.caption = ''

    def mythreadFunc(self, images):
        caption = predict.test(images)
        self.caption = caption

    async def recv(self):
        frame = await self.track.recv()
        self.count += 1
        #print('**********' + str(self.count) + '*********')
        img = frame.to_ndarray(format="bgr24")

        if self.count <= 80:
            image = cv2.resize(img, (224, 224))
            #frame = cv2.resize(frame, (224, 224, 3))
            self.frames.append(image)
        elif self.count == 81:
            self.count = 0
            images = np.array(self.frames)
            self.frames = []
            thread = Thread(target = self.mythreadFunc, args = (images,))
            thread.start()

        font = cv2.FONT_HERSHEY_SIMPLEX
        if (self.caption != None):
            text = 'Caption: ' + self.caption;
            img = cv2.putText(img, text, (10, 440), font, 1, (255, 255, 0), 2, cv2.LINE_AA)
            
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame
        