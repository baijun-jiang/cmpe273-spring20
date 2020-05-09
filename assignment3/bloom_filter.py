import hashlib
import math
import mmh3
from bitarray import bitarray

class BloomFilter:

    def __init__(self, keys, false_positive_probability):
        self.size = int((round(-(keys * math.log10(false_positive_probability)) / (math.log10(2) * math.log10(2)))))
        self.hash_count = int(round((self.size / keys * math.log10(2))))
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add(self, data):

        for i in range(self.hash_count):
            index = mmh3.hash(data, i) % self.size
            self.bit_array[index] = 1
    
    def is_member(self, data):

        for i in range(self.hash_count):
            index = mmh3.hash(data, i) % self.size

            if self.bit_array[index] == 0:
                return False
        
        return True
