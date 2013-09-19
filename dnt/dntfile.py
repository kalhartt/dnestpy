#!/usr/bin/python2.7
import struct
import column

_HEADER = b'\x00\x00\x00\x00'
_TAIL = b'\x05THEND'
_TYPEMAP = {
    1: column.Varchar,
    2: column.Boolean,
    3: column.Integer,
    4: column.Float,
    5: column.Float
}


class DNTFile(object):
    """Object for reading/writing DragonNest DNT files."""

    def __init__(self, filename):
        self.filename = filename
        self.columns = []
        self.rows = []

    def read_all(self):
        """Parses an entire DNT file."""
        self.parse_header()
        with open(self.filename, 'rb') as f:
            f.seek(self.row_start, 0)
            for i in range(self.num_rows):
                self.read_row(f)

            assert f.read() == _TAIL, "Unexpected EOF"

    def parse_header(self):
        """Parse DNT header to get column information and number of rows."""
        columns = []
        with open(self.filename, 'rb') as f:
            header = f.read(4)
            assert header == _HEADER, "Invalid header bytes: %s" % repr(header)
            self.num_columns = struct.unpack('<H', f.read(2))[0] + 1
            self.num_rows = struct.unpack('<I', f.read(4))[0]
            columns.append(column.Integer('id'))

            while len(columns) < self.num_columns:
                name_length = struct.unpack('<H', f.read(2))[0]
                name = f.read(name_length).decode('euckr')
                dtype = _TYPEMAP[struct.unpack('B', f.read(1))[0]]
                columns.append(dtype(name))

            self.row_start = f.tell()
        self.columns = columns

    def read_row(self, f):
        """Parse row starting at cursor location in open file f."""
        assert self.columns, "No columns defined."
        start = f.tell()
        data = []
        for col in self.columns:
            if col.datalen == column.VARIABLE_LEN:
                datalen = col.decodelen(f.read(col.markerlen))
                data.append(col.decode(f.read(datalen)))
            else:
                data.append(col.decode(f.read(col.datalen)))
        self.rows.append({
            'location': start,
            'data': data
        })

    def write_row(self, f, data):
        """Write a row at cursor location in open file f.

        Checks data for type matches with defined columns then blindly writes
        the values to the open file f. If overwriting a row, be sure
        the old and new row have identical encoded byte lengths.
        """
        assert len(data) == len(self.columns), "Data / Column length mismatch."
        out = ""
        for col, val in zip(self.columns, data):
            out += col.encode(val)
        f.write(out)
