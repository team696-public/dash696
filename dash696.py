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

class Gain_Frame(ttk.Frame, object):
    def __init__(self, parent):
        super(Gain_Frame, self).__init__()

        self.exposure_text = tk.StringVar()
        self.analog_text = tk.StringVar()
        self.digital_text = tk.StringVar()
        self.awb_red_text = tk.StringVar()
        self.awb_blue_text = tk.StringVar()
        self.y_text = tk.StringVar()
        self.u_text = tk.StringVar()
        self.v_text = tk.StringVar()
        self.bits_per_second_text = tk.StringVar()
        self.frames_per_second_text = tk.StringVar()

        self.exposure_text.set("1.0")
        self.analog_text.set("1.0")
        self.digital_text.set("1.0")
        self.awb_red_text.set("1.0")
        self.awb_blue_text.set("1.0")
        self.y_text.set("128")
        self.u_text.set("128")
        self.v_text.set("128")
        self.bits_per_second_text.set("0.0")
        self.frames_per_second_text.set("0.0")

        self.exposure_label_1 = ttk.Label(self, text="exposure")
        self.exposure_label_2 = ttk.Label(self, textvariable = self.exposure_text)
        self.exposure_label_1.grid(row = 0, column = 0)
        self.exposure_label_2.grid(row = 0, column = 1)

        self.analog_label_1 = ttk.Label(self, text="analog")
        self.analog_label_2 = ttk.Label(self, textvariable = self.analog_text)
        self.analog_label_1.grid(row=1, column=0)
        self.analog_label_2.grid(row=1, column=1)

        self.digital_label_1 = ttk.Label(self, text="digital")
        self.digital_label_2 = ttk.Label(self, textvariable = self.digital_text)
        self.digital_label_1.grid(row=2, column=0)
        self.digital_label_2.grid(row=2, column=1)

        self.awb_red_label_1 = ttk.Label(self, text="AWB red")
        self.awb_red_label_2 = ttk.Label(self, textvariable = self.awb_red_text)
        self.awb_red_label_1.grid(row=3, column=0)
        self.awb_red_label_2.grid(row=3, column=1)

        self.awb_blue_label_1 = ttk.Label(self, text="AWB blue")
        self.awb_blue_label_2 = ttk.Label(self, textvariable = self.awb_blue_text)
        self.awb_blue_label_1.grid(row=4, column=0)
        self.awb_blue_label_2.grid(row=4, column=1)

        self.y_label_1 = ttk.Label(self, text="center Y")
        self.y_label_2 = ttk.Label(self, textvariable=self.y_text)
        self.y_label_1.grid(row=5, column=0)
        self.y_label_2.grid(row=5, column=1)

        self.u_label_1 = ttk.Label(self, text="center U")
        self.u_label_2 = ttk.Label(self, textvariable=self.u_text)
        self.u_label_1.grid(row=6, column=0)
        self.u_label_2.grid(row=6, column=1)

        self.v_label_1 = ttk.Label(self, text="center V")
        self.v_label_2 = ttk.Label(self, textvariable=self.v_text)
        self.v_label_1.grid(row=7, column=0)
        self.v_label_2.grid(row=7, column=1)

        self.bits_per_second_label_1 = ttk.Label(self, text="bits per second")
        self.bits_per_second_label_2 = ttk.Label(self, textvariable = self.bits_per_second_text)
        self.bits_per_second_label_1.grid(row=8, column=0)
        self.bits_per_second_label_2.grid(row=8, column=1)

        self.frames_per_second_label_1 = ttk.Label(self, text="frames per second")
        self.frames_per_second_label_2 = ttk.Label(self, textvariable=self.frames_per_second_text)
        self.frames_per_second_label_1.grid(row=9, column=0)
        self.frames_per_second_label_2.grid(row=9, column=1)

    def update(self, gain_tuple):
        exposure, analog_gain, digital_gain, awb_red_gain, awb_blue_gain, y, u, v, connections,\
                                                                        bits_per_second, frames_per_second = gain_tuple
        self.exposure_text.set("%10.3f" % (exposure))
        self.analog_text.set("%10.3f" %(analog_gain))
        self.digital_text.set("%10.3f" % (digital_gain))
        self.awb_red_text.set("%10.3f" % (awb_red_gain))
        self.awb_blue_text.set("%10.3f" % (awb_blue_gain))
        self.y_text.set("%3d" % (y))
        self.u_text.set("%3d" % (u))
        self.v_text.set("%3d" % (v))
        if bits_per_second > 0.0:
            self.bits_per_second_text.set("%12.3f K" % (bits_per_second))
        if frames_per_second > 0.0:
            self.frames_per_second_text.set("%10.3f" % (frames_per_second))


class Dash_696(ttk.Frame, object):
    def __init__(self, queue):
        super(Dash_696, self).__init__()
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.queue = queue
        self.gain_frame = Gain_Frame(self.master)
        self.gain_frame.pack(side=tk.LEFT)
        self.image_label = ttk.Label(self.master)# label for the video frame
        self.image_label.pack(side=tk.RIGHT)
        self.master.after(0, func=lambda: self.update_all())

    def update_image(self, cv_img):
        im = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        a = PIL.Image.fromarray(im)
        b = PIL.ImageTk.PhotoImage(image=a)
        self.image_label.configure(image=b)
        self.image_label._image_cache = b  # avoid garbage collection
        self.master.update()

    def update_all(self):
        cv_img = self.queue.get()
        cv_img, gain_tuple = self.queue.get()

        self.update_image(cv_img)
        self.gain_frame.update(gain_tuple)
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
            frame_secs = time.time() - start_secs
            if frame_secs > 0.0: print("Kb/sec = %.1f   frames/sec = %.1f" % (byte_count / frame_secs / 1000.0 * 8, 1.0 / frame_secs))
            print("exp= %u  gains: alog %.3f dig %.3f red %.3f blue %.3f" % (exposure, analog_gain, digital_gain, awb_red_gain, awb_blue_gain))
            print("yuv= %u %u %u" % (y, u, v))
            frames_per_second = 0.0
            bits_per_second = 0.0
            if frame_secs > 0:
                bits_per_second = byte_count / frame_secs / 1000.0 * 8
                frames_per_second = 1.0 / frame_secs
            start_secs = time.time()
            byte_count = 0
            connections = 1
            queue.put((i, (exposure, analog_gain, digital_gain, awb_red_gain, awb_blue_gain, y, u, v, connections,
                           bits_per_second, frames_per_second)))


if __name__ == '__main__':
   queue = multiprocessing.Queue()
   print 'queue initialized...'
   root = tk.Tk()
   root.wm_title("dash696")
   dash_696 = Dash_696(queue)
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

