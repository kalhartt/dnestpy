#!/usr/bin/python2.7
import os, struct
import sqlalchemy as sqla
from dnt.dntfile import DNTFile
from dnt import column

# Adjuts this as needed
dnt_filedir = '/mnt/500G/Games/dragonnest/extract/resource/ext'
dnt_filenames = [ os.path.join(dnt_filedir, x) for x in os.listdir(dnt_filedir) if x.endswith('.dnt') ]

_SQLTYPEMAP = {
        column.Varchar : sqla.String(255),
        column.Boolean : sqla.Boolean,
        column.Integer : sqla.Integer,
        column.Float : sqla.Float
        }

engine = sqla.create_engine('sqlite:///dnt.db', echo=False)
metadata = sqla.MetaData()

for dnt_filename in dnt_filenames:
    if os.stat(dnt_filename).st_size == 0:
        continue
    
    print dnt_filename
    dntfile = DNTFile(dnt_filename)
    dntfile.read_all()

    ## Column and Table Setup
    table_name = os.path.basename(dnt_filename[:-4])
    table_cols = []
    for col in dntfile.columns:
        if col.name == 'id':
            table_cols.append( sqla.Column('id', sqla.Integer, primary_key=True) )
        else:
            table_cols.append( sqla.Column(col.name, _SQLTYPEMAP[type(col)]) )
    table = sqla.Table(table_name, metadata, *table_cols)
    metadata.create_all(engine)

    col_names = [ x.name for x in dntfile.columns ]
    data = [ dict(zip(col_names, row['data'])) for row in dntfile.rows ]
    engine.connect().execute(table.insert(), data)
