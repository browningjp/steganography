import socket
import cv2
import pickle
import numpy as np
import random
from bitarray import bitarray
import struct

from PIL import Image
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
import io
import time
import sys


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

class CamHandler(BaseHTTPRequestHandler):
  # adapted from https://gist.github.com/n3wtron/4624820
  def do_GET(self):
    if self.path.endswith('.mjpg'):
      self.send_response(200)
      self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
      self.end_headers()
      while True:
        try:
          rc,frame = capture.read()
          if not rc:
            continue

          # Set least significant bit to zero
          frame = np.invert(frame)
          frame = np.bitwise_or(frame,1)
          frame = np.invert(frame)

          # reshape message array to same shape as camera image
          message_frame = np.reshape(message,frame.shape)

          # perform LSB embedding
          frame = np.bitwise_or(frame,message_frame)

          imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
          jpg = Image.fromarray(imgRGB)
          tmpFile = io.BytesIO()
          jpg.save(tmpFile,'JPEG')
          self.wfile.write("--jpgboundary".encode())
          self.send_header('Content-type','image/jpeg')
          self.send_header('Content-length',str(sys.getsizeof(tmpFile)))
          self.end_headers()
          jpg.save(self.wfile,'JPEG')
          time.sleep(0.05)
        except KeyboardInterrupt:
          break
      return

# Set resolution
x_res = 1280
y_res = 720

# Create window for original webcam feed
cv2.namedWindow('Server',cv2.WINDOW_NORMAL)

# Get message from user and convert to array
messageString = input("Enter a secret message: ")
global message
message = convertStringToArray(messageString,x_res,y_res)

# Open webcam
global capture
capture = cv2.VideoCapture(0)

# Start server
try:
  server = HTTPServer(('', 8080), CamHandler)
  print("server started")
  server.serve_forever()
except KeyboardInterrupt:
  capture.release()
  server.socket.close()
