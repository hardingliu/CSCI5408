import csv

input_file1 = './data_part1.csv'
input_file2 = './data_part2.csv'
output_file = './data.csv'

with open(input_file1, 'r') as infile1, open(input_file2, 'r') as infile2, open(output_file, 'w') as outfile:
    reader1 = csv.reader(infile1)
    reader2 = csv.reader(infile2)
    writer = csv.writer(outfile)
    next(reader2, None)
    for row in reader1:
        writer.writerow(row)
    for row in reader2:
        writer.writerow(row)
