import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import math
import os
import os.path

fs = 50
i = 0
b, a = signal.butter(6, 0.8)     # 20 * 2 / fs = 0.8
tran_data_dir = "C:\\gd_data\\tran_data"
filter_data_dir = "C:\\gd_data\\filter_data"
data_label = ["motionRotationRateX", "motionRotationRateY", "motionRotationRateZ",
              "motionUserAccelerationX", "motionUserAccelerationY", "motionUserAccelerationZ",
              "motionGravityX", "motionGravityY", "motionGravityZ"]
for parents, dir_names, file_names in os.walk(tran_data_dir):
    for file_name in file_names:
        i = 0
        line_num = 0
        fin = open(tran_data_dir + "\\" + file_name, "r")  # count lines
        line = fin.readlines()
        line_num = len(line)
        fin.close()

        T = line_num / fs
        t = np.linspace(0, T, line_num)

        fileout = open(filter_data_dir + "\\" + file_name.split('.')[0] + "_filter.txt", "w", encoding="utf8")
        see_x = []
        see_x_filter = []
        x = []
        x_filter = []
        for i in range(9):
            y = []
            fin = open(tran_data_dir + "\\" + file_name, "r")
            for line in fin:
                line = line.strip()
                line_word = line.split("|")     # every line's [i]var write into y[]
                y.append(float(line_word[i]))
            x.append(y)

        for i in range(9):
            y = signal.filtfilt(b, a, np.asarray(x[i]), padlen=(line_num-1))
            x_filter.append(y)
        for _i in range(line_num):
            for i in range(9):
                fileout.write(str(x_filter[i][_i]) + "|")
            fileout.write(file_name[0] + "\n")

        fin.close()
        fileout.close()
