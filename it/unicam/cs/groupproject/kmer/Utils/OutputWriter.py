import os

import pandas as pd
from csv import reader, writer


class OutputWriter:

    def __init__(self):
        pass

    def write_to_output(self, path, dictionary, lock, ith):
        lock.acquire()
        new_file_path = self.__get_new_file_name(path)
        if not os.path.exists(new_file_path):
            open(new_file_path, "x").close()
        if ith == 0:
            self.__write_first_time(path,dictionary)
            lock.release()
            return
        size = self.__get_file_lenght(path)
        i = 0
        print("size: ",size)
        with open(path,"r") as fr:
            fw = open(new_file_path,"a")
            i = 0
            list_temp = list()
            while i < size:
                line = fr.readline()
                line_split = line.split(",")
                if line_split[0] in dictionary:
                    fw.write(line_split[0]+","+str(line_split[1]+dictionary[line_split[0]])+"\n")
                    list_temp.append(line_split[0])
                i+=1
            for key, value in dictionary.items():
                if not key in list_temp:
                    fw.write(key + "," + str(value) + "\n")
        os.remove(path)
        os.rename(new_file_path, path)
        lock.release()

    def __get_new_file_name(self, path):
        indexs = [pos for pos, char in enumerate(path) if char == os.sep]
        index_to_remove = indexs[len(indexs) - 1]
        new_string = path[:index_to_remove]
        new_string = os.path.join(new_string, "new_out.csv")
        return new_string

    def __get_file_lenght(self, path):
        with open(path, "rb") as f:
            f.seek(0)
            f.seek(0, 2)
            size = f.tell()
            f.close()
            return size

    def __write_first_time(self, path, dictionary):
        with open(path, "a") as fw:
            for key, values in dictionary.items():
                _string = key + "," + str(values) + "\n"
                fw.write(_string)
