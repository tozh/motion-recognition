import os
import os.path
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack
import scipy.stats as stats
import statsmodels.tsa.ar_model as ar


delta_t = 1/50
fs = 50

def entropy(data_set):
    max_value = np.max(data_set)
    min_value = np.min(data_set)
    step_length = (max_value - min_value) / 10
    p = [0] * 10
    for i in range(len(data_set)):
        for j in range(10):
            if min_value + j * step_length <= data_set[i] <= min_value + (j+1) * step_length:
                p[j] += 1/len(data_set)
                break
    entropy_data = stats.entropy(p, base=2)
    return entropy_data


def arcoeff(data_set, order=4):
    ar_model = ar.AR(data_set)
    ar_model_fit = ar_model.fit(maxlag=order, ic=None, trend='nc')
    return ar_model_fit.params


def simple_feature(data_set):
    f_vec = [np.mean(data_set), np.std(data_set), abs(np.median(data_set)),
             np.max(data_set), np.min(data_set), np.dot(data_set, data_set) / len(data_set),
             (np.percentile(data_set, 75) - np.percentile(data_set, 25)), entropy(data_set)]
    f_vec.extend(list(arcoeff(data_set)))
    return f_vec


def sma_1(data_1):
    sum_1 = 0
    for i in range(len(data_1)):
        sum_1 += data_1[i]

    sma_1 = [sum_1/len(data_1)]
    return sma_1


def sma_3(data_1, data_2, data_3):
    sum_1 = 0
    sum_2 = 0
    sum_3 = 0
    if len(data_1) == len(data_2) == len(data_3):
        for i in range(len(data_1)):
            sum_1 += data_1[i]
            sum_2 += data_2[i]
            sum_3 += data_3[i]

    sma_3 = [(sum_1 + sum_2 + sum_3)/len(data_1)]
    return sma_3


def jerk(data_set):
    jerk_set = []
    for i in range(len(data_set)):
        jerk_set.append((data_set[(i+1) % len(data_set)] - data_set[(i-1) % len(data_set)]) / (2 * delta_t))
    jerk_set[0] = jerk_set[1]
    jerk_set[len(data_set)-1] = jerk_set[len(data_set)-2]
    return jerk_set


def freq_component(data_set):
    fft_tran = fftpack.fft(data_set)
    f_component = []
    for i in range(len(fft_tran)):
        if i == 0:
            f_component.append(abs(fft_tran[i])/len(fft_tran))
        else:
            f_component.append(abs(fft_tran[i]) * 2 / len(fft_tran))
    return f_component


def magnitude(data_1, data_2, data_3):
    if len(data_1) == len(data_2) == len(data_3):
        mag = []
        for i in range(len(data_1)):
            mag.append(math.sqrt(data_1[i]**2 + data_2[i]**2 + data_3[i]**2))
    return mag


def max_index(data_set):
    f_step = fs/len(data_set)
    return data_set.index(max(data_set)) * f_step


def mean_freq(data_set):
    f_step = fs/len(data_set)
    f = 0
    data_sum = 0
    weighted_sum = 0
    for i in range(len(data_set)):
        data_sum += data_set[i]
        weighted_sum += f * data_set[i]
        f += f_step
    return weighted_sum/data_sum


def band_energy(data_set):
    f_step = fs/len(data_set)
    b_0_8 = 0
    b_8_16 = 0
    b_16_24 = 0
    b_24_32 = 0
    b_32_40 = 0
    b_40_50 = 0
    for i in range(len(data_set)):
        if 0 < i*f_step < 8:
            b_0_8 += (data_set[i] * 2 / len(data_set))**2
        elif 8 <= i*f_step < 16:
            b_8_16 += (data_set[i] * 2 / len(data_set))**2
        elif 16 <= i*f_step < 24:
            b_16_24 += (data_set[i] * 2 / len(data_set))**2
        elif 24 <= i*f_step < 32:
            b_24_32 += (data_set[i] * 2 / len(data_set))**2
        elif 32 <= i*f_step < 40:
            b_32_40 += (data_set[i] * 2 / len(data_set))**2
        elif 40 <= i*f_step < 50:
            b_40_50 += (data_set[i] * 2 / len(data_set))**2
    b_0_16 = b_0_8 + b_8_16
    b_16_32 = b_16_24 + b_24_32
    b_32_50 = b_32_40 + b_40_50

    b_0_24 = b_0_8 + b_8_16 + b_16_24
    b_24_50 = b_24_32 + b_32_40 + b_40_50

    band_energy = [b_0_8, b_8_16, b_16_24, b_24_32, b_32_40, b_40_50, b_0_16, b_16_32, b_32_50, b_0_24, b_24_50]
    return band_energy


def band_energy_3 (data_1, data_2, data_3):
    band_energy_3 =[]
    if len(data_1) == len(data_2) == len(data_3):
        for i in range(len(band_energy(data_1))):
            band_energy_3.append(band_energy(data_1)[i] + band_energy(data_1)[i] + band_energy(data_1)[i])
    return band_energy_3


def freq_feature(data_set):
    ff_vec = [max_index(data_set), mean_freq(data_set), stats.skew(data_set), stats.kurtosis(data_set)]
    return ff_vec


def correlation_x_y_z(_x, _y, _z):
    corr = []
    corr.extend(np.correlate(_x, _y))
    corr.extend(np.correlate(_x, _z))
    corr.extend(np.correlate(_y, _z))
    return corr


def angel(data_1, data_2):
    _angel = [math.acos(np.dot(data_1, data_2)/math.sqrt(np.dot(data_1, data_1) * math.sqrt(np.dot(data_2, data_2))))]
    return _angel


def signal_mean(data_1, data_2, data_3):
    signal_mean = [np.mean(data_1), np.mean(data_2), np.mean(data_3)]
    return signal_mean

filter_data_dir = "C:\\gd_data\\filter_data"
feature_vector_dir = "C:\\gd_data\\feature_vector"
data_label = ["motionRotationRateX", "motionRotationRateY", "motionRotationRateZ",
              "motionUserAccelerationX", "motionUserAccelerationY", "motionUserAccelerationZ",
              "motionGravityX", "motionGravityY", "motionGravityZ"]
for parents, dir_names, file_names in os.walk(filter_data_dir):
    for file_name in file_names:
        line_num = 0
        fin = open(filter_data_dir + "\\" + file_name, "r")  # count lines
        line = fin.readlines()
        line_num = len(line)
        fin.close()

        x = []
        x_jerk = []

        fileout = open(feature_vector_dir + "\\" + file_name.split('_')[0] + "_feature_vec.txt", "w", encoding="utf8")

        for i in range(9):
            y = []
            fin = open(filter_data_dir + "\\" + file_name, "r")
            for line in fin:
                line = line.strip()
                line_word = line.split("|")  # every line's [i]var write into y[]
                y.append(float(line_word[i]))
            x.append(y)
            fin.close()

        for j in range(len(x[0])//64 - 1):
            feature_vec = []

            for i in range(0, 9, 3):

                y1 = x[i][j*64:(j+2)*64]
                y2 = x[i+1][j*64:(j+2)*64]
                y3 = x[i+2][j*64:(j+2)*64]
                if i == 0:
                    r_mean = signal_mean(y1, y2, y3)
                elif i == 3:
                    acc_mean = signal_mean(y1, y2, y3)
                elif i == 6:
                    g_mean = signal_mean(y1, y2, y3)
                y_mag = magnitude(y1, y2, y3)
                feature_vec.extend(simple_feature(y1))
                feature_vec.extend(simple_feature(y2))
                feature_vec.extend(simple_feature(y3))
                feature_vec.extend(sma_3(y1, y2, y3))
                feature_vec.extend(correlation_x_y_z(y1, y2, y3))
                feature_vec.extend(simple_feature(y_mag))
                feature_vec.extend(sma_1(y_mag))

                if i != 6:
                    y1_jerk = jerk(y1)
                    y2_jerk = jerk(y2)
                    y3_jerk = jerk(y3)
                    y_jerk_mag = magnitude(y1_jerk, y2_jerk, y3_jerk,)
                    y1_f = freq_component(y1)
                    y2_f = freq_component(y2)
                    y3_f = freq_component(y3)
                    if i == 3:
                        acc_jerk_mean = signal_mean(y1_jerk, y2_jerk, y3_jerk)
                    elif i == 0:
                        r_jerk_mean = signal_mean(y1_jerk, y2_jerk, y3_jerk)
                    y_mag_f = freq_component(y_mag)
                    y1_jerk_f = freq_component(y1_jerk)
                    y2_jerk_f = freq_component(y2_jerk)
                    y3_jerk_f = freq_component(y3_jerk)
                    y_jerk_mag_f = freq_component(y_jerk_mag)

                    feature_vec.extend(simple_feature(y1_jerk))
                    feature_vec.extend(simple_feature(y2_jerk))
                    feature_vec.extend(simple_feature(y3_jerk))
                    feature_vec.extend(sma_3(y1_jerk, y2_jerk, y3_jerk))
                    feature_vec.extend(correlation_x_y_z(y1_jerk, y2_jerk, y3_jerk))
                    feature_vec.extend(simple_feature(y_jerk_mag))
                    feature_vec.extend(sma_1(y_jerk_mag))

                    feature_vec.extend(simple_feature(y1_f))
                    feature_vec.extend(freq_feature(y1_f))
                    feature_vec.extend(simple_feature(y2_f))
                    feature_vec.extend(freq_feature(y2_f))
                    feature_vec.extend(simple_feature(y3_f))
                    feature_vec.extend(freq_feature(y3_f))
                    feature_vec.extend(sma_3(y1_f, y2_f, y3_f))
                    feature_vec.extend(band_energy_3(y1_f, y2_f, y3_f))

                    feature_vec.extend(simple_feature(y_mag_f))
                    feature_vec.extend(freq_feature(y_mag_f))
                    feature_vec.extend(sma_1(y_mag_f))

                    feature_vec.extend(simple_feature(y1_jerk_f))
                    feature_vec.extend(freq_feature(y1_jerk_f))
                    feature_vec.extend(simple_feature(y2_jerk_f))
                    feature_vec.extend(freq_feature(y2_jerk_f))
                    feature_vec.extend(simple_feature(y3_jerk_f))
                    feature_vec.extend(freq_feature(y3_jerk_f))
                    feature_vec.extend(sma_3(y1_jerk_f, y2_jerk_f, y3_jerk_f))
                    if i == 3:
                        feature_vec.extend(band_energy_3(y1_jerk_f, y2_jerk_f, y3_jerk_f))

                    feature_vec.extend(simple_feature(y_jerk_mag_f))
                    feature_vec.extend(freq_feature(y_jerk_mag_f))
                    feature_vec.extend(sma_1(y_jerk_mag_f))

            feature_vec.extend(angel(acc_mean, g_mean))
            feature_vec.extend(angel(acc_jerk_mean, g_mean))
            feature_vec.extend(angel(r_mean, g_mean))
            feature_vec.extend(angel(r_jerk_mean, g_mean))
            feature_vec.extend(angel([1, 0, 0], g_mean))
            feature_vec.extend(angel([0, 1, 0], g_mean))
            feature_vec.extend(angel([0, 0, 1], g_mean))

            for data in feature_vec:
                fileout.write(str(data) + "|")
            fileout.write("\n")
        fileout.close()






