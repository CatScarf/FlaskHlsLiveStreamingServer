import os
import queue
import shutil
import threading
import time
from datetime import datetime
from math import ceil

import ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def makedir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

# Draw a frame
def draw_example_image(timestamp, save=False):
    datatime = datetime.fromtimestamp(timestamp)
    image = Image.new(mode = 'RGB', size = (480, 320), color = (96,140,159))
    draw = ImageDraw.Draw(image)
    time_string = str(datatime)
    padding = 150
    xy = (100, (320 - padding * 2) * (timestamp % 1) + padding)
    draw.text(xy, text=time_string, fill=(255, 255, 255))
    if save:
        image.save(f'{time_string}.jpg')
    return image

# Generate an example video
def generate_example_video(start_timestamp, fps=60, duration=10):
    timestamp = start_timestamp
    for i in range(ceil(fps * duration)):
        image = draw_example_image(timestamp)
        tempdir = f'{os.getcwd()}/{start_timestamp}'
        makedir(tempdir)
        image.save(f'{tempdir}/{timestamp}.jpg')
        timestamp += 1 / fps

    video_path = f'{os.getcwd()}/{time.time()}.ts'
    (
        ffmpeg
        .input(f'{start_timestamp}/*.jpg', pattern_type='glob', framerate=fps)
        .output(video_path)
        .run()
    )

    shutil.rmtree(tempdir)
    
    return video_path

# Move the video from the temporary folder to the . /video folder
def save_video(dir, name, video_path):
    # todo
    if not os.path.exists(dir):
        os.makedirs(dir)
        
    shutil.move(video_path, f'{dir}/{name}')

# Delete Video
def delete_video(dir, name):
    os.remove(f'{dir}/{name}')

# Generate m3u8 text
def generate_m3u8(start_idx, video_queue, vq_lock, duration):
    # Add header information
    s = f'#EXTM3U\n'
    s += f'#EXT-X-VERSION:4\n'
    s += f'#EXT-X-TARGETDURATION:{ceil(duration)}\n'
    s += f'#EXT-X-MEDIA-SEQUENCE:{start_idx}\n'
    temp_queue = queue.Queue()
    
    # Add video name
    vq_lock.acquire()
    while video_queue.qsize() > 0:
        name = video_queue.get()
        s += f'#EXTINF:{float(duration)},\n'
        s += f'{name}\n'
        temp_queue.put(name)
        
    while temp_queue.qsize() > 0:
        video_queue.put(temp_queue.get())
    vq_lock.release()
        
    return s

# Continuous generating video sequence and saving
def generate_thread(video_queue, vq_lock, old_queue, stop, fps=60, duration=10, max_cache=10, dir='./video', del_old_second=None):
    start_time = time.time()
    start_idx = 1 # EXT-X-MEDIA-SEQUENCE
    idx = 1  
    while stop.qsize() == 0:
        # Generate video and save it
        # print(f'[generate_thread][{os.getpid()}] idx={idx}, start_idx={start_idx}')
        video_path = generate_example_video(start_time, fps, duration)
        name = f'{idx}.ts'
        idx += 1
        save_video(dir, name, video_path)
        
        # Put the video name into the queue, 
        # and if the queue exceeds the limit, 
        # move the earliest video out of the playlist
        vq_lock.acquire()
        video_queue.put(name)
        if video_queue.qsize() > max_cache:
            start_idx += 1
            file_to_delete = video_queue.get()
            old_queue.put(file_to_delete)
            
            # If the queue of outdated videos exceeds del_old_second, the oldest outdated video will be deleted
            if del_old_second is not None and old_queue.qsize() * duration > del_old_second:
                delete_video(dir, old_queue.get())
        vq_lock.release()
        
        m3u8 = generate_m3u8(start_idx, video_queue, vq_lock, duration)
        with open(f'{dir}/playlist.m3u8', 'w') as f:
            f.write(m3u8)
        
        if duration - (time.time() - start_time) < 0:
            print(f'[error][generate_thread][{os.getpid()}] generate video timeout')
            
        time.sleep(max(0, duration - (time.time() - start_time)))
        start_time += duration
        
# For generate example videos
class M3U8:
    def __init__(self, dir='./video', fps=60, duration=10, max_cache=10, del_dir=False, del_old_second=None):
        self.dir = dir
        self.fps = fps
        self.duration = float(duration)
        self.max_cache = max_cache
        self.del_dir = del_dir
        
        # Generate the video and store it in . /video folder
        self.video_queue = queue.Queue()
        self.vq_lock = threading.Lock()
        self.old_queue = queue.Queue()
        self.stop = queue.Queue()
        self.generate_threading = threading.Thread(
            target=generate_thread, 
            args=(self.video_queue, self.vq_lock, self.old_queue, 
                  self.stop, fps, duration, max_cache, dir, 
                  del_old_second))
        self.generate_threading.start()
        
    def __del__(self):
        self.stop.put('')
        if self.del_dir == True:
            shutil.rmtree(self.dir)
            os.makedirs(self.dir)
        self.generate_threading.join()
    

if __name__ == '__main__':
    # Only for test
    m3u8 = M3U8(duration=1, del_old_second=60)
    input('View folder \"./video\" to see the generated videos, press any key to exit\n')
    del(m3u8)
