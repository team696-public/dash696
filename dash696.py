import cv2
import urllib
import numpy as np
import struct

def parse_tif_tags(jpg):
    TIFOFF = 12
    mm, version, ifd_offset, ifd_count = struct.unpack('!HHIH', jpg[TIFOFF:TIFOFF+10])
    columns = 0
    rows = 0
    bbox_offset = 0
    bbox_count = 0
    for ii in range(0, ifd_count):
        start_off = TIFOFF + ifd_offset + 2 + ii * 12
        tag, type, count, num = struct.unpack('!HHII', jpg[start_off:start_off + 12])
        if tag == 0x0100:
            columns = num
        elif tag == 0x0101:
            rows = num
        elif tag == 0x9696:
            bbox_count = count
            bbox_offset = num
    rect_list = []
    if bbox_offset > 0:
        for ii in range(0, bbox_count / 4):
            start_off = TIFOFF + bbox_offset + ii * 8
            x0, y0, x1, y1 = struct.unpack('!HHHH', jpg[start_off:start_off + 8])
            rect_list.append(((x0, y0), (x1, y1)))
    return (columns, rows, rect_list)




stream = urllib.urlopen('http://10.0.1.15:8080/?action=stream')
bytes = ''
while True:
    bytes += stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        cols, rows, rect_list = parse_tif_tags(jpg)
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
        for rect in rect_list:
            cv2.rectangle(i, rect[0], rect[1], (0,0,255))
        cv2.imshow('i', i)
        if cv2.waitKey(1) == 27:
            exit(0)
