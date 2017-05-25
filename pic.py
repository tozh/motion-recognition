import os
import os.path
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack


def freq_component(data_set):
    fft_tran = fftpack.fft(data_set, n=len(data_set))
    f_component = []
    for i in range(len(fft_tran)):
        if i == 0:
            f_component.append(abs(fft_tran[i])/len(fft_tran))
        else:
            f_component.append(abs(fft_tran[i]) * 2 / len(fft_tran))
    return f_component


fs = 50
i = 0
b, a = signal.butter(6, 0.8)     # 20 * 2 / fs = 0.8
see_length = 128
tran_data_dir = "C:\\gd_data\\1"
motion_lable = ["Walk", "Run", "Sit", "Walk Upstairs", "Walk Downstairs"]
data_label = ["RotationRateX", "RotationRateY", "RotationRateZ",
              "AccelerationX", "AccelerationY", "AccelerationZ",
              "GravityX", "GravityY", "GravityZ"]

for parents, dir_names, file_names in os.walk(tran_data_dir):
    for file_name in file_names:
        i = 0
        line_num = 0
        fin = open(tran_data_dir + "\\" + file_name, "r")  # count lines
        line = fin.readlines()
        line_num = len(line)
        fin.close()

        T = line_num / fs
        see_T = see_length / fs
        t = np.linspace(0, T, line_num)
        see_t = np.linspace(0, see_T, see_length)
        see_f = np.linspace(0, fs, see_length)
        print(len(see_t))
        see_x = []
        see_x_filter = []
        x = []
        x_filter = []
        see_x_f = []
        see_x_filter_f = []

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


        for i in range(9):
            see_x.append(x[i][0:see_length:])
            see_x_filter.append(x_filter[i][0:see_length:])
            plt.subplot(3, 3, i+1)
            plt.plot(see_t, see_x[i], "r-", see_t, see_x_filter[i], "g-")
            # plt.plot(see_t, see_x[i], "r-")
            plt.ylabel('data(t)')
            plt.title(motion_lable[int(file_name[0])] + "-" + data_label[i])
        plt.suptitle(motion_lable[int(file_name[0])]+"-time", fontsize='24')
        # plt.savefig("C:\\gd_data\\pic\\"+motion_lable[int(file_name[0])]+"-time", dpi=200)
        plt.show()

        for i in range(9):
            see_x_f.append(freq_component(x[i][0:see_length:]))
            see_x_filter_f.append(freq_component(x_filter[i][0:see_length:]))
            print(len(see_x_f[i]))
            plt.subplot(3, 3, i+1)
            plt.plot(see_f, see_x_f[i], "r-", see_f, see_x_filter_f[i], "g-")
            # plt.plot(see_f, see_x_f[i], "r-")
            plt.ylabel('data(f)')
            plt.title(motion_lable[int(file_name[0])] + "-" + data_label[i])
        plt.suptitle(motion_lable[int(file_name[0])]+"-frequence", fontsize='24')
        # plt.savefig("C:\\gd_data\\pic\\"+motion_lable[int(file_name[0])]+"-frequence", dpi=200)
        plt.show()

        fin.close()
