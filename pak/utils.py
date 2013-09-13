#!/usr/bin/python2.7
"""Utility classes and methods for manipulating pak archives."""

import os, sys, time

def fmt_size(b):
    """Convert byte size into human readable format."""
    for s in ['B', 'kB', 'MB', 'GB', 'TB']:
        if b < 1024:
            return '%4.1f %s' % (b, s)
        b /= 1024.0
    return '%4.1f PB' % b

class Confirm_Replace(object):
    
    def __init__(self):
        self.default = None
        
    def dialog(self, file_name, new_size):
        """Dialog prompt to handle filename conflicts.
        
        Prompts user for input when filenames conflict. Function will return a
        tuple (choice, new_name), where choice is one of 'y', 'n', 'r' and
        new_name is the replacement name should the file be renamed.

        Arguments:
        file_name -- the filename, including path (absolute or relative)
        new_size -- size of the replacement file in bytes
        """
        ans = self.default
        if not ans:
            file_size = fmt_size(os.path.getsize(file_name))
            file_date = time.ctime(os.path.getmtime(file_name))
            print "File %s already exists, would you like to replace" % file_name
            print "%s\tsize: %s\tmodified: %s" % (file_name, file_size, file_date)
            print "with"
            print "%s\tsize: %s" % (file_name, fmt_size(new_size))

        while ans not in ['y', 'yes', 'always', 'a', 'n', 'no', 'r', 'rename', 'e']:
            sys.stdout.write("Yes / Always / No / neVer / Rename / always rEname (Y/A/N/V/R/E): ")
            ans = raw_input().lower()
        if ans[0] == 'y':
            return ('y', file_name)
        if ans[0] == 'a':
            self.default = 'a'
            return ('y', file_name)
        if ans[0] == 'n':
            return ('n', None)
        if ans[0] == 'v':
            self.default = 'v'
            return ('n', file_name)
        if ans[0] == 'e':
            self.default = 'e'
        root, ext = os.path.splitext(file_name)
        n = 1
        new_name = root + '_conflict%08d'%n + ext
        while os.path.lexists(new_name):
            n += 1
            new_name = root + '_conflict%08d'%n + ext
        return (ans[0], new_name)
