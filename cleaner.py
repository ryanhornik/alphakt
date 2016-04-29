import os
import csv

p1 = "completed_data/8hr/"
p2 = "completed_data/fixed/"

distinguished = {'': 0, 'moderator': 1, 'admin': 2, 'special': 3}


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
                if key == "distinguished":
                    temp[key] = distinguished[val]
                elif key.endswith('num_reports'):
                    temp[key] = val if val else 0
                elif key in ("author_flair_text", "link_flair_text"):
                    temp[key] = 1 if val else 0
                elif key.endswith('edited'):
                    temp[key] = 0 if val == 0 else 1
                elif key.endswith('locked'):
                    temp[key] = 0 if val == 0 else 1
                else:
                    temp[key] = val if not isinstance(val, str) else val.replace('(True,)', '1')\
                                                                        .replace('(False,)', '0')\
                                                                        .replace('False', '0')\
                                                                        .replace('True', '1')
            out_csv.writerow(temp)

    print(fuckups)


if __name__ == "__main__":
    correct_accidental_tuples()



