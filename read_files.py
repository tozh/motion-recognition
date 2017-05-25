# read the data files to create the raw data
import os
import os.path


total_raw_data_dir = "C:\\gd_data\\total_raw_data"
raw_data_dir = "C:\\gd_data\\raw_data"
see_raw_data_dir = "C:\\gd_data\\see_raw_data"
for parents, dir_names, file_names in os.walk(total_raw_data_dir):
    for file_name in file_names:
        i = 0
        line_num = 0
        fin = open(total_raw_data_dir + "\\" + file_name, "r")  # count lines
        line = fin.readlines()
        line_num = len(line)
        fin.close()

        line_num -= (line_num-400) % 64        # 调整成128的倍数为后面处理做准备

        fin = open(total_raw_data_dir + "\\" + file_name, "r")
        fileout = open(raw_data_dir + "\\" + file_name.split('.')[0] + ".txt", "w", encoding="utf8")
        fileout_see = open(see_raw_data_dir + "\\" + file_name.split('.')[0] + "_see.txt", "w", encoding="utf8")
        for line in fin:
            if 0 == i or (200 < i < (line_num - 200)):  # delete the data in the first 4s and last 4s
                line = line.strip()
                line_word = line.split("|")
                # delete the useless data:
                del line_word[30:34]
                del line_word[22:27]
                del line_word[0:13]
                for data in line_word:
                    if i > 0:
                        fileout.write(data + "|")
                    fileout_see.write("{0:30}".format(data))
                if i > 0:
                    fileout.write("\n")
                fileout_see.write("\n")
            i += 1
        fin.close()
        fileout.close()


# fin = open("C:\\gd_data\\raw_data\\0.txt", "r")   # 读空格型数据
# i = 0
# for line in fin:
#     if 0 == i:
#         new_line = []
#         line = line.strip()
#         line_word = line.split(" ")
#         for word in line_word:
#             word = word.strip()
#             if word != '':
#                 new_line.append(word)
#         print(new_line)
#     else:
#         break
#     i += 1
