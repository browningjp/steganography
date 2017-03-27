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

def create_random_message_array(x_res,y_res,filename):

  total_length = x_res * y_res * 3 # resolution x 3 colour channels

  # list of random bits of length (total_length)
  bits = [random.getrandbits(1) for i in range(total_length)]

  # create empty array same size as frame
  final_array = np.empty((total_length),dtype=bool)

  # convert bit string to a bitarray
  message_array = bitarray(bits)

  # first part of final array made from bitstring of message
  final_array = np.asarray(message_array)

  # pad remainder of frame with random bits
  # final_array[length_so_far:] = np.random.randint(2, size=length_to_go).astype(bool)

  # save to file
  np.save(filename,final_array)

  return final_array

significance = 2 ** (int(sys.argv[1]) - 1)


x_res = 1280
y_res = 720

# # Open camera
cam = cv2.VideoCapture(0)
cv2.namedWindow('Server',cv2.WINDOW_NORMAL)

class CamHandler(BaseHTTPRequestHandler):
# adapted from https://gist.github.com/n3wtron/4624820
  def do_GET(self):
    if self.path.endswith('.mjpg'):

      filename = "original"
      message = create_random_message_array(x_res,y_res,filename)
      message = message.astype(np.uint8)

      self.send_response(200)
      self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
      self.end_headers()

      i = 0

      while True:
        try:
          rc,frame = capture.read()
          if not rc:
            continue

          # Set least significant bit to zero
          frame = np.invert(frame)
          frame = np.bitwise_or(frame,significance)
          frame = np.invert(frame)

          # reshape message array to same shape as camera image
          message_frame = np.reshape(message,frame.shape)

          # perform LSB embedding
          frame = np.bitwise_or(frame,significance * message_frame)

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

          i += 1

        except KeyboardInterrupt:
          break
      return

global capture
capture = cv2.VideoCapture(0)
try:
  server = HTTPServer(('', 8080), CamHandler)
  print("server started")
  server.serve_forever()
except KeyboardInterrupt:
  capture.release()
  server.socket.close()
