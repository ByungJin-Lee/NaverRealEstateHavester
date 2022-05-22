import os
import csv

path = input("Input path : ")

output_filename = input("Output File Name : ") + '.csv'

def csv_filter(li):
    files = list()
    for f in li:
        if f.endswith('.csv'):
            files.append(f)
    return files

csv_files = csv_filter(os.listdir(path))

csv_files.sort()

total = len(csv_files)

cur = 1

header = False

with open(output_filename, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    for victim in csv_files:
        print("progress[%s]: %d/%d" % (csv_files[cur-1], cur, total))
        with open(path + '/' + victim, 'r', encoding='utf-8', newline='') as v:
            res = [val for val in csv.reader(v)]
            if header is False:
                header = True
                w.writerow(res[0])
            w.writerows(res[1:])
        cur += 1




