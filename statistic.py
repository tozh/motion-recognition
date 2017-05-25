import os
import os.path
import math

libsvm_dir = "C:\\libsvm-3.21\\tools"
test_file = "data.test"
predict_file = "data.predict"
test = []
predict = []
statistic = [[0 for col in range(5)] for row in range(5)]
fin = open(libsvm_dir + "\\" + test_file, "r")
for line in fin:
    line = line.strip()
    if line != "":
        line_word = line.split(" ")
        test.append(line_word[0])
print(len(test))
fin.close()

fin = open(libsvm_dir + "\\" + predict_file, "r")
for line in fin:
    line = line.strip()
    if line != "":
        line_word = line.split(" ")
        predict.append(line_word[0])
print(len(predict))
fin.close()

i = 0
if len(test) == len(predict):
    for i in range(len(test)):
        statistic[int(predict[i])][int(test[i])] += 1
print(statistic)
fileout = open(libsvm_dir + "\\" + test_file + ".stat", "w", encoding="utf8")
i = 0
j = 0
for i in range(5):
    for j in range(5):
        fileout.write(str(statistic[i][j]) + "\t" + "\t")
    fileout.write("\n")
fileout.close()

