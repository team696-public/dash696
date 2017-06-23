import time
import multiprocessing
import Tkinter as tk
import cv2
import urllib
import numpy as np
import struct
import PIL.Image
import PIL.ImageTk

#tkinter GUI functions----------------------------------------------------------
def quit_(root, process):
   process.join()
   root.destroy()

def update_image(image_label, queue):
   frame = queue.get()
   im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   a = PIL.Image.fromarray(im)
   b = PIL.ImageTk.PhotoImage(image=a)
   image_label.configure(image=b)
   image_label._image_cache = b  # avoid garbage collection
   root.update()

def update_all(root, image_label, queue):
   update_image(image_label, queue)
   root.after(0, func=lambda: update_all(root, image_label, queue))

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


#multiprocessing image processing functions-------------------------------------
def image_capture(queue):
   #vidFile = cv2.VideoCapture(0)
   #while True:
   #   try:
   #      flag, frame=vidFile.read()
   #      if flag==0:
   #        break
   #      queue.put(frame)
   #      cv2.waitKey(20)
   #   except:
   #      continue
   stream = urllib.urlopen('http://10.0.1.15:8080/?action=stream')
   bytes = ''
   while True:
       bytes += stream.read(1024)
       a = bytes.find('\xff\xd8')
       b = bytes.find('\xff\xd9')
       if a != -1 and b != -1:
           jpg = bytes[a:b + 2]
           cols, rows, rect_list = parse_tif_tags(jpg)
           bytes = bytes[b + 2:]
           i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
           for rect in rect_list:
               cv2.rectangle(i, rect[0], rect[1], (0, 0, 255))

           queue.put(i)


if __name__ == '__main__':
   queue = multiprocessing.Queue()
   print 'queue initialized...'
   root = tk.Tk()
   print 'GUI initialized...'
   image_label = tk.Label(master=root)# label for the video frame
   image_label.pack()
   print 'GUI image label initialized...'
   p = multiprocessing.Process(target=image_capture, args=(queue,))
   p.start()
   print 'image capture process has started...'
   # quit button
   quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root,p))
   quit_button.pack()
   print 'quit button initialized...'
   # setup the update callback
   root.after(0, func=lambda: update_all(root, image_label, queue))
   #print 'root.after was called...'
   root.mainloop()
   print 'mainloop exit'
   p.join()
   print 'image capture process exit'

