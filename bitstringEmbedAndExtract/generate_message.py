import numpy as np
import sys

def main():

    filename = sys.argv[1]

    # Create sequence 10100100010000100000100000010000000100000000 etc

    numpy_index = 0
    numpy_array = np.zeros(720*1280*3,dtype=bool)
    numberOfZeros = 1

    print("Generating example message...")

    while True:
        numpy_array[numpy_index] = 1
        numpy_index += 1
        for j in range(numberOfZeros):
            numpy_array[numpy_index] = 0
            numpy_index += 1
        numberOfZeros += 1

        # if not enough room in array for next round, make all the remaining array values = 1
        if(numberOfZeros + 1 > 720*1280*3 - numpy_index):
            for k in range(720*1280*3 - numpy_index,720*1280*3):
                numpy_array[k] = 1
            break;
    print("done!")
    print("Saving example message...")
    np.save(filename, numpy_array)
    print("done!")

if __name__ == '__main__':
    main()
