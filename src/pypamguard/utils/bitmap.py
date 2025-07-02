# bitmap.py

class Bitmap:
    def __init__(self, size: int = 0, fields: list = None, value: int = 0):
        """
        A class that represents a [labelled] bitmap. A bitmap
        is labelled when a list of fields is provided and each
        bit corresponds to a field.
        
        :param size: the number of bytes in the bitmap
        :param fields: a list of fields to label the bitmap from least significant to most significant.
            (defaults to None, in which case the bitmap is unlabelled and each bit corresponds only to an index)
        :param value: the initial value of the bitmap (defaults to 0)
        """

        self.fields2index = {}
        self.index2fields = {}
        
        if fields is not None:
            for index, field in enumerate(fields):
                self.fields2index[field] = index
                self.index2fields[index] = field
        
        self.size = size
        self.bits = value
    
    def __get_index(self, field_or_index):
        if isinstance(field_or_index, str):
            return self.fields2index[field_or_index]
        else:
            return field_or_index

    def set(self, field_or_index):
        """Sets the field or index in the bitmap. """
        index = self.__get_index(field_or_index)
        if index < 0 or index >= (self.size * 8):
            raise ValueError("Index out of range")
        self.bits |= 1 << index
    
    def clear(self, field_or_index):
        """Clears the field or index in the bitmap. """
        index = self.__get_index(field_or_index)
        if index < 0 or index >= (self.size * 8):
            raise ValueError("Index out of range")
        self.bits &= ~(1 << index)
    
    def is_set(self, field_or_index):
        """Returns True if the field or index is set in the bitmap. """
        index = self.__get_index(field_or_index)
        if index < 0 or index >= (self.size * 8):
            raise ValueError("Index out of range")
        return (self.bits & (1 << index)) != 0

    def get_set_bits(self):
        """Returns a list of fields or indices that are set in the bitmap. """
        return [
            self.index2fields.get(index, index)
            for index in range(self.size * 8)
            if (self.bits & (1 << index)) != 0
        ]
    
    def get_binary_representation(self):
        return bin(self.bits)[2:].zfill(self.size * 8)

    def __len__(self):
        return self.size * 8

    def __repr__(self):
        return f"Bitmap(size={self.size}, bits={self.bits}, set_bits={self.get_set_bits()})"
