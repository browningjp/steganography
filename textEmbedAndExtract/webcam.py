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
      outputString = convertArrayToString(decoded_message)

      print(outputString)
    if(i == 1000):
      return

    i += 1


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

def main():

    messageString = input("Enter a secret message: ")
    message = convertStringToArray(messageString,720,1280)

    show_webcam(message)

if __name__ == '__main__':
    main()

# TODO - only works if message is less than size of a frame
