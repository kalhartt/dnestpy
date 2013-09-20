#!/usr/bin/python2.7
import os
from pak.pakfile import PAKFile

#dn_dir = '/mnt/win8/Nexon/DragonNest/'
#out_dir = '/mnt/500G/Games/dragonnest/extract/'
dn_dir = '/home/alex/downloads'
out_dir = '/home/alex/downloads'
pak_filenames = [ os.path.join(dn_dir, x) for x in os.listdir(dn_dir) if x.endswith('.pak') ]

for pak_filename in pak_filenames:
    print pak_filename
    mypak = PAKFile(pak_filename)
    mypak.read_filelist()
    mypak.extract_all(out_dir)
