'''Interactive testing autotrace binary with matplotlib GUI'''

# Results:
# works badly with regular forms (ie triangle )
# works quite well with real GAN outputs (despeckle_level way up, despeckle_tightness way down)
# is very slow: 100-300ms for 320px image, 30-150ms for 128px image

import subprocess as _subprocess
from PIL import Image
import cairosvg
import os.path
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider
import io
import time
# import numpy as np

bin_path = './lib/autotrace.app/Contents/MacOS/autotrace'
image_path = 'img/test/triangle_1px.png'
# image_path = 'img/pre1/5660_5_2.tga'
svg_render_scale = 2

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

def trace(img_path, *extra_args):
    '''Run autotrace on an image
    img_path: file path to image
    *extra_args: extra args passed to autotrace
    Returns: SVG bytestring.
    '''
    img = Image.open(img_path)
    tmp_path = 'img/temp.ppm'
    img.save(tmp_path, 'ppm') # Convert input image to PPM (Portable Pixmap) format
    
    extra_args = map(str, extra_args)
    args = [ bin_path, '-output-format', 'svg', '-input-format', 'ppm', *extra_args, tmp_path ]
    timer2.start()
    res = _subprocess.run(args, capture_output=True)
    timer2.stop()
    print(f'autotrace exit code: {res.returncode}')
    print(f'autotrace process: {timer2.last*1000:.1f}')
    return res.stdout


def test_trace(img_path, bg_color='ffffff'):
    '''Trace and show results'''
    img = Image.open(img_path)
    d1.clear()
    d1.imshow(img)
    timer.start()
    
    args = []
    for c in controls:
        args.append( '-' + c.label.get_text() )
        args.append( c.val )
    
    svg_data = trace(img_path, '-background-color', 'bg_color', '-centerline', *args)
    timer.stop()
    print(f'autotrace total: {timer.last*1000:.1f}')
    timer.start()
    png_data = cairosvg.svg2png(bytestring=svg_data, scale=svg_render_scale)
    timer.stop()
    print(f'render svg2png: {timer.last*1000:.1f}')
    out = Image.open(io.BytesIO(png_data))
    d2.clear()
    d2.imshow(out)

def update(val=None):
    test_trace(image_path)
    print()

timer = Timer()
timer2 = Timer()

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 1)
dis = gs[0].subgridspec(1,2)  # display area
d1 = fig.add_subplot(dis[0])
d2 = fig.add_subplot(dis[1])
NUM_CONTROLS = 12
gui = gs[1].subgridspec(NUM_CONTROLS, 1) # gui 
g = []
for i in range(NUM_CONTROLS):
    g.append( fig.add_subplot(gui[i]) )

controls = [
    Slider( g[0], 'color-count', 0, 255, 0, valstep=1),
    Slider( g[1], 'corner-always-threshold', 0, 360, 60, valstep=1 ),
    Slider( g[2], 'corner-surround', 0, 16, 4, valstep=1 ),
    Slider( g[3], 'corner-threshold', 0, 360, 100, valstep=1 ),
    Slider( g[4], 'despeckle-level', 0, 20, 0, valstep=1 ),
    Slider( g[5], 'despeckle-tightness', 0.0, 8.0, 2, valstep=0.1 ),
    Slider( g[6], 'error-threshold', 0.0, 10.0, 2.0, valstep=0.1 ),
    Slider( g[7], 'filter-iterations', 0.0, 10.0, 4, valstep=1 ),
    Slider( g[8], 'line-reversion-threshold', 0.01, 1, 0.01, valstep=0.01 ),
    Slider( g[9], 'line-threshold', 1, 10, 1, valstep=0.1 ),
    Slider( g[10], 'noise-removal', 0.0, 1.0, 0.99, valstep=0.01 ),
    Slider( g[11], 'width-weight-factor', 0.0, 10.0, 1.0, valstep=0.1 ),
    
]
for c in controls: c.on_changed(update)

update()

plt.show()
