# Live video steganography using LSB

## Embed a text message inside webcam feed, transmit as MJPEG stream to another program, then decode the message

### Usage

1. Start the server program:

`python my_mjpeg_server.py`

2. Enter the secret message when prompted, and press return.

3. Once the server is running, start the client:

`python my_client.py`

4. The video transmission will begin. After 200 frames, the message will be printed to the terminal of the client.
The message is corrupted, so the output message is rubbish. The end of end-of-transmission character is also corrupted,
so rubbish is printed continually.
