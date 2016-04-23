import os
import csv

p1 = "completed_data/8hr/"
p2 = "completed_data/fixed/"


def correct_accidental_tuples():
    fuckups = []

    if not os.path.isdir(p2):
        os.mkdir(p2)
    for filename in os.listdir(p1):
        input_ = p1 + filename
        output_ = p2 + filename
        in_csv = csv.DictReader(open(input_, 'r'))
        out_csv = csv.DictWriter(open(output_, 'w'), in_csv.fieldnames)
        out_csv.writeheader()

        for line in in_csv:
            if len(line) != 90:
                fuckups.append(line)
                print(len(line))
            temp = {}
            for key, val in line.items():
                temp[key] = val if not isinstance(val, str) else val.replace('(True,)', 'True')\
                                                                    .replace('(False,)', 'False')
            out_csv.writerow(temp)

    print(fuckups)


if __name__ == "__main__":
    correct_accidental_tuples()




