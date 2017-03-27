import numpy as np
import os

original = np.load("original.npy")
original = original.astype(np.uint8)

listOfReceivedFiles = [f for f in sorted(os.listdir("./")) if f.endswith("_received.npy")]

percentages_of_bits_correctly_received = []
percentages_of_0s_correctly_received = []
percentages_of_1s_correctly_received = []

numbers,counts = np.unique(original, return_counts=True)
number_of_0s_originally = counts[0]
number_of_1s_originally = counts[1]

percentage_of_1s_originally = number_of_1s_originally * 100 / (number_of_0s_originally + number_of_1s_originally)
percentage_of_0s_originally = number_of_0s_originally * 100 / (number_of_0s_originally + number_of_1s_originally)

for i in range(len(listOfReceivedFiles)):

    received = np.load(listOfReceivedFiles[i])
    received = received.astype(np.uint8)


    comparison = original + 2 * received

    numbers,counts = np.unique(comparison, return_counts=True)

    # 0 = 0 sent, 0 received
    # 1 = 1 sent, 0 received
    # 2 = 0 sent, 1 received
    # 3 = 1 sent, 1 received

    dictionary = {}

    for j in range(len(numbers)):
        dictionary[numbers[j]] = counts[j]

    number_of_0s_correctly_received = dictionary.get(0,0)
    number_of_1s_flipped = dictionary.get(1,0)
    number_of_0s_flipped = dictionary.get(2,0)
    number_of_1s_correctly_received = dictionary.get(3,0)

    number_of_bits_correctly_received = number_of_0s_correctly_received + number_of_1s_correctly_received
    number_of_bits_flipped = number_of_0s_flipped + number_of_1s_flipped

    percentage_of_bits_correctly_received = number_of_bits_correctly_received * 100 / len(received)
    percentage_of_bits_flipped = number_of_bits_flipped * 100 / len(received)

    percentage_of_0s_correctly_received = number_of_0s_correctly_received * 100 / number_of_0s_originally
    percentage_of_1s_correctly_received = number_of_1s_correctly_received * 100 / number_of_1s_originally

    # add results to lists
    percentages_of_bits_correctly_received.append(percentage_of_bits_correctly_received)
    percentages_of_0s_correctly_received.append(percentage_of_0s_correctly_received)
    percentages_of_1s_correctly_received.append(percentage_of_1s_correctly_received)


    print("Frame #" + str(i+1))
    print()
    print("Percentage of 0s originally: " + str(percentage_of_0s_originally))
    print("Percentage of 1s originally: " + str(percentage_of_1s_originally))
    print("Percentage of bits correctly received: " + str(percentage_of_bits_correctly_received) + "%")
    # print("Percentage of bits flipped: " + str(percentage_of_bits_flipped) + "%")
    print("Percentage of 0s correctly received: " + str(percentage_of_0s_correctly_received) + "%")
    print("Percentage of 1s correctly received: " + str(percentage_of_1s_correctly_received) + "%")
    print()

# get averages and print

average_pc_of_bits_correct = np.mean(percentages_of_bits_correctly_received)
average_pc_of_0s_correct = np.mean(percentages_of_0s_correctly_received)
average_pc_of_1s_correct = np.mean(percentages_of_1s_correctly_received)

print("AVERAGE")
print()
print("Percentage of 0s originally: " + str(percentage_of_0s_originally) + "%")
print("Percentage of 1s originally: " + str(percentage_of_1s_originally) + "%")
print("Percentage of bits correctly received: " + str(average_pc_of_bits_correct) + "%")
print("Percentage of 0s correctly received: " + str(average_pc_of_0s_correct) + "%")
print("Percentage of 1s correctly received: " + str(average_pc_of_1s_correct) + "%")
print()
