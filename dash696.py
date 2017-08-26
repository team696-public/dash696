import ttk
import Tkinter as tk
import multiprocessing
import struct
import time
import urllib

import PIL.Image
import PIL.ImageTk
import cv2
import numpy as np


#tkinter GUI functions----------------------------------------------------------
def quit_(root, process):
   process.join()
   root.destroy()
   
class Dash_696_Gui:
    def __init__(self, master, queue):
        self.master = master
        self.queue = queue
        self.image_label = tk.Label(master)# label for the video frame
        self.image_label.pack()
        self.master.after(0, func=lambda: self.update_all())

    def update_image(self):
       frame = self.queue.get()
       im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
       a = PIL.Image.fromarray(im)
       b = PIL.ImageTk.PhotoImage(image=a)
       self.image_label.configure(image=b)
       self.image_label._image_cache = b  # avoid garbage collection
       self.master.update()

    def update_all(self):
       # type: () -> object
       self.update_image()
       self.master.after(0, func=lambda: self.update_all())

def parse_tif_tags(jpg):
    TIFOFF = 12
    mm, version, ifd_offset, ifd_count = struct.unpack('!HHIH', jpg[TIFOFF:TIFOFF+10])
    exposure = 0
    analog_gain = 0.0
    digital_gain = 0.0
    awb_red_gain = 0.0
    awb_blue_gain = 0.0
    gain_offset = 0
    gain_count = 0
    bbox_offset = 0
    bbox_count = 0
    y = 0
    u = 0
    v = 0
    for ii in range(0, ifd_count):
        start_off = TIFOFF + ifd_offset + 2 + ii * 12
        tag, type, count, num = struct.unpack('!HHII', jpg[start_off:start_off + 12])
        if tag == 0x9697:
            exposure = num
        elif tag == 0x9698:
            gain_count = count
            gain_offset = num
        elif tag == 0x9699:
            tag, type, count, y, u, v = struct.unpack('!HHIBBB', jpg[start_off:start_off + 11])
        elif tag == 0x9696:
            bbox_count = count
            bbox_offset = num

    if (gain_offset > 0 and gain_count == 4):
        off = TIFOFF + gain_offset
        analog_gain, digital_gain, awb_red_gain, awb_blue_gain = struct.unpack('!ffff', jpg[off:off + 16])

    rect_list = []
    if bbox_offset > 0:
        for ii in range(0, bbox_count / 4):
            start_off = TIFOFF + bbox_offset + ii * 8
            x0, y0, x1, y1 = struct.unpack('!HHHH', jpg[start_off:start_off + 8])
            rect_list.append(((x0, y0), (x1, y1)))
    return (exposure, analog_gain, digital_gain, awb_red_gain, awb_blue_gain, y, u, v, rect_list)

def connect_to_server(ip_port):
    connected = False
    while not connected:
        try:
            stream = urllib.urlopen('http://10.0.1.15:8080/?action=stream')
            connected = True
        except IOError as e:
            print("can't urlopen " + ip_port + " " + str(e))
    return stream



#multiprocessing image processing functions-------------------------------------
def image_capture(queue):


    bytes = ''
    byte_count = 0
    start_secs = time.time()
    default_ip_port = "10.0.1.15:8080"
    stream = connect_to_server(default_ip_port)
    while True:
        buf = stream.read(1024)
        byte_count += len(buf)
        bytes += buf
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            exposure, analog_gain, digital_gain, awb_red_gain, awb_blue_gain, y, u, v, rect_list = parse_tif_tags(jpg)
            bytes = bytes[b + 2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            for rect in rect_list:
                cv2.rectangle(i, rect[0], rect[1], (0, 0, 255))
            queue.put(i)
            frame_secs = time.time() - start_secs
            if frame_secs > 0.0: print("Kb/sec = %.1f   frames/sec = %.1f" % (byte_count / frame_secs / 1000.0 * 8, 1.0 / frame_secs))
            print("exp= %u  gains: alog %.3f dig %.3f red %.3f blue %.3f" % (exposure, analog_gain, digital_gain, awb_red_gain, awb_blue_gain))
            print("yuv= %u %u %u" % (y, u, v))
            start_secs = time.time()
            byte_count = 0


if __name__ == '__main__':
   queue = multiprocessing.Queue()
   print 'queue initialized...'
   root = tk.Tk()
   root.wm_title("dash696")
   dash_696_gui = Dash_696_Gui(root, queue)
   p = multiprocessing.Process(target=image_capture, args=(queue,))
   p.start()
   print 'image capture process has started...'
   # quit button
   #quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root,p))
   #quit_button.pack()

   # setup the update callback

   #print 'root.after was called...'
   root.mainloop()
   print 'mainloop exit'
   p.join()
   print 'image capture process exit'

