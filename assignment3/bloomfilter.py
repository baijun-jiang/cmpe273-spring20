import hashlib

class Bloomfilter:

    def __init__(self, size):
        self.hashs = [hashlib.md5, hashlib.sha1, hashlib.sha224, hashlib.sha256, hashlib.sha384]
        self.bit_array = [0] * size
        self.size = size

    def add(self, data):
        data = data.encode('utf-8')

        for hash_func in self.hashs:
            index = int(hash_func(data).hexdigest(), 16) % self.size
            self.bit_array[index] = 1
    
    def is_member(self, data):
        data = data.encode('utf-8')

        for hash_func in self.hashs:
            index = int(hash_func(data).hexdigest(), 16) % self.size

            if self.bit_array[index] == 0:
                return False
        
        return True