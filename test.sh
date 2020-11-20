#!/bin/sh

BIN=lib/autotrace.app/Contents/MacOS/autotrace



# $BIN -centerline img/5660_1.png
# OH[2A][5D]: invalid chunk type

# $BIN -centerline img/5660_1.jpg 
# fatal: Unsupported input format.

# $BIN -centerline -output-file trace01.svg img/trace01.bmp

# $BIN -centerline img/5660_1.tiff
# fatal: Unsupported input format.

# $BIN -centerline -output-file 5660_1.svg img/5660_1.tga

$BIN -centerline -output-file 5660_1_2.svg img/pre1/5660_1_2.tga
$BIN -centerline -output-file 5660_2_2.svg img/pre1/5660_2_2.tga
$BIN -centerline -output-file 5660_3_2.svg img/pre1/5660_3_2.tga
$BIN -centerline -output-file 5660_4_2.svg img/pre1/5660_4_2.tga
$BIN -centerline -output-file 5660_5_2.svg img/pre1/5660_5_2.tga
