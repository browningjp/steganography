import socket
import cv2
import pickle
import numpy as np
import random
from bitarray import bitarray
import struct
import urllib
import urllib.request as request

URL = "http://127.0.0.1:8080/stream.mjpg"

def convertArrayToString(inputArray):
  # convert string of bits to bitarray
  bits = bitarray(inputArray.tolist())

  outputString = ''
  haveSeenEOTCharacter = False
  index = 0
  while not haveSeenEOTCharacter:

    # current character
    characterBits = bits[index:index+8]

    # if current character is the end of transmission character, stop
    if(characterBits.to01() == '00000100'):
      haveSeenEOTCharacter = True
      break

    # convert byte (in bits) to int
    integer = int(characterBits.to01(),2)

    # append character to end of output string
    outputString += chr(integer)

    index += 8 # increment index by 8

  return outputString


cv2.namedWindow('Client',cv2.WINDOW_NORMAL)
#
previousMessage = ''


stream = request.urlopen(URL)
myBytes = bytes()

while True:
# http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera
    myBytes += stream.read(1024)
    a = myBytes.find(b'\xff\xd8')
    b = myBytes.find(b'\xff\xd9')

    if a != -1 and b != -1:
        jpg = myBytes[a:b+2]
        myBytes = myBytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('Client', frame)

        decoded_message = np.bitwise_and(frame,1)

        # print("Reshaping message array...")
        decoded_message = decoded_message.flatten()

        # print("Converting message to boolean values...")
        decoded_message = decoded_message.astype(bool)

        # print("Converting to string")
        outputString = convertArrayToString(decoded_message)

        if(outputString != previousMessage):
          print(outputString)
          previousMessage = outputString

        if cv2.waitKey(1) == 27:
            exit(0)


# TODO

# - Multiple messages
# - Separate computers
# - better stability
# - higher resolution?
# - change framerate?
