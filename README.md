##PyGP

##Setting up

The project comes with the preloaded datasets and destfile

```
sudo pip install virtualenv
virtualenv venv/
cd pygp 
source ../venv/bin/activate

python setup.py install

```

##Installing:

```
   //downloading the dataset

   //for linux kernal > 3.00

   sudo apt-get install -y libbz2-dev zlib1g-dev
   cd /usr/src
   wget http://www.ris.ripe.net/source/bgpdump/libbgpdump-1.4.99.14.tgz
   tar -xf libbgpdump-1.4.99.14.tgz
   cd libbgpdump-1.4.99.14
   ./configure --prefix=/opt/libbgpdump
   make install


  sudo cp bgpdump /usr/local/bin
  cd dataset/
  bgpdump dsets | grep ASPATH > destfile

```

##License:

&copy; 2015 AnantaBalaji email: anantanarayanantce@gmail.com
