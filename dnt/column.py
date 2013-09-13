#!/usr/bin/python2.7
import struct

VARIABLE_LEN = 0

class _Column(object):
    """Prototype class for datatype objects."""
    datalen = VARIABLE_LEN

    def __init__(self, name):
        self.name = name

    def encode(self, data):
        pass

    def decode(self, data):
        pass

class Varchar(_Column):
    """Represents dnt format varchar fields."""
    datalen = VARIABLE_LEN
    markerlen = 2

    def encode(self, data):
        """Encode a unicode string to dnt byte format."""
        msg = data.encode('euckr')
        msglen = struct.pack('<H', len(msg))
        return msglen + msg

    def decode(self, data):
        """Decode a dnt varchar field to a unicode string."""
        return data.decode('euckr', 'replace')

    def decodelen(self, data):
        """Decode byte length of the varchar field excluding length marker."""
        return struct.unpack('<H', data)[0]

class Boolean(_Column):
    """Represents dnt format boolean fields."""
    datalen = 4

    def encode(self, data):
        """Encode a boolean to dnt format."""
        return struct.pack('?xxx', data)

    def decode(self, data):
        """Decode a dnt boolean field to a boolean."""
        return struct.unpack('?xxx', data)[0]

class Integer(_Column):
    """Represents dnt format unsigned Integer fields."""
    datalen = 4

    def encode(self, data):
        """Encode an unsigned integer to dnt format."""
        return struct.pack('<I', data)

    def decode(self, data):
        """Decode a dnt unsigned integer to an integer."""
        return struct.unpack('<I', data)[0]

class Float(_Column):
    """Represents a dnt format floating point field."""
    datalen = 4

    def encode(self, data):
        """Encode a floating point number to dnt format."""
        return struct.pack('<f', data)

    def decode(self, data):
        """Decode a dnt float to a float."""
        return struct.unpack('<f', data)[0]

