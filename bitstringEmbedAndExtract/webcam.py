import numpy as np
import sys
import cv2
import filecmp
import random
from bitarray import bitarray
import time


def show_webcam(message):
  # open camera stream
  cam = cv2.VideoCapture(0)

  # set up windows
  cv2.namedWindow('Webcam',cv2.WINDOW_NORMAL)
  cv2.namedWindow('Webcam + message',cv2.WINDOW_NORMAL)

  # resize windows
  cv2.resizeWindow('Webcam',640,360)
  cv2.resizeWindow('Webcam + message',640,360)

  # move second window
  cv2.moveWindow("Webcam + message",641,0)

  i = 0

  while True:

    # get frame from camera
    return_val, img = cam.read()

    # show camera image
    small_img = cv2.resize(img, (640,360))
    cv2.imshow('Webcam', small_img) # display resulting image

    # Set least significant bit to zero
    img = np.invert(img)
    img = np.bitwise_or(img,1)
    img = np.invert(img)

    # reshape message array to same shape as camera image
    message = np.reshape(message,img.shape)

    # perform LSB embedding
    img = np.bitwise_or(img,message)

    # show camera image
    small_img = cv2.resize(img, (640,360))
    cv2.imshow('Webcam + message', small_img) # display resulting image

    if(i == 200):
      decoded_message = np.bitwise_and(img,1)

      # print("Reshaping message array...")
      decoded_message = decoded_message.reshape(720*1280*3)

      # print("Converting message to boolean values...")
      decoded_message = decoded_message.astype(bool)

      # print("Converting to string")
      output_filename = sys.argv[2]
      np.save(output_filename, decoded_message)

      return

    i += 1

def main():

    # load message from file
    input_filename = sys.argv[1]
    message = np.load(input_filename)

    show_webcam(message)

if __name__ == '__main__':
    main()