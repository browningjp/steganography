import socket
import cv2
import pickle
import numpy as np
import random
from bitarray import bitarray

def convertStringToArray(inputString,x_res,y_res):

  # convert string to string of bits (sequence of 8-bit ascii characters)
  bits = ''.join('{0:08b}'.format(ord(char)) for char in inputString)

  # add END OF TRANSMISSION character at the end
  bits = bits + '00000100'

  # calculate the number of bits we need to fill randomly to fill frame
  total_length = x_res * y_res * 3 # resolution x 3 colour channels
  length_so_far = len(bits)
  length_to_go = total_length - length_so_far

  # create empty array same size as frame
  final_array = np.empty((total_length),dtype=bool)

  # convert bit string to a bitarray
  message_array = bitarray(bits)

  # first part of final array made from bitstring of message
  final_array[:length_so_far] = np.asarray(message_array)

  # pad remainder of frame with random bits
  final_array[length_so_far:] = np.random.randint(2, size=length_to_go).astype(bool)

  return final_array

x_res = 80
y_res = 45


messageString = input("Enter a secret message: ")
# print("Processing message...")
message = convertStringToArray(messageString,x_res,y_res)
# print("done!")

HOST = "127.0.0.1"
PORT = 8081



# Create socket
mySocket = socket.socket()
mySocket.bind((HOST,PORT))

mySocket.listen(1)

# Establish connection
conn, addr = mySocket.accept()
print("Connection from " + str(addr))

# Open camera
cam = cv2.VideoCapture(0)
cv2.namedWindow('Server',cv2.WINDOW_NORMAL)
cam.set(3,x_res)
cam.set(4,y_res)
# cam.set(cv2.CAP_PROP_FPS,2)

prev_size = 0

while True:
    return_val, frame = cam.read() # get frame from camera

    # resize frame
    big_frame = cv2.resize(frame,(640,360))

    # show frame
    cv2.imshow('Server', big_frame) # display resulting image

    # Set least significant bit to zero
    frame = np.invert(frame)
    frame = np.bitwise_or(frame,1)
    frame = np.invert(frame)

    # reshape message array to same shape as camera image
    message = np.reshape(message,frame.shape)

    # perform LSB embedding
    frame = np.bitwise_or(frame,message)

    # serialize array
    serialized = pickle.dumps(frame, protocol=4)

    if(len(serialized) != prev_size):
        print(len(serialized))
        prev_size = len(serialized)

    # send serialized frame
    conn.send(serialized)

conn.close()
