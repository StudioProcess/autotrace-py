Autotrace binaries/version used:

Darwin:
https://github.com/autotrace/autotrace/releases/tag/travis-20200219.65

Linux:
Since the above broke on Ubuntu 22.04, built from source https://github.com/autotrace/autotrace/commit/cba2237e379ab82d4c0c5d1ec86f7b69732c162f


Fresh Ubunutu 22.04 VM:
```
sudo snap install multipass
multipass launch --name autotrace-build --cpus 4 --memory 8G --mount $HOME 22.04
multipass exec autotrace-build -- HOST_HOME=$HOME bash

multipass exec -- HOST_HOME=$HOME bash
```

Build:
```
git clone https://github.com/autotrace/autotrace.git
cd autotrace
git reset --hard cba2237

sudo apt install -y libgraphicsmagick1-dev libpng-dev libexiv2-dev libtiff-dev libjpeg-dev libxml2-dev libbz2-dev libfreetype6-dev libpstoedit-dev autoconf automake libtool intltool autopoint
sudo apt install -y build-essential
./autogen.sh
./configure
make
make check
make install
./distribute/distribute.sh

# Output files are written to `distribute/out`; Copy to host machine's home
cp distribute/out/*.deb $HOST_HOME
``` 