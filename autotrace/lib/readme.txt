Autotrace binaries/version used:

Darwin:
https://github.com/autotrace/autotrace/releases/tag/travis-20200219.65

Linux:
Since the above broke starting from Ubuntu 22.04, built from source https://github.com/autotrace/autotrace/commit/9386166585f6466f7ef09546e3edd1fab4bb5882


Fresh Ubunutu 24.04 VM (running on Pop!_OS 22.04):
```
#sudo snap remove --purge multipass
sudo snap install multipass

multipass launch --name autotrace-build --cpus 4 --memory 8G --disk 8G --mount $HOME:/home/ubuntu/host-home 24.04

multipass shell autotrace-build

git clone https://github.com/autotrace/autotrace.git; cd autotrace; git reset --hard 9386166

sudo apt install -y build-essential 
sudo apt install -y autotools-dev autopoint libtool intltool
sudo apt install -y libpng-dev libexif-dev libtiff5-dev libjpeg-dev libxml2-dev libbz2-dev libpstoedit-dev libmagickcore-dev libfreetype6-dev

./autogen.sh
./configure --prefix=/usr --without-pstoedit
make

# copy necessary libs
mkdir -p libs
cp .libs/libautotrace.so libs
cp /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0 libs
cp /usr/lib/x86_64-linux-gnu/libMagickCore-6.Q16.so.7 libs
cp /usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0 libs

# copy to host
mkdir -p ~/host-home/autotrace-libs
cp libs/* ~/host-home/autotrace-libs

exit
cd $HOME/autotrace-libs
```