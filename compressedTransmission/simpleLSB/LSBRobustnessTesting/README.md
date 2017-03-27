# Live video steganography using LSB

## Embed a random bistring in the n-th significant bit of a webcam feed. Transmit as MJPEG. Calculate stats for how many bits are correctly decoded by the client.

### Usage

1. Start the server program:

`python my_mjpeg_server.py <N>` where <N> is the significance of the bit in which to embed the bitstring message.

A random bitstring message is generated and saved as *original.npy*.

2. Once the server is running, start the client:

`python my_client.py <N>` where <N> is the same as for the client.

4. The video transmission will begin and last for 300 frames. Each received frame will be saved to a file (*<i>_received.npy*).

5. Once the client has finished, run measure.py to generate stats:

`python measure.py`