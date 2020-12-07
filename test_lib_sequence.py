'''Trace sequence of images with autotrace library'''

import autotrace as at
import time
import cairosvg
import glob
import os
import os.path
from PIL import Image, ImageOps
import shutil
import subprocess

# image_path = 'img/test/triangle_2px.png'
image_glob = 'img_seq/lines1/*.png'
out = 'traced_seq/lines1'

# scale = 4
# level_black = 20
# level_white = 200

video_fps = 1

# total in scale should match total svg+out scale (for side-by-side video comp)
in_video_scale = 1
in_video_pad = 2

svg_render_scale = 2
out_video_scale = 1
out_video_pad = 1




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
        print(f'\npath len={path.length}:')
        for i in range(path.length):
            s = path.data[i] # one spline
            print(s)
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

# tracing options
opts = at.at_fitting_opts_new()
opts.contents.centerline = 1
opts.contents.despeckle_level = 20
opts.contents.despeckle_tightness = 0.1

os.makedirs(out, exist_ok=True)

for image_path in files:
    img = Image.open(image_path)
    img = ImageOps.invert(img)
    bmp = at.to_at_bitmap(img)

    timer.start()
    splines = at.at_splines_new( bmp, opts, None, None )
    d = at_splines_to_path(splines, bmp.contents.height)
    at.at_splines_free(splines)
    t = timer.stop()
    time_total += t
    print(f't = {t*1000:.1f} ms')

    svg = path_to_svg(d, bmp.contents.width, bmp.contents.height)
    root, _ = os.path.splitext( os.path.basename(image_path) )
    outfile = out + '/' + root + '.png'
    cairosvg.svg2png(bytestring=svg.encode('utf-8'), scale=svg_render_scale, write_to=outfile)
    at.at_bitmap_free(bmp)

# create video from PNGs
if shutil.which('ffmpeg') is not None:
    print('\nRendering input video...')
    subprocess.run(['ffmpeg', '-r', str(video_fps), '-pattern_type', 'glob', '-i', f'{image_glob}', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '25', '-movflags', '+faststart', '-preset', 'veryslow', '-vf', f'scale=iw*{in_video_scale}:-1:flags=neighbor,pad=iw*{in_video_pad}:ih*{in_video_pad}:-1:-1:Gray', f'{out}/_in.mp4'])
    
    print('\nRendering output video...')
    subprocess.run(['ffmpeg', '-r', str(video_fps), '-pattern_type', 'glob', '-i', f'{out}/*.png', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '25', '-movflags', '+faststart', '-preset', 'veryslow', '-vf', f'scale=iw*{out_video_scale}:-1:flags=neighbor,pad=iw*{out_video_pad}:ih*{out_video_pad}:-1:-1:Gray', f'{out}/_out.mp4'])
    
    print('\nRendering composite video...')
    subprocess.run(['ffmpeg', '-i', f'{out}/_in.mp4', '-i', f'{out}/_out.mp4', '-filter_complex', '[0:v]pad=iw*2:ih[int];[int][1:v]overlay=W/2:0[vid]', '-map', '[vid]', f'{out}/_comp.mp4'])
else:
    print('Skipping video (ffmpeg not installed)')

print(f'\nt_average = {time_total*1000/len(files):.1f} ms')

at.at_fitting_opts_free(opts)

