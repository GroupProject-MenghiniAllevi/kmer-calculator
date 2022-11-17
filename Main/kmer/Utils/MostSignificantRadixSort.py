from Main.kmer.Utils.Reader import FastaReader

COUNT_SIZE = 17


class MostSignificantRadixSort:
    __values_list = list()
    __byte_table = []
    __string_length = 0
    __list_len = 0
    __alphabet = [sub for sub in FastaReader.ALPHABET if all(ele.isupper() for ele in sub)]
    __alphabet_dict = dict()
    __alphabet_len = 0

    def __init__(self, value_list):
        self.__values_list.clear()
        if len(value_list) == 0:
            ValueError("è stata inserita una lista vuota...")
        self.__from_list_to_list_of_list(value_list)
        self.__string_length = len(value_list[0])
        self.__list_len = len(value_list)
        self.__alphabet_len = len(self.__alphabet)

    def sort(self):
        exp = self.__string_length-1
        i = 0
        while exp > i:
            self.counting_sort(i)
            i += 1

    def get_list(self):
        l = list()
        for element in self.__values_list:
            s = ""
            for i in element:
                char = list(self.__alphabet_dict.keys())[list(self.__alphabet_dict.values()).index(i)]
                s += char
            l.append(s)
        return l


    def counting_sort(self, exp):
        arr_length = len(self.__values_list)
        output = [0] * arr_length
        count = [0] * len(self.__alphabet_dict)
        for i in range(arr_length):
            index = self.__values_list[i][exp]
            count[self.__alphabet_dict[self.from_number_get_char(index)]] += 1
        for i in range(1, self.__alphabet_len):
            count[i] += count[i - 1]
        for i in range(arr_length - 1, -1, -1):
            index = self.__values_list[i][exp]
            output[count[self.__alphabet_dict[self.from_number_get_char(index)]] - 1] = self.__values_list[i]
            count[self.__alphabet_dict[self.from_number_get_char(index)]] -= 1
        self.__values_list[:] = output

    def from_number_get_char(self,number):
        return list(self.__alphabet_dict.keys())[list(self.__alphabet_dict.values()).index(number)]

    def counting_elements(self, place_value):
        count = [0] * COUNT_SIZE
        for i in range(self.__list_len):
            count_index = self.__alphabet_dict[self.__values_list[i][place_value]]
            count[count_index-1] += 1
        for i in range(1,COUNT_SIZE):
            count[i] += count[i - 1]
        return count

    def reconstruct_output_count_sort(self, count, place_value):
        output = self.__values_list
        i = self.__string_length - 1
        i_index = 0
        while i_index < i:
            current_ele = output[i_index]
            place_elements = self.__alphabet_dict[self.__values_list[i_index][place_value]]
            count[place_elements] = - 1
            new_pos = count[place_elements]
            output[new_pos] = current_ele
            i_index += 1
        return output

    def __from_list_to_list_of_list(self, value_list):
        i = 0
        l = list()
        for m in self.__alphabet:
            l.append(m)
        l.sort()
        for j in l:
            self.__alphabet_dict[j] = i
            i += 1
        for element in value_list:
            l = list()
            for i in range(len(element)):
                char = element[i]
                value = self.__alphabet_dict[char.upper()]
                l.append(value)
            self.__values_list.append(l)

    def __get_all_char_at_index(self, char_index):
        d = dict()
        for i in self.__values_list:
            d[i] = i[char_index]
        return d

