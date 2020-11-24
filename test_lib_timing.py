'''Timing autotrace library'''

# RESULTS:
# 
# inital results (128 x 128):
# 
# unoptimized: 34 ms
# with image in memory: 24 ms
# 
# 
# 128 x 128 px:
# 
# img/test/triangle_1px.png
# default params: 24 ms
# with despeckling: 4 ms
# 
# img/test/triangle_2px.png: 
# default params: 22 ms
# with despeckling: 4 ms
# 
# 
# 320 x 320 px:
# 
# img/pre1/5660_1_2.tga: 
# default params: 74 ms
# with despeckling: 27 ms
# 
# img/pre1/5660_2_2.tga: 
# default params: 102 ms
# w/despeckling: 26 ms
# 
# img/pre1/5660_3_2.tga: 
# default params: 58 ms
# w/despeckling: 25 ms
# 
# img/pre1/5660_4_2.tga: 
# default params: 47 ms
# w/despeckling: 26 ms
# 
# img/pre1/5660_5_2.tga: 
# default params: 75 ms
# w/despeckling: 25 ms


import autotrace as at
import time

# image_path = 'img/test/triangle_1px.png'
image_path = 'img/test/triangle_2px.png'
# image_path = 'img/pre1/5660_3_2.tga'
n = 100

class Timer():
    def __init__(self):
        self.start()
        self.last = 0
    def start(self):
        self.t_start = time.perf_counter()
        return self.start
    def stop(self):
        self.t_stop = time.perf_counter()
        self.last = self.t_stop - self.t_start
        return self.last

timer = Timer()
total = 0

bmp = at.to_at_bitmap(image_path)
opts = at.at_fitting_opts_new()
opts.contents.centerline = 1
opts.contents.despeckle_level = 20
opts.contents.despeckle_tightness = 0.1


for i in range(n):
    timer.start()
    splines = at.at_splines_new( bmp, opts, None, None )
    timer.stop()
    
    len = 0
    for j in range(splines.contents.length):
        path = splines.contents.data[j]
        len += path.length
    at.at_splines_free(splines)
    print(f'n={i}: ({len}) {timer.last*1000:.1f}')
    total += timer.last

print()
print(f'average: {total*1000/n:.1f}')

at.at_fitting_opts_free(opts)
at.at_bitmap_free(bmp)
