#!/usr/bin/python2.7
import sqlalchemy as sqla
import codecs, re

uistring = '/mnt/500G/Games/dragonnest/extract/resource/uistring/uistring.xml'
message_re = re.compile(r'<message mid="(\d+)"><!\[CDATA\[(.+)\]\]></message>', re.UNICODE|re.DOTALL)

def readlines(f, bufsize):
    buf = u''
    data = True
    while data:
        data = f.read(bufsize)
        buf += data
        lines = buf.split('\r\n')
        buf = lines.pop()
        for line in lines:
            yield line
    yield buf

messages = []
with codecs.open(uistring, encoding='utf-8', mode='r') as f:
    for line in readlines(f, 524288):
        match = message_re.match(line)
        if match:
            messages.append({ 'id' : int(match.group(1)), '_Message' : match.group(2) })

engine = sqla.create_engine('sqlite:///dnt.db', echo=False)
metadata = sqla.MetaData()
table = sqla.Table('UISTRING', metadata,
        sqla.Column('id', sqla.Integer, primary_key=True),
        sqla.Column('_Message', sqla.Text))
metadata.create_all(engine)
engine.connect().execute(table.insert(), messages)
