# Live video steganography using LSB

## Embed a generated bitstring inside webcam feed, extract it, then compare the messages

### Usage

Note that all filenames should end in .npy

1. Generate the sample message to a .npy file:

`python generate_message.py <messageFile>`

2. Embed and extract to a .npy file

`python webcam.py <messageFile> <extractedMessageFile>`

3. Compare the original message with the extracted message:

`python compare_files.py <messageFile> <extractedMessageFile`
