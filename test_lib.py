'''Initial tests to use autotrace as library (ctypes)'''

import ctypes
import os.path
import autotrace as at

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

res = at.at_bitmap_new( 640, 480, 3)
print(res.contents.width)
print(res.contents.height)
print(res.contents.np)
at.at_bitmap_free( res )
print()

test_img = os.path.abspath('img/test/blue_f.tga').encode('utf-8')
test_img = b'img/test/blue_f.tga'
print(test_img)
handler = at.at_input_get_handler( test_img )
print(handler)

h2 = at.at_input_get_handler_by_suffix(b'tga')
print(h2)
# res = at.at_bitmap_read(None, test_img) # Segfault
print()



img = at.at_bitmap_new( 4, 8, 3 );
print(img.contents.width)
print(img.contents.height)
print(img.contents.np)
print()

print( at.at_bitmap_get_width(img) )
print( at.at_bitmap_get_height(img) )
print( at.at_bitmap_get_planes(img) )

c = at.at_color()
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


bmp = at.to_at_bitmap('img/test/triangle_2px.png')
opts = at.at_fitting_opts_new()
opts.contents.centerline = 1
splines = at.at_splines_new( bmp, opts, None, None ).contents
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
