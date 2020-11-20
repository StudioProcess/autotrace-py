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
        return f'({self.x},{self.y},{self.z})'

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

at.at_fitting_opts_new.argtype = []
at.at_fitting_opts_new.restype = ctypes.POINTER(at_fitting_opts)

at.at_bitmap_new.argtype = [ctypes.c_ushort, ctypes.c_ushort, ctypes.c_uint]
at.at_bitmap_new.restype = ctypes.POINTER(at_bitmap)

# at.at_bitmap_read.restype = ctypes.POINTER(at_bitmap)
# at.at_bitmap_copy.restype = ctypes.POINTER(at_bitmap)

at.at_input_get_handler.argtype = [ctypes.c_char_p]
at.at_input_get_handler.restype = ctypes.c_void_p

at.at_input_get_handler_by_suffix.argtype = [ctypes.c_char_p]
at.at_input_get_handler_by_suffix.restype = ctypes.c_void_p

at.at_bitmap_get_width.argtype = [ctypes.POINTER(at_bitmap)]
at.at_bitmap_get_width.restype = ctypes.c_ushort

at.at_bitmap_get_height.argtype = [ctypes.POINTER(at_bitmap)]
at.at_bitmap_get_height.restype = ctypes.c_ushort

at.at_bitmap_get_planes.argtype = [ctypes.POINTER(at_bitmap)]
at.at_bitmap_get_planes.restype = ctypes.c_ushort

at.at_bitmap_get_color.argtype = [ctypes.POINTER(at_bitmap), ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(at_color)]
at.at_bitmap_get_color.restype = None

at.at_splines_new.argtype = [ctypes.POINTER(at_bitmap), ctypes.POINTER(at_fitting_opts)]
at.at_splines_new.restype = ctypes.POINTER(at_splines)

