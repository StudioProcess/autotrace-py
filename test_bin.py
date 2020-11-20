'''Tests to use autotrace binary'''

import subprocess as _subprocess
from PIL import Image
import cairosvg
import os.path

bin_path = './lib/autotrace.app/Contents/MacOS/autotrace'

def trace(img_path, *extra_args):
    '''Run autotrace on an image
    img_path: file path to image
    *extra_args: extra args passed to autotrace
    Returns: SVG bytestring.
    '''
    img = Image.open(img_path)
    tmp_path = 'img/temp.ppm'
    img.save(tmp_path, 'ppm') # Convert input image to PPM (Portable Pixmap) format
    
    args = [ bin_path, '-output-format', 'svg', '-input-format', 'ppm', *extra_args, tmp_path ]
    res = _subprocess.run(args, capture_output=True)
    print(f'autotrace exit code: {res.returncode}')
    return res.stdout


def test_trace(img_path, bg_color='ffffff'):
    '''Trace and render back to PNG for verification'''
    svg_data = trace(img_path, '-background-color', 'bg_color', '-centerline')
    # print(svg_data[0:100])
    root, _ = os.path.splitext( os.path.basename(img_path) )
    dest = 'traced/' + root
    with open(dest+'.svg', 'wb') as f: f.write(svg_data)
    png_data = cairosvg.svg2png(bytestring=svg_data, write_to=dest+'.png', scale=10)

test_trace('img/test/triangle_1px.png')
test_trace('img/test/triangle_2px.png')
