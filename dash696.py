import ttk
import Tkinter as tk
import multiprocessing
import struct
import time
import urllib
import socket

import PIL.Image
import PIL.ImageTk
import cv2
import numpy as np

class Tcp_Tag:
    # These constants must match those with the same names in tcp_comms.h
    RASPICAM_QUIT =                   0
    RASPICAM_SATURATION =             1
    RASPICAM_SHARPNESS =              2
    RASPICAM_CONTRAST =               3
    RASPICAM_BRIGHTNESS =             4
    RASPICAM_ISO =                    5
    RASPICAM_METERING_MODE =          6
    RASPICAM_VIDEO_STABILISATION =    7
    RASPICAM_EXPOSURE_COMPENSATION =  8
    RASPICAM_EXPOSURE_MODE =          9
    RASPICAM_AWB_MODE =              10
    RASPICAM_AWB_GAINS =             11
    RASPICAM_IMAGE_FX =              12
    RASPICAM_COLOUR_FX =             13
    RASPICAM_ROTATION =              14
    RASPICAM_FLIPS =                 15
    RASPICAM_ROI =                   16
    RASPICAM_SHUTTER_SPEED =         17
    RASPICAM_DRC =                   18
    RASPICAM_STATS_PASS =            19
    RASPICAM_TEST_IMAGE_ENABLE =     20
    RASPICAM_YUV_WRITE_ENABLE =      21
    RASPICAM_JPG_WRITE_ENABLE =      22
    RASPICAM_DETECT_YUV_ENABLE =     23
    RASPICAM_BLOB_YUV =              24


class Tcp_Comms():
    def __init__(self, ip_addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip_addr, port))

    def _send_int_msg(self, tag, count, int0=0, int1=0, int2=0):
        if count == 0:
            data = struct.pack('!BBBB', tag, 0, 0, 0)
        elif count == 1:
            data = struct.pack('!BBBBI', tag, 0, 0, 0, int0)
        elif count == 2:
            data = struct.pack('!BBBBII', tag, 0, 0, 0, int0, int1)
        elif count == 3:
            data = struct.pack('!BBBBIII', tag, 0, 0, 0, int0, int1, int2)
        else:
            print("_send_int_msg saw bad count " + str(count))
            return
        bytes = self.sock.send(data)
        if bytes != len(data):
            print("_send_int_msg: short sock.send byte count (" + str(bytes) + "); expected " + str(len(data)) + "; ignoring")

    def _send_float_msg(self, tag, count, float0 = 0, float1 = 0, float2 = 0, float3 = 0):
        if count == 0:
            data = struct.pack('!BBBB', tag, 0, 0, 0)
        elif count == 1:
            data = struct.pack('!BBBBf', tag, 0, 0, 0, float0)
        elif count == 2:
            data = struct.pack('!BBBBff', tag, 0, 0, 0, float0, float1)
        elif count == 3:
            data = struct.pack('!BBBBfff', tag, 0, 0, 0, float0, float1, float2)
        elif count == 4:
            data = struct.pack('!BBBBffff', tag, 0, 0, 0, float0, float1, float2, float3)
        else:
            print("_send_int_msg saw bad count " + str(count))
            return
        bytes = self.sock.send(data)
        if bytes != len(data):
            print("_send_float_msg: short sock.send byte count (" + str(bytes) + "); expected " + str(len(data)) + "; ignoring")


    def send_saturation(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_SATURATION, 1, value)

    def send_sharpness(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_SHARPNESS, 1, value)

    def send_saturation(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_SATURATION, 1, value)

    def send_contrast(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_CONTRAST, 1, value)

    def send_brightness(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_BRIGHTNESS, 1, value)

    def send_iso(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_ISO, 1, value)

    def send_metering_mode(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_METERING_MODE, 1, value)

    def send_video_stabilisation(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_VIDEO_STABILISATION, 1, value)

    def send_exposure_compensation(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_EXPOSURE_COMPENSATION, 1, value)

    def send_expsoure_mode(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_EXPOSURE_MODE, 1, value)

    def send_awb_mode(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_AWB_MODE, 1, value)

    def send_awb_gains(self, red_gain, blue_gain):
        self._send_float_msg(Tcp_Tag.RASPICAM_AWB_GAINS, 2, red_gain, blue_gain)

    def send_image_fx(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_IMAGE_FX, 1, value)

    def send_colour_fx(self, red, green, blue):
        self._send_int_msg(Tcp_Tag.RASPICAM_COLOUR_FX, 3, red, green, blue)

    def send_rotation(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_ROTATION, 1, value)

    def send_flips(self, hflip, vflip):
        self._send_int_msg(Tcp_Tag.RASPICAM_FLIPS, 2, hflip, vflip)

    def send_roi(self, x, y, w, h):
        self._send_float_msg(Tcp_Tag.RASPICAM_ROI, 4, x, y, w, h)

    def send_shutter_speed(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_SHUTTER_SPEED, 1, value)

    def send_drc(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_DRC, 1, value)

    def send_stats_pass(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_STATS_PASS, 1, value)

    def send_test_image_enable(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_TEST_IMAGE_ENABLE, 1, value)

    def send_yuv_write_enable(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_YUV_WRITE_ENABLE, 1, value)

    def send_jpg_write_enable(self, value):
        self._send_int_msg(Tcp_Tag.RASPICAM_JPG_WRITE_ENABLE, 1, value)

    def send_blob_yuv(self, y_min, y_max, u_min, u_max, v_min, v_max):
        struct.pack('!BBBBBBB', Tcp_Tag.RASPICAM_BLOB_YUV, y_min, y_max, u_min, u_max, v_min, v_max)
        self.sock.send(str)










#tkinter GUI functions----------------------------------------------------------
class Awb_Widget():
    def __init__(self, parent, tcp_comms):
        self.value_list = ("off", "auto", "sun", "cloud", "shade", "tungsten", "fluorescent",
                      "incandescent", "flash", "horizon")
        self.value = tk.StringVar()
        self.value.set(self.value_list[0])
        self.widget = tk.OptionMenu(parent, self.value, *self.value_list, command=self.command)
        self.tcp_comms = tcp_comms

    def command(self, value):
        for ii in range(0, len(self.value_list)):
            if value == self.value_list[ii]: break
        print(value + " " + str(ii))
        self.tcp_comms.send_awb_mode(ii)

    def grid(self, row, column):
        self.widget.grid(row = row, column = column)

class Cam_Param_Frame(ttk.Frame, object):
    def __init__(self, parent, ip_addr):
        super(Cam_Param_Frame, self).__init__(parent)
        TCP_PORT = 10696
        tcp_comms = Tcp_Comms(ip_addr, TCP_PORT)
        self.awb_label = ttk.Label(self, text="AWB")
        self.awb_param = Awb_Widget(self, tcp_comms)
        self.awb_label.grid(row = 0, column = 0)
        self.awb_param.grid(row = 0, column = 1)

    def update(self):
        pass



class Gain_Frame(ttk.Frame, object):
    def __init__(self, parent):
        super(Gain_Frame, self).__init__(parent)

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

    def update(self, queue_entry):
        self.exposure_text.set("%10.3f" % (queue_entry.exposure_secs))
        self.analog_text.set("%10.3f" %(queue_entry.analog_gain))
        self.digital_text.set("%10.3f" % (queue_entry.digital_gain))
        self.awb_red_text.set("%10.3f" % (queue_entry.awb_red_gain))
        self.awb_blue_text.set("%10.3f" % (queue_entry.awb_blue_gain))
        self.y_text.set("%3d" % (queue_entry.y))
        self.u_text.set("%3d" % (queue_entry.u))
        self.v_text.set("%3d" % (queue_entry.v))
        if queue_entry.bits_per_second > 0.0:
            self.bits_per_second_text.set("%12.3f K" % (queue_entry.bits_per_second))
        if queue_entry.frames_per_second > 0.0:
            self.frames_per_second_text.set("%10.3f" % (queue_entry.frames_per_second))


class Dash_696(ttk.Frame, object):
    def __init__(self, ip_addr, queue):
        super(Dash_696, self).__init__()
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.queue = queue
        self.notebook = ttk.Notebook(self.master)
        self.tab0 = Gain_Frame(self.notebook)
        self.notebook.add(self.tab0, text="Gains")
        self.tab1 = Cam_Param_Frame(self.notebook, ip_addr)
        self.notebook.add(self.tab1, text="Camera Params")
        self.notebook.pack(side=tk.LEFT)
        self.image_label = ttk.Label(self.master)# label for the video frame
        self.image_label.pack(side=tk.RIGHT)
        self.do_quit = False
        self.master.after(0, func=lambda: self.update_all())

    def update_image(self, cv_img):
        im = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        a = PIL.Image.fromarray(im)
        b = PIL.ImageTk.PhotoImage(image=a)
        self.image_label.configure(image=b)
        self.image_label._image_cache = b  # avoid garbage collection
        self.master.update()

    def update_all(self):
        queue_entry = self.queue.get()
        if queue_entry.do_quit:
            self.quit()
        else:
            self.update_image(queue_entry.cv_img)
            self.tab0.update(queue_entry)
            self.tab1.update()
            self.master.after(0, func=lambda: self.update_all())

    def quit(self):
        self.master.quit() # quit mainloop()

class Image_Capture_Queue_Entry():
    def __init__(self,
                 cv_img,
                 exposure_secs = 0.0,
                 analog_gain = 0.0,
                 digital_gain = 0.0,
                 awb_red_gain = 0.0,
                 awb_blue_gain = 0.0,
                 y = 0,
                 u = 0,
                 v = 0,
                 udp_connection_status = 0,
                 bits_per_second = 0.0,
                 frames_per_second = 0.0):
        self.do_quit = False
        rows, cols, channels = cv_img.shape
        if rows == 0 and cols == 0:
            self.do_quit = True
        self.cv_img = cv_img
        self.exposure_secs = exposure_secs
        self.analog_gain = analog_gain
        self.digital_gain = digital_gain
        self.awb_red_gain = awb_red_gain
        self.awb_blue_gain = awb_blue_gain
        self.y = y
        self.u = u
        self.v = v
        self.udp_connection_status = udp_connection_status
        self.bits_per_second = bits_per_second
        self.frames_per_second = frames_per_second

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

def connect_to_server(ip_addr, port):
    connected = False
    ip_port = ip_addr + ":" + port
    while not connected:
        try:
            stream = urllib.urlopen('http://' + ip_port + '/?action=stream')
            connected = True
        except IOError as e:
            print("can't urlopen " + ip_port + " " + str(e))
    return stream

def draw_crosshairs(img):
    LEN = 3  # length in pixels of each component of crosshairs mark
    COLOR = (0, 255, 255)
    rows, cols, channels = img.shape
    center_x = cols / 2
    center_y = rows / 2
    cv2.line(img, (center_x, center_y - 2 * LEN), (center_x, center_y - LEN), COLOR)
    cv2.line(img, (center_x, center_y + 2 * LEN), (center_x, center_y + LEN), COLOR)
    cv2.line(img, (center_x - 2 * LEN, center_y), (center_x - LEN, center_y), COLOR)
    cv2.line(img, (center_x + 2 * LEN, center_y), (center_x + LEN, center_y), COLOR)


#multiprocessing image processing functions-------------------------------------
def image_capture(ip_addr, queue, do_quit):
    bytes = ''
    byte_count = 0
    start_secs = time.time()
    #ip_addr = "10.6.96.96"
    port = "8080"
    #default_ip_port = "10.6.96.96:8080"
    stream = connect_to_server(ip_addr, port)
    while not do_quit.value:
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
            draw_crosshairs(i)
            frame_secs = time.time() - start_secs
            #if frame_secs > 0.0: print("Kb/sec = %.1f   frames/sec = %.1f" % (byte_count / frame_secs / 1000.0 * 8, 1.0 / frame_secs))
            #print("exp= %u  gains: alog %.3f dig %.3f red %.3f blue %.3f" % (exposure, analog_gain, digital_gain, awb_red_gain, awb_blue_gain))
            #print("yuv= %u %u %u" % (y, u, v))
            frames_per_second = 0.0
            bits_per_second = 0.0
            if frame_secs > 0:
                bits_per_second = byte_count / frame_secs / 1000.0 * 8
                frames_per_second = 1.0 / frame_secs
            start_secs = time.time()
            byte_count = 0
            udp_connection_status = 0
            queue.put(Image_Capture_Queue_Entry(i, exposure/1000.0, analog_gain, digital_gain, awb_red_gain,
                                                awb_blue_gain, y, u, v, udp_connection_status, bits_per_second,
                                                frames_per_second))
    null_image = np.zeros((0, 0, 3), np.uint8)
    queue.put(Image_Capture_Queue_Entry(null_image))

class Quitter():
    def __init__(self):
        self.do_quit = multiprocessing.Value('d',0)

    def quit(self):
        self.do_quit.value = 1

if __name__ == '__main__':
   queue = multiprocessing.Queue()
   print 'queue initialized...'
   root = tk.Tk()
   root.wm_title("dash696")
   quitter = Quitter()
   root.protocol("WM_DELETE_WINDOW", quitter.quit) # quit if window is deleted
   SERVER_IP_ADDR = "10.6.96.96"
   dash_696 = Dash_696(SERVER_IP_ADDR, queue)
   p = multiprocessing.Process(target=image_capture, args=(SERVER_IP_ADDR, queue, quitter.do_quit))
   p.start()
   print 'image capture process has started...'

   # setup the update callback

   root.mainloop()
   print 'mainloop exit'
   #p.terminate()
   p.join()
   root.destroy()
   print 'image capture process exit'

