import heapq
import os
class binarytreenode:
    def __init__(self,value,freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq

class encrypt:
    def __init__(self,path):
        self.path=path
        self.__heap=[]
        self.__codes={}
        self.__reversecodes={}

    def __makefrequencydict(self,text):
        freq_dict={}
        for char in text:
            if char not in freq_dict:
                freq_dict[char]=0
            freq_dict[char] += 1
        return freq_dict

    def __buildheap(self,freq_dict):
        for key in freq_dict:
            frequency = freq_dict[key]
            build_binary_tree = binarytreenode(key, frequency)
            heapq.heappush(self.__heap , build_binary_tree)

    def __buildtree(self):
        while(len(self.__heap)>1):
            make_node_1=heapq.heappop(self.__heap)
            make_node_2=heapq.heappop(self.__heap)

            freq_sum = make_node_1.freq + make_node_2.freq

            new_node= binarytreenode(None,freq_sum)

            new_node.left=make_node_1
            new_node.right=make_node_2

            heapq.heappush(self.__heap, new_node)
        return

    def __buildcodeshelper(self,root,curr_bits):
        if root is None:
            return

        if root.value is not None:
            self.__codes[root.value] = curr_bits
            self.__reversecodes[curr_bits] = root.value
            return

        self.__buildcodeshelper(root.left,curr_bits+"0")
        self.__buildcodeshelper(root.right,curr_bits+"1")

    def __buildcodes(self):
        root=heapq.heappop(self.__heap)
        self.__buildcodeshelper(root,"")

    def __get_encodedtext(self,text):
        encoded_text = " "
        for char in text:
            encoded_text += self.__codes[char]
        return encoded_text

    def __getpaddedencodedtext(self,encoded_text):

        padded_amount = 8-(len(encoded_text)%8)

        for i in range (padded_amount):
            encoded_text += "0"

        padded_info = "{0:08b}" . format(padded_amount)

        padded_encoded_text = padded_info + encoded_text
        return padded_encoded_text

    def __getbytesconverted(self,padded_encoded_text):
        array=[]
        for i in range(0,len(padded_encoded_text),8):
            byte = padded_encoded_text[i:i+8]
            array.append(int(byte,2))
        return array


    def compress(self):
        file_name,file_extension = os.path.splitext(self.path)
        output_path = file_name + ".bin"
        with open(self.path,'r+') as file , open(output_path,'wb') as output :
            text = file.read()
            text = text.rstrip()
            freq_dict = self.__makefrequencydict(text)
            self.__buildheap(freq_dict)
            self.__buildtree()
            self.__buildcodes()
            encoded_text = self.__get_encodedtext(text)
            padded_encoded_text = self.__getpaddedencodedtext(encoded_text)
            bytes_array = self.__getbytesconverted(padded_encoded_text)
            final_byte = bytes(bytes_array)
            output.write(final_byte)
        print('compreesseed')
        return output_path

    def __removepadding(self,text):
        padding_info = text[:8]
        extra_padding = int(padding_info,2)

        text = text[8:]
        text_after_padding_removed = text[:-1*extra_padding]

        return text_after_padding_removed

    def __decodetext(self,text):
        decoded_text =""
        current_bits=""

        for bit in text :
            current_bits += bit
            if current_bits in self.__reversecodes:
                charcter = self.__reversecodes[current_bits]
                decoded_text += charcter
                current_bits = ""
        return decoded_text


    def decompress(self,input_path):
        file_name, file_extension = os.path.splitext(self.path)
        output_path = file_name + "_decompressed" + ".txt"
        with open(input_path,'rb') as file, open(output_path,'w') as output:
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8,'0')
                bit_string += bits
                byte = file.read(1)
            actual_text = self.__removepadding(bit_string)
            decompressed_text = self.__decodetext(actual_text)
            output.write(decompressed_text)

path = r"E:\Pycharm python\sample_code.txt"
h=encrypt(path)
output_path = h.compress()
h.decompress(output_path)