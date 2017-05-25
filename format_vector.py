import os
import os.path


format_vector_dir = "C:\\gd_data\\format_vector"
feature_vector_dir = "C:\\gd_data\\feature_vector"

for parents, dir_names, file_names in os.walk(feature_vector_dir):
    for file_name in file_names:
        fin = open(feature_vector_dir + "\\" + file_name, "r")
        fileout = open(format_vector_dir + "\\" + "data", "a", encoding="utf8")
        for line in fin:
            fileout.write(file_name[0] + ' ')
            i = 1
            line = line.strip()
            line = line.strip('|')
            line_word = line.split("|")
            for data in line_word:
                fileout.write(str(i) + ':' + data + ' ')
                i += 1
            fileout.write("\n")
        fin.close()
        fileout.close()
