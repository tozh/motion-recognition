import numpy as np
import scipy as spy
import sys
import math
import os
import os.path
from numpy import *


raw_data_dir = "C:\\gd_data\\raw_data"
tran_data_dir = "C:\\gd_data\\tran_data"
for parents, dir_names, file_names in os.walk(raw_data_dir):
    for file_name in file_names:
        fin = open(raw_data_dir + "\\" + file_name, "r")
        fileout = open(tran_data_dir + "\\" + file_name.split('.')[0] + "_tran.txt", "w", encoding="utf8")
        for line in fin:
            line = line.strip()
            line_word = line.split("|")
            yaw = line_word[0]
            pitch = line_word[1]
            roll = line_word[2]
            cy = cos(float(yaw))
            sy = sin(float(yaw))
            cp = cos(float(pitch))
            sp = sin(float(pitch))
            cr = cos(float(roll))
            sr = sin(float(roll))
            YAW = np.mat(str(cy) + ', 0, ' + str(-sy) + ';' + '0, 1, 0;' + str(sy) + ', 0, ' + str(cy))
            PITCH = np.mat('1, 0, 0;' + '0, ' + str(cp) + ', ' + str(sp) + ';' + '0, ' + str(-sp) + ', ' + str(cp))
            ROLL = np.mat(str(cr) + ', ' + str(sr) + ', 0;' + str(-sr) + ', ' + str(cr) + ', 0;' + '0, 0, 1')
            RM = YAW * PITCH * ROLL
            RMT = RM.T

            a = 3
            while a <= 9:
                XYZ_phone = np.mat(line_word[a] + ', ' + line_word[a+1] + ', ' + line_word[a+2])
                XYZ_ground = XYZ_phone * RMT.I
                for i in range(3):
                    fileout.write(str(asarray(XYZ_ground)[0][i]) + "|")
                a += 3
            fileout.write(file_name[0] + "\n")
        fin.close()
        fileout.close()


