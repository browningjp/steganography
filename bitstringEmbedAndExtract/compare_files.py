import filecmp
import sys
import numpy as np

file_1 = sys.argv[1]
file_2 = sys.argv[2]

if __name__ == '__main__':

    print("Checking if extracted message matches original...")
    if(filecmp.cmp(file_1,file_2)):
        print("MATCH")
    else:
        print("NO MATCH")
