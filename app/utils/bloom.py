import mmh3
from bitarray import bitarray

from app.utils.singleTon import Singleton

BIT_SIZE = 5000000


@Singleton
class BloomFilterUtils:
    def __init__(self):
        bit_array = bitarray(BIT_SIZE)
        bit_array.setall(0)

        self.bit_array = bit_array

    def add(self, data):
        point_list = self.get_postions(data)

        for b in point_list:
            self.bit_array[b] = 1

    def contains(self, data):
        point_list = self.get_postions(data)
        result = True
        for b in point_list:
            result = result and self.bit_array[b]
            if not result:
                break

        return result

    def get_postions(self, data):
        point1 = mmh3.hash(data, 41) % BIT_SIZE
        point2 = mmh3.hash(data, 42) % BIT_SIZE
        point3 = mmh3.hash(data, 43) % BIT_SIZE
        point4 = mmh3.hash(data, 44) % BIT_SIZE
        point5 = mmh3.hash(data, 45) % BIT_SIZE
        point6 = mmh3.hash(data, 46) % BIT_SIZE
        point7 = mmh3.hash(data, 47) % BIT_SIZE
        return [point1, point2, point3, point4, point5, point6, point7]
