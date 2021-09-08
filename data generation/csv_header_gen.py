"""
Generate the header for csv
"""

count = 30

if __name__ == '__main__':
    for i in range(0, count):
        print("orb{},".format(i), end="")
    print("combo\n")
