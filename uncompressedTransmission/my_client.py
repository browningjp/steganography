import socket
import cv2
import pickle
import numpy as np
import random
from bitarray import bitarray

HOST = "127.0.0.1"
PORT = 8081

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

# Create socket
mySocket = socket.socket()
mySocket.connect((HOST,PORT))

cv2.namedWindow('Client',cv2.WINDOW_NORMAL)

previousMessage = ''


while True:

    # serialized array
    serialized = mySocket.recv(43362)
    # conn.send(serialized)
    frame = pickle.loads(serialized)

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

    # resize frame
    big_frame = cv2.resize(frame,(640,360))

    # show frame
    cv2.imshow('Client', big_frame) # display resulting image
    cv2.waitKey(25)

conn.close()

# TODO

# - Multiple messages
# - Separate computers
# - better stability
# - higher resolution?
# - change framerate?
