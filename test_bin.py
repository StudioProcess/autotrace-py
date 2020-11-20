import subprocess as _subprocess
from PIL import Image
import cairosvg
import os.path

bin_path = './lib/autotrace.app/Contents/MacOS/autotrace'

def trace(img_path, *extra_args):
    img = Image.open(img_path)
    tmp_path = 'img/temp.ppm'
    img.save(tmp_path, 'ppm')
    
    args = [ bin_path, '-output-format', 'svg', '-input-format', 'ppm', *extra_args, tmp_path ]
    res = _subprocess.run(args, capture_output=True)
    print(f'exit code: {res.returncode}')
    return res.stdout


def test_trace(img_path, bg_color='ffffff', size=1000):
    svg_data = trace(img_path, '-background-color', 'bg_color', '-centerline')
    # print(svg_data[0:100])
    root, _ = os.path.splitext( os.path.basename(img_path) )
    dest = 'traced/' + root + '.png'
    png_data = cairosvg.svg2png(bytestring=svg_data, write_to=dest, scale=10)

test_trace('img/test/triangle_1px.png')
# test_trace('img/test/triangle_2px.png')