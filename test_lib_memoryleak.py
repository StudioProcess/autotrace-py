'''Testing autotroce library use for memory leaks
pip install memory_profiler
pip install matplotlib
mprof run --include-children --interval 10 python test_lib_memoryleak.py
mprof plot
mprof plot --output memory-profile.png
'''

import autotrace as at
import time
import cairosvg
import glob
import os
import os.path
from PIL import Image, ImageOps
import shutil
import subprocess
import sys


RUNTIME_MINS = 180

# image_path = 'img/test/triangle_2px.png'
image_glob = 'img_seq/patch_scale3_large/*.png'

# pre-processing
pre_scale = 2
pre_levels = (0, 0) # percent of range default: (2, 10)
pre_threshold = 20 # percent of range
pre_invert = True
pre_equalize = False
svg_render_scale = 1

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
time_total = 0
time_min = sys.maxsize
time_max = 0
iterations = 0

# * origin is bottom left ie. y+ points up
# * degree 1: v0 and v3 are begin and end. v1 and v2 are ignored in SVG output
# * degree 3: v0 = start point, v1 = first control point, v2 = 2nd control point v3 = end point

def at_splines_to_path(splines, height=128, decimals = -1):
    def coords(at_coord):
        def rnd(n): return ('{:.' + str(decimals) + 'f}').format(n) if decimals >= 0 else n
        return f'{rnd(at_coord.x)} {height - rnd(at_coord.y)}' # flip y coordinate (needs height)
    d = ''
    for j in range(splines.contents.length): # iterate over paths
        path = splines.contents.data[j] # one path (multiple connected splines)
        # print('new path:')
        # print(f'\npath len={path.length}:')
        for i in range(path.length):
            s = path.data[i] # one spline
            # print(s)
            if s.degree == 1:
                if i == 0: d += f'M {coords(s.v[0])} '
                d += f'L {coords(s.v[3])} '
            elif s.degree == 3:
                if i == 0: d += f'M {coords(s.v[0])} '
                d += f'C {coords(s.v[1])} {coords(s.v[2])} {coords(s.v[3])} '
            else:
                print(f'Warning: Unsupported spline, degree={s.degree}')
    d = d.strip()
    return d

def path_to_svg(d, width=128, height=128, style={}):
    style_defaults = {
        'fill': 'none',
        'stroke': 'black',
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': width/1000 * 7,
    }
    if type(d) is str: d = [d]
    paths = ''.join([ f'<path d="{d}" />' for d in d ])
    style_dict = {}
    style_dict.update(style_defaults)
    style_dict.update(style)
    style = ' '.join([ f'{key}:{value};' for key, value in style_dict.items() ])
    bg = '<rect width="100%" height="100%" stroke="none" fill="white" />'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="{style}">{bg} {paths}</svg>'
    return svg


# find input files
files = glob.glob(image_glob)
files.sort()

timer_global = Timer()
while timer_global.stop() / 60 < RUNTIME_MINS:
    # tracing options
    opts = at.at_fitting_opts_new()
    opts.contents.centerline = 1
    opts.contents.despeckle_level = 20
    opts.contents.despeckle_tightness = 0.1

    # os.makedirs(out, exist_ok=True)
    # os.makedirs(f'{out}/in_pre', exist_ok=True)

    for image_path in files:
        img = Image.open(image_path)
        if pre_scale > 1: img = ImageOps.scale(img, pre_scale)
        if pre_levels[0] > 0 or pre_levels[1] > 0: img = ImageOps.autocontrast(img, pre_levels)
        if pre_threshold > 0: img = img.point(lambda i: 0 if i < pre_threshold/100*255 else 255)
        if pre_invert: img = ImageOps.invert(img)
        if pre_equalize: img = ImageOps.equalize(img)
        bmp = at.to_at_bitmap(img, gray=True)
        timer.start()
        splines = at.at_splines_new( bmp, opts, None, None )
        d = at_splines_to_path(splines, bmp.contents.height)
        at.at_splines_free(splines)
        t = timer.stop()
        time_total += t
        # print(f't = {t*1000:.1f} ms')
        if t > time_max: time_max = t
        if t < time_min: time_min = t
        iterations += 1

        svg = path_to_svg(d, bmp.contents.width, bmp.contents.height)
        root, _ = os.path.splitext( os.path.basename(image_path) )
        # img.save(f'{out}/in_pre/{root}.png') # save preprocessed image
        # cairosvg.svg2png(bytestring=svg.encode('utf-8'), scale=svg_render_scale, write_to=f'{out}/{root}.png') # save rendered svg
        cairosvg.svg2png(bytestring=svg.encode('utf-8'), scale=svg_render_scale)
        at.at_bitmap_free(bmp)
    at.at_fitting_opts_free(opts)

    print(f'\nt_min = {time_min*1000:.1f} ms')
    print(f't_max = {time_max*1000:.1f} ms')
    print(f't_average = {time_total*1000/iterations:.1f} ms')
    print(f'RUN TIME {timer_global.stop()/60:.1f} min')

