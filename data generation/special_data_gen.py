"""
Generate specialised data entry
"""

max_orb = 6


def one_combo():
    for i in range(max_orb):
        output = ""
        for _ in range(30):
            output += "{},".format(i)
        output += "1"
        print(output)


if __name__ == '__main__':
    one_combo()
