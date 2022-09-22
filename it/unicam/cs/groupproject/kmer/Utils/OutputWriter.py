import os


class OutputWriter:
    __file_name = ""

    __out_file = None
    __new_out_file = None
    __new_out_path = ""
    __out_file_path = ""
    __row_lenght = 0

    def __init__(self, filename, path):
        self.__file_name = filename
        self.__out_file = open(path, "rb")
        self.__new_out_path = self.__create_temp_file(path)
        self.__out_file_path = path

    def write_to_output(self, kmer_dictionary):
        if len(kmer_dictionary) == 0:
            return
        # print(self.__file_name,kmer_dictionary)
        file_lenght = self.__get_file_lenght(self.__out_file_path)
        values = list()
        kmer_keys = list()
        for key in kmer_dictionary:
            values.append(kmer_dictionary[key])
            kmer_keys.append(key)
        kmer_keys.sort()
        if file_lenght == 0:
            self.create_intestation(kmer_keys, len(kmer_keys), values)
        else:
            kmer_keys = self.__get_keys_from_dict(kmer_dictionary)
            new_kmer_indexs = self.read_and_write_intestation(kmer_keys)
            kmer_new_keys = self.get_new_kmer_from_changed(kmer_keys)
            kmer_keys = self.__get_keys_from_dict(kmer_dictionary)
            kmer_duplicates_indexs = self.get_index_of_changed_value(kmer_keys)
            filename_dict = self.get_all_file_names_inside_file()
            self.__out_file = open(self.__out_file_path, "rb")
            self.__new_out_file = open(self.__new_out_path, "rb+")
            self.get_row_length()
            kmer_duplicates_values = self.get_dupl_kmer_value_from_dict(kmer_dictionary)
            kmer_new_values = list()
            for key in kmer_dictionary:
                if key in kmer_new_keys:
                    kmer_new_values.append(kmer_dictionary[key])
            for key in filename_dict:
                self.__out_file.seek(filename_dict[key], 0)
                print(new_kmer_indexs, kmer_new_values, kmer_duplicates_indexs, list(kmer_duplicates_values), key)
                self.write_new_out_line(new_kmer_indexs, kmer_new_values, kmer_duplicates_indexs,
                                        list(kmer_duplicates_values), key)
            # print(self.__new_out_file.tell())
            self.__new_out_file.seek(0, 2)
            if not self.__file_name in filename_dict:
                kmer_index = self.__get_index_of_kmer(kmer_dictionary)
                kmer_values = self.__get_kmer_order_values(kmer_keys, kmer_dictionary)
                # print(self.__file_name, kmer_index, kmer_values)
                self.write_new_line(kmer_index, kmer_values)
                # print("----------------")
        self.close_all_files()
        os.remove(self.__out_file_path)
        os.rename(self.__new_out_path, self.__out_file_path)

    def create_intestation(self, kmer_keys, kmer_len, kmer_count):
        with open(self.__new_out_path, "wb") as file:
            index_kmer = 0
            f_line_tell = 0
            if kmer_len == 0:
                file.write(b'id\n')
                f_line_tell = file.tell()
            else:
                k = 0
                v = 0
                while v < len(kmer_count) + 1:
                    s = ""
                    if index_kmer == 0:
                        s = "id,"
                        index_kmer += 1
                    elif index_kmer == kmer_len + 1:
                        s = str(kmer_keys[v - 1]) + "\n"
                    else:
                        s = str(kmer_keys[v - 1]) + ","
                    file.write(s.encode())
                    v += 1
                    index_kmer += 1
            file.close()
        if kmer_len > 0:
            self.__write_new_kmer_count(kmer_count, f_line_tell)

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

    def __get_keys_from_dict(self, kmer_dict):
        l = list()
        for key in kmer_dict:
            l.append(key)
        l.sort()
        return l

    def get_all_file_names_inside_file(self):
        filename_list = dict()
        with open(self.__out_file_path, "rb") as file:
            readed_value = ""
            index_column, index_row = 0, 0
            while True:
                c = file.read(1)
                if not c:
                    break
                if c == b"\n" or c == b"\r":
                    if index_column == 0 and not index_row == 0:
                        filename_list[readed_value] = file.tell() - (len(readed_value) + 1)
                    index_row += 1
                    index_column = 0
                    readed_value = ""
                elif c == b",":
                    if not index_row == 0 and index_column == 0:
                        filename_list[readed_value] = file.tell() - (len(readed_value) + 1)
                    readed_value = ""
                    index_column += 1
                else:
                    readed_value += c.decode('utf-8')

            file.close()
        return filename_list

    def __create_temp_file(self, path):
        new_file_path = self.__get_new_file_name(path)
        if not os.path.exists(new_file_path):
            self.__new_out_file = open(new_file_path, "x")
            self.__new_out_file.close()
        else:
            self.__new_out_file = open(new_file_path, "wb+")
            self.__new_out_file.close()
        return new_file_path

    def read_and_write_intestation(self, kmer_list):
        """
        Questo metodo serve per leggere l'intestazione dal vecchio file e riscriverla in quello nuovo.
        :param: kmer_list: i kmer da aggiungere
        :return: gli indici dei nuovi kmer
        """
        index_column = 0
        readed_value = ""
        index_list = 0
        previous_readed = ""
        index_new_kmer = list()
        list_new_kmer = self.get_new_kmer_from_changed(kmer_list)
        self.__out_file = open(self.__out_file_path, "rb")
        self.__new_out_file = open(self.__new_out_path, "wb")
        self.__new_out_file.seek(0, 0)
        while True:
            c = self.__out_file.read(1)
            if not c or c == b'\n' or c == b'\r':
                if index_column == 0:
                    self.__new_out_file.write(b'id\n')
                elif index_list <= len(list_new_kmer) - 1:
                    s = readed_value + ","
                    self.__new_out_file.write(s.encode('utf-8'))
                    index_column += 1
                    index_new_kmer.extend(self.__add_remain_kmer_to_end(list_new_kmer, index_list, index_column))
                else:
                    s = readed_value + "\n"
                    self.__new_out_file.write(s.encode())
                break
            elif c == b',':
                if index_column == 0:
                    self.__new_out_file.write(b'id,')
                elif len(list_new_kmer) - 1 >= index_list and previous_readed < list_new_kmer[
                    index_list] < readed_value:
                    s = list_new_kmer[index_list] + ","
                    index_new_kmer.append(index_column)
                    self.__new_out_file.write(s.encode())
                    self.__out_file.seek(-(len(list_new_kmer[index_list]) + 1), 1)
                    previous_readed = list_new_kmer[index_list]
                    index_list += 1
                else:
                    self.__write_kmer_to_out(index_column, readed_value)
                    previous_readed = readed_value
                index_column += 1
                readed_value = ""

            else:
                readed_value += c.decode()
        self.close_all_files()
        return index_new_kmer

    def __write_kmer_to_out(self, index_column, readed_value):
        if index_column == 0:
            self.__new_out_file.write(b'id,')
        else:
            s = readed_value + ","
            self.__new_out_file.write(s.encode())
        self.__new_out_file.flush()

    def get_index_of_changed_value(self, kmer_key_values):
        list_of_index = list()
        with open(self.__new_out_path, "rb") as file:
            column_index = 0
            readed_value = ""
            file.seek(0, 0)
            while True:
                c = file.read(1)
                if not c or c == b"\r" or c == b"\n":
                    if readed_value in kmer_key_values:
                        list_of_index.append(column_index)
                    break
                elif c == b',':
                    if readed_value in kmer_key_values:
                        list_of_index.append(column_index)
                    column_index += 1
                    readed_value = ""
                else:
                    readed_value += c.decode()
            file.close()
        return list_of_index

    def get_new_kmer_from_changed(self, kmer_list):
        """
        Questo metodo determina quali sono i nuovi kmer da aggiungere all'intestazione del file.
        :param kmer_list: i kmer da aggiungere
        :return: una lista contenente i kmer che non sono già presenti nel file.
        """
        l = kmer_list
        with open(self.__out_file_path, "rb") as f:
            readed_value = ""
            f.seek(0, 0)
            while True:
                c = f.read(1)
                if not c or c == b"\n" or c == b"\r":
                    if readed_value in kmer_list:
                        l.remove(readed_value)
                    break
                elif c == b",":
                    if readed_value in kmer_list:
                        l.remove(readed_value)
                    readed_value = ""
                else:
                    readed_value += c.decode()

        self.close_all_files()
        return l

    def __add_remain_kmer_to_end(self, list_new_kmer, index_list, index_column):
        i = index_list
        l = list()
        ic = index_column
        while i <= len(list_new_kmer) - 1:
            s = list_new_kmer[i]
            if i == len(list_new_kmer) - 1:
                s += "\n"
                self.__new_out_file.write(s.encode())
            else:
                s += ","
                self.__new_out_file.write(s.encode())
            self.__new_out_file.flush()
            l.append(ic)
            ic += 1
            i += 1
        return l

    def close_all_files(self):
        if not self.__out_file.closed:
            self.__out_file.close()
        if not self.__new_out_file.closed:
            self.__new_out_file.close()

    def __write_new_kmer_count(self, kmer_count, first_line_pos):
        index_kmer = 0
        kmer_len = len(kmer_count)
        with open(self.__new_out_path, "ab") as file:
            file.seek(first_line_pos, 0)
            v = 0
            while v < len(kmer_count) + 1:
                s = ""
                if v == 0:
                    s = self.__file_name + ","
                    index_kmer += 1
                elif v == kmer_len:
                    s = str(kmer_count[v - 1]) + "\n"
                else:
                    s = str(kmer_count[v - 1]) + ","
                file.write(s.encode())
                v += 1
            file.close()

    def write_new_out_line(self, new_kmer_indexs, kmer_new_values, kmer_duplicates_indexs, kmer_duplicates_values,
                           actual_filename):
        index_column = 0
        readed_value = ""
        index_kmer_dup = 0
        index_kmer_new_key = 0
        line = 0
        self.__new_out_file.seek(0, 2)
        # print( kmer_duplicates_indexs, kmer_duplicates_values)
        while index_column < self.__row_lenght:
            c = self.__out_file.read(1)
            if not c:
                j2 = [i for i in new_kmer_indexs if i >= index_column]
                for vv in range(len(j2)):
                    if actual_filename == self.__file_name:
                        if vv == len(j2) - 1:
                            s = str(kmer_new_values[vv]) + "\n"
                        else:
                            s = str(kmer_new_values[vv]) + ","
                    else:
                        if vv == len(j2) - 1:
                            s = str(0) + "\n"
                        else:
                            s = str(0) + ","
                    self.__new_out_file.write(s.encode('utf-8'))
                    if c == b"\n" or c == b"\r":
                        line += 1
                break
            if c == b"," or c == b"\n" or c == b"\r":
                v = readed_value
                if index_column in new_kmer_indexs:
                    # se il kmer è nuovo
                    if not actual_filename == self.__file_name:
                        v = str(0)
                    else:
                        v = kmer_new_values[index_kmer_new_key]
                        index_kmer_new_key += 1
                    self.__out_file.seek(-(len(readed_value) + 1), 1)
                elif index_column in kmer_duplicates_indexs:
                    if not actual_filename == self.__file_name:
                        v = readed_value
                    else:
                        v = str(int(kmer_duplicates_values[index_kmer_dup] + int(readed_value)))
                        # print(self.__new_out_file.tell())
                    index_kmer_dup += 1
                else:
                    v = readed_value
                if index_column == self.__row_lenght - 1:
                    s = str(v) + "\n"
                else:
                    s = str(v) + ","
                self.__new_out_file.write(s.encode('utf-8'))
                if c == b"\n" or c == b"\r":
                    line += 1
                readed_value = ""
                index_column += 1
            else:
                readed_value += c.decode('utf-8')

    def get_row_length(self):
        if self.__new_out_file.closed:
            self.__new_out_file = open(self.__new_out_path, "rb+")
        if self.__out_file.closed:
            self.__out_file = open(self.__out_file_path, "rb")
        self.__new_out_file.seek(0, 0)

        index = 0
        readed_value = ""
        while True:
            c = self.__new_out_file.read(1)
            if not c or c == b"\n" or c == b"\r":
                if not readed_value == "":
                    index += 1
                break
            else:
                if c == b",":
                    if not readed_value == "":
                        index += 1
                    readed_value = ""
                else:
                    readed_value += c.decode('utf-8')
        self.__row_lenght = index
        return index

    def write_new_line(self, new_kmer_index, kmer_new_values):
        self.__new_out_file.seek(0, 2)
        index_column = 0
        index_knv = 0
        print(new_kmer_index)
        while index_column < self.__row_lenght:
            if index_column == 0:
                v = self.__file_name
                s = ","
            else:
                if index_column in new_kmer_index:
                    v = str(kmer_new_values[index_knv])
                    index_knv += 1
                else:
                    v = str(0)
                if index_column == self.__row_lenght-1:
                    s = "\n"
                else:
                    s = ","
            string = v + s
            print("scrivendo..."+string+" alla colonna:"+str(index_column)+" con knv:"+str(index_knv))
            index_column += 1
            self.__new_out_file.write(string.encode('utf-8'))

    def __get_index_of_kmer(self, kmer_dictionary):
        self.__new_out_file.seek(0, 0)
        l = list()
        readed_value = ""
        ic = 0
        while True:
            c = self.__new_out_file.read(1)
            if not c or c == b'\r' or c == b'\n':
                print(readed_value,kmer_dictionary.keys(),readed_value in kmer_dictionary)
                if readed_value in kmer_dictionary:
                    l.append(ic)
                break
            elif c == b",":
                print(readed_value, kmer_dictionary.keys(), readed_value in kmer_dictionary,ic)
                if readed_value in kmer_dictionary:
                    l.append(ic)
                ic += 1
                readed_value = ""
            else:
                readed_value += c.decode('utf-8')
        return l

    def get_dupl_kmer_value_from_dict(self, kmer_dict):
        ic = 0
        readed_value = ""
        l = list()
        # print(kmer_dict)
        self.__new_out_file.seek(0, 0)
        while True:
            c = self.__new_out_file.read(1)
            if not c or c == b'\r' or c == b'\n':
                if ic != 0:
                    if readed_value in kmer_dict:
                        l.append(kmer_dict[readed_value])
                break
            else:
                if c == b",":
                    if not ic == 0:
                        if readed_value in kmer_dict:
                            l.append(kmer_dict[readed_value])
                    readed_value = ""
                    ic += 1
                else:
                    readed_value += c.decode('utf-8')
        # print(l)
        return l

    def __get_kmer_order_values(self, kmer_keys, kmer_dictionary):
        l = list()
        for key in kmer_keys:
            l.append(kmer_dictionary[key])
        return l
