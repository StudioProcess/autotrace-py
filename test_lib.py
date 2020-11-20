'''Initial tests to use autotrace as library (ctypes)'''

import ctypes
import os.path

lib_path = 'lib/autotrace.app/Contents/Frameworks/libautotrace.dylib'

# load depended-on libs into global namespace
# otherwise loading autotrace will fail with 'Symbol not found'
# https://stackoverflow.com/questions/39239775/python-ctypes-link-multiple-shared-library-with-example-gsl-gslcblas
deps = ['libglib-2.0.0.dylib','libGraphicsMagick.3.dylib', 'libpstoedit.0.dylib', 'libgobject-2.0.0.dylib' ]
for dep in deps:
    ctypes.CDLL(f'{os.path.dirname(lib_path)}/{dep}', mode=ctypes.RTLD_GLOBAL)

# others = ['libffi.6.dylib', 'libfreetype.6.dylib', 'libgmodule-2.0.0.dylib', 'libgthread-2.0.0.dylib', 'libintl.8.dylib', 'liblcms2.2.dylib', 'libltdl.7.dylib', 'libpcre.1.dylib', 'libpng16.16.dylib']
# for dep in others:
#     ctypes.CDLL(f'{os.path.dirname(lib_path)}/{dep}', mode=ctypes.RTLD_GLOBAL)

at = ctypes.cdll.LoadLibrary(lib_path)
print(f'autotrace library opened: {lib_path}')

# https://gitlab.gnome.org/GNOME/glib/-/blob/master/glib/gtypes.h
gfloat = ctypes.c_float # gfloat -> float -> c_float
gushort = ctypes.c_ushort # gushort -> unsigned short -> c_ushort
gboolean = ctypes.c_int # gboolean -> int -> c_int
guint8 = ctypes.c_uint8 # guint8
gchar = ctypes.c_char # gchar -> char -> c_char
gpointer = ctypes.c_void_p # gpointer -> void* -> c_void_p

class at_bitmap(ctypes.Structure):
    _fields_ = [
        ('height', ctypes.c_ushort),
        ('width',  ctypes.c_ushort),
        ('bitmap', ctypes.POINTER(ctypes.c_char)),
        ('np',     ctypes.c_uint)
    ]

class at_coord(ctypes.Structure):
    _fields_ = [
        ('x', gushort),
        ('y', gushort)
    ]
    def __repr__(self):
        return f'({self.x},{self.y})'

class at_real_coord(ctypes.Structure):
    _fields_ = [
        ('x', gfloat),
        ('y', gfloat),
        ('z', gfloat)
    ]
    def __repr__(self):
        return f'({self.x:.1f}, {self.y:.1f}, {self.z:.1f})'

class at_color(ctypes.Structure):
    _fields_ = [
        ('r', guint8),
        ('g', guint8),
        ('b', guint8)
    ]
    def __repr__(self):
        return f'({self.r},{self.g},{self.b})'


at_polynomial_degree = ctypes.c_uint
# enum _at_polynomial_degree {
#   AT_LINEARTYPE = 1,
#   AT_QUADRATICTYPE = 2,
#   AT_CUBICTYPE = 3,
#   AT_PARALLELELLIPSETYPE = 4,
#   AT_ELLIPSETYPE = 5,
#   AT_CIRCLETYPE = 6
#       /* not the real number of points to define a
#          circle but to distinguish between a cubic spline */
# };


# one spline
class at_spline(ctypes.Structure):
    _fields_ = [
        ('v', at_real_coord * 4),
        ('degree', at_polynomial_degree),
        ('linearity', gfloat)
    ]
    def __repr__(self):
        return f'v0={self.v[0]} v1={self.v[1]} v2={self.v[2]} v3={self.v[3]} degree={self.degree} linearity={self.linearity:.2f}'

# one path/outline (multiple connected splines)
class at_spline_list(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.POINTER(at_spline) ),
        ('length', ctypes.c_uint),
        ('clockwise', gboolean),
        ('color', at_color),
        ('open', gboolean)
    ]

# multiple outlines
class at_splines(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.POINTER(at_spline_list)),
        ('length', ctypes.c_uint),
        ('height', ctypes.c_ushort),
        ('width', ctypes.c_ushort),
        ('background_color', ctypes.POINTER(at_color)),
        ('centerline', gboolean),
        ('preserve_width', gboolean),
        ('width_weight_factor', gfloat)
    ]

class at_fitting_opts(ctypes.Structure):
    _fields_ = [
        ('background_color', ctypes.POINTER(at_color)),
        ('charcode', ctypes.c_uint),
        ('color_count', ctypes.c_uint),
        ('corner_always_threshold', gfloat),
        ('corner_surround', ctypes.c_uint),
        ('corner_threshold', gfloat),
        ('error_threshold', gfloat),
        ('filter_iterations', ctypes.c_uint),
        ('line_reversion_threshold', gfloat),
        ('line_threshold', gfloat),
        ('remove_adjacent_corners', gboolean),
        ('tangent_surround', ctypes.c_uint),
        ('despeckle_level', ctypes.c_uint),
        ('despeckle_tightness', gfloat),
        ('noise_removal', gfloat),
        ('centerline', gboolean),
        ('preserve_width', gboolean),
        ('width_weight_factor', gfloat)
    ]

at.at_fitting_opts_new.restype = ctypes.POINTER(at_fitting_opts)

res = at.at_fitting_opts_new()
res = res.contents
print(res)
print( dir(res) )

print( res.background_color )
print( res.charcode )
print( res.color_count )
print( res.corner_always_threshold )
print( res.corner_surround )
print( res.corner_threshold )
print( res.error_threshold )
print( res.filter_iterations )
print( res.line_reversion_threshold )
print( res.line_threshold )
print( res.remove_adjacent_corners )
print( res.tangent_surround )
print( res.despeckle_level )
print( res.despeckle_tightness )
print( res.noise_removal )
print( res.centerline )
print( res.preserve_width )
print( res.width_weight_factor )
print()

# at_input_read_func rfunc = at_input_get_handler(fname);
# bitmap = at_bitmap_read(rfunc, fname, NULL, NULL, NULL);
# at.at_splines_new(bitmap, opts, NULL, NULL);

# pnm, pbm, pgm, ppm, bmp and tga
# pnm: portably anymap
# pbm: portable bitmap [1bit]
# pgm: portable graymap [8/16 bit]
# ppm: portable pixmap [24/48 bit]


# at.at_input_get_handler

at.at_bitmap_read.restype = ctypes.POINTER(at_bitmap)
at.at_bitmap_new.restype = ctypes.POINTER(at_bitmap)
at.at_bitmap_new.copy = ctypes.POINTER(at_bitmap)

at.at_bitmap_new.argtype = [ctypes.c_ushort, ctypes.c_ushort, ctypes.c_uint]

res = at.at_bitmap_new( 640, 480, 3)
print(res.contents.width)
print(res.contents.height)
print(res.contents.np)
at.at_bitmap_free( res )
print()

test_img = os.path.abspath('img/test/blue_f.tga').encode('utf-8')
test_img = b'img/test/blue_f.tga'
print(test_img)
at.at_input_get_handler.argtypes = [ctypes.c_char_p]
handler = at.at_input_get_handler( test_img )
print(handler)

at.at_input_get_handler_by_suffix.argtypes = [ctypes.c_char_p]
h2 = at.at_input_get_handler_by_suffix(b'tga')
print(h2)
# res = at.at_bitmap_read(None, test_img) # Segfault
print()



img = at.at_bitmap_new( 4, 8, 3 );
print(img.contents.width)
print(img.contents.height)
print(img.contents.np)
print()

at.at_bitmap_get_width.argtype = [ctypes.POINTER(at_bitmap)]
at.at_bitmap_get_width.restype = ctypes.c_ushort

at.at_bitmap_get_height.argtype = [ctypes.POINTER(at_bitmap)]
at.at_bitmap_get_height.restype = ctypes.c_ushort

at.at_bitmap_get_planes.argtype = [ctypes.POINTER(at_bitmap)]
at.at_bitmap_get_planes.restype = ctypes.c_ushort

at.at_bitmap_get_color.argtype = [ctypes.POINTER(at_bitmap), ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(at_color)]

print( at.at_bitmap_get_width(img) )
print( at.at_bitmap_get_height(img) )
print( at.at_bitmap_get_planes(img) )

c = at_color()
# c.r = 0
# c.g = 128
# c.b = 255
print(c)

data = img.contents.bitmap
data[0] = 0
data[1] = 128
data[2] = 255

at.at_bitmap_get_color( img, 0, 0, ctypes.pointer(c) )
print(c)


from PIL import Image
import numpy as np
image = Image.open('img/test/blue_f_small.tga')
image = np.asarray(image)
print(image.shape)
image = image.flatten()
print(image.shape)
print(image)
image = image.tolist()
print(image)
print()

# at.at_bitmap_free( res )
# print()

at.at_splines_new.argtype = [ctypes.POINTER(at_bitmap), ctypes.POINTER(at_fitting_opts)]
at.at_splines_new.restype = ctypes.POINTER(at_splines)

# opts = at.at_fitting_opts_new()
# opts.contents.centerline = 1
# bitmap = at.at_bitmap_new( 640, 480, 3 )
# splines = at.at_splines_new( bitmap, opts, None, None ).contents
# print(splines)
# print(splines.data)
# print(splines.length)
# print(splines.width)
# print(splines.height)
# print(splines.background_color)
# print(splines.centerline)
# print(splines.preserve_width)
# print(splines.width_weight_factor)
# print()

def to_at_bitmap(img_path):
    img = Image.open(img_path)
    bmp = at.at_bitmap_new( img.width, img.height, 3 );
    # bitmap is: r00, g00, b00, r10, g10, b10, ...
    img_data = np.asarray(img).flatten()
    bmp_data = bmp.contents.bitmap
    for i, x in enumerate(img_data): bmp_data[i] = int(x)
    return bmp

bmp = to_at_bitmap('img/test/triangle_2px.png')
opts = at.at_fitting_opts_new()
opts.contents.centerline = 1
splines = splines = at.at_splines_new( bmp, opts, None, None ).contents
print(splines)
print(splines.data)
print(splines.length)
print(splines.width)
print(splines.height)
print(splines.background_color)
print(splines.centerline)
print(splines.preserve_width)
print(splines.width_weight_factor)
print()

for i in range(splines.length):
    path = splines.data[i]
    print(f'path {i} ({path.length}) {path.color}')
    for i in range(path.length):
        print(f'    {path.data[i]}')

# paths: 
# * origin is bottom left ie. y+ points up
# * degree 1: v0 and v3 are begin and end. v1 and v2 are ignored in SVG output
# * degree 3: v0 = start point, v1 = first control point, v2 = 2nd control point v3 = end point
