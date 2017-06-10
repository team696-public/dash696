import cv2
import urllib
import numpy as np
import struct

class Bbox:
    def __init__(self, x0=0, y0=0, x1=0, y1=0):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

def parse_tif_tags(jpg):
    TIFOFF = 12
    #struct.unpack('=cccHccccccc')
    mm, version, ifd_offset, ifd_count = struct.unpack('!HHIH', jpg[TIFOFF:TIFOFF+10])
    print(str(ifd_offset) + " " + str(ifd_count))
    columns = 0
    rows = 0
    bbox_offset = 0
    bbox_count = 0
    for ii in range(0, ifd_count):
        start_off = TIFOFF + ifd_offset + 2 + ii * 12
        tag, type, count, num = struct.unpack('!HHII', jpg[start_off:start_off + 12])
        print("ttcn " + str(tag) + " " + str(type) + " " + str(count) + " " + str(num))

        if tag == 0x0100:
            columns = num
        elif tag == 0x0101:
            rows = num
        elif tag == 0x9696:
            bbox_count = count
            bbox_offset = num
    print("crb = " + str(columns) + " " + str(rows) + " " + str(bbox_count) + " " + str(bbox_offset))
    bbox_list = []
    if bbox_offset > 0:
        for ii in range(0, bbox_count / 4):
            start_off = TIFOFF + bbox_offset + ii * 8
            x0, y0, x1, y1 = struct.unpack('!HHHH', jpg[start_off:start_off + 8])
            bbox_list.append(Bbox(x0, y0, x1, y1))
            print("bbox " + str(x0) + " " + str(y0) + " " + str(x1) + " " + str(y1))




stream = urllib.urlopen('http://10.0.1.15:8080/?action=stream')
bytes = ''
while True:
    bytes += stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        parse_tif_tags(jpg)
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
        cv2.imshow('i', i)
        if cv2.waitKey(1) == 27:
            exit(0)
