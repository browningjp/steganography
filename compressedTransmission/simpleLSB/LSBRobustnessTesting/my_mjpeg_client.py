import socket
import cv2
import pickle
import numpy as np
import random
from bitarray import bitarray
import struct
import urllib
import urllib.request as request
import sys

significance = 2 ** (int(sys.argv[1]) - 1)

URL = "http://127.0.0.1:8080/stream.mjpg"

def saveArrayToFile(i,inputArray):
  # save to file
  filename = str(i) + "_received"
  np.save(filename,inputArray)


cv2.namedWindow('Client',cv2.WINDOW_NORMAL)

stream = request.urlopen(URL)
myBytes = bytes()

i = 0

while i < 300:
# http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera
    myBytes += stream.read(1024)
    a = myBytes.find(b'\xff\xd8')
    b = myBytes.find(b'\xff\xd9')

    if a != -1 and b != -1:
        jpg = myBytes[a:b+2]
        myBytes = myBytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('Client', frame)

        decoded_message = np.bitwise_and(frame,significance)

        # print("Reshaping message array...")
        decoded_message = decoded_message.flatten()

        decoded_message = decoded_message / significance

        # print("Converting message to boolean values...")
        decoded_message = decoded_message.astype(bool)

        # print("Converting to string")
        saveArrayToFile(i,decoded_message)

        i += 1

        if cv2.waitKey(1) == 27:
            exit(0)
