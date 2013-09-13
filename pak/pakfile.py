#!/usr/bin/python2.7
import os, struct, zlib
import utils

_IDSTRING = b"EyedentityGames Packing File 0.1"

class PAKFile(object):

    def __init__(self, filename):
        self.file_info = []
        self.filename = filename
        self.confirm_replace = utils.Confirm_Replace().dialog

    def extract_file(self, file_info):
        """Extract file with file_info taken from self.read_filelist().
        
        PAK files can contain multiples of the same file, often with many
        malformed versions. In these cases, extract_file will not catch the
        raised zlib.error.
        """
        with open(self.filename, 'rb'):
            f.seek(zfile['offset'])
            zfile_zbytes = f.read(zfile['zsize'])
        return zlib.decompress(zfile_zbytes)

    def read_filelist(self):
        with open(self.filename, 'rb') as f:
            assert f.read(len(_IDSTRING)) == _IDSTRING, "Unrecognized File"
            f.seek(0x100, 0)
            assert f.read(4) == "\x0B\x00\x00\x00", "Unrecognized File"
            self.num_files = struct.unpack('<I', f.read(4))[0]
            self.info_offset = struct.unpack('<I', f.read(4))[0]
            f.seek(self.info_offset, 0)

            for n in range(self.num_files):
                name = f.read(0x100).partition('\x00')[0].decode('euckr')
                name = os.path.join(*name.split('\\'))
                zsize = struct.unpack('<I', f.read(4))[0]
                size = struct.unpack('<I', f.read(4))[0]
                zsize1 = struct.unpack('<I', f.read(4))[0]
                offset = struct.unpack('<I', f.read(4))[0]
                unk3 = struct.unpack('<I', f.read(4))[0]
                assert f.read(0x28) == '\x00'*0x28, "Corrupt file listing"
                self.file_info.append({
                    'name' : name,
                    'zsize' : zsize,
                    'size' : size,
                    'zsize1' : zsize1,
                    'offset' : offset,
                    'unk3' : unk3
                    })
            self.file_info.sort(key=lambda x: x['offset'])

    def extract_all(self, outdir):
        with open(self.filename, 'rb') as f:
            for zfile in self.file_info:
                out_fdir = os.path.join(outdir, os.path.dirname(zfile['name']))
                out_file = os.path.join(outdir, zfile['name'])

                if not os.path.isdir(out_fdir):
                    os.makedirs(out_fdir)

                if os.path.exists(out_file):
                    mode, out_file = self.confirm_replace(out_file, zfile['size'])
                    if mode == 'n':
                        continue

                f.seek(zfile['offset'])
                zfile_zbytes = f.read(zfile['zsize'])

                try:
                    zfile_bytes = zlib.decompress(zfile_zbytes)
                except zlib.error as e:
                    print zfile['name'], e
                    continue

                with open(out_file, 'wb') as outf:
                    outf.write(zfile_bytes)

    def write_header(self):
        # TODO
        pass

    def write_file(self):
        # TODO
        pass

    def write_all(self):
        # TODO
        pass

    def write_filelist(self):
        # TODO
        pass
