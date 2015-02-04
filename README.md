[<img src="https://travis-ci.org/bodleian/dmt.manifestcompiler.svg?branch=master">](https://travis-ci.org/bodleian/dmt.manifestcompiler)

Introduction
============

This egg comprises of two command line tools to compile IIIF compliant manifests (it uses Harvard University's ManifestFactory code from https://github.com/IIIF/presentation-api):

First, a command line tool to take folder path of a group of images of type given. From this it will generate a IIIF compliant JSON manifest for viewing via Mirador and a Loris/IIP image server.

e.g ```python importFiles.py -p /home/loris/dev/dmt.factory -t jp2 -i http://iiif-dev.bodleian.ox.ac.uk/loris/ -m http://iiif-dev.bodleian.ox.ac.uk/iiif/metadata/ -ht 500 -wt 500```

Second, a command line tool to take a METS XML file. From this it will generate a IIIF compliant JSON manifest for viewing via Mirador and a Loris/IIP image server

e.g.  ```python importMETS.py -p /home/loris/dev/dmt.factory/mets.xml -i http://iiif-dev.bodleian.ox.ac.uk/loris/ -m http://iiif-dev.bodleian.ox.ac.uk/iiif/metadata/ -ht 500 -wt 500```

These may be called from the command line via ```__main__``` or as an object call.

First, in ```yourFile.py```:

```code
from factory import ManifestFactory
from importFiles import import_images_export_iiif_json
from importMETS import import_mets_export_iiif_json
```

Then, for example, ```manifest = import_mets_export_iiif_json(args).execute()```

or ```manifest = import_files_export_iiif_json(args).execute()```

Installation
============

Create user "bodl-dmt-svc"
----------------------------

```bash
sudo useradd bodl-dmt-svc
sudo passwd bodl-dmt-svc
sudo mkdir -p /home/bodl-dmt-svc/.ssh
cd /home
sudo chown -R bodl-dmt-svc:bodl-dmt-svc bodl-dmt-svc/
sudo chsh -s /bin/bash bodl-dmt-svc
su - bodl-dmt-svc
ssh-keygen -t rsa
```

Copy and paste your key into gitlab by choosing My Profile (the grey person graphic link in the top right hand corner) then Add Public Key.

```bash
cat ~/.ssh/id_rsa.pub
```

Install and configure Git 
-------------------------

```bash
su - <sudo user>
sudo apt-get install git
```
```bash
git config --global user.email "my@address.com"
git config --global user.name "name in quotes"
```

Setup server
------------

```bash
su - <sudo user>
sudo apt-get install $(cat /home/bodl-dmt-svc/sites/bodl-dmt-svc/ubuntu_requirements)
su - bodl-dmt-svc
```

Checkout the buildout
---------------------
```bash
su - bodl-dmt-svc
mkdir -p ~/sites/bodl-dmt-svc
cd ~/sites/bodl-dmt-svc
git clone https://github.com/bodleian/dmt.manifestcompiler.git ./
```

Install Python
--------------

```bash
mkdir -p /home/bodl-dmt-svc/Downloads
```

```bash
su - bodl-dmt-svc
cd ~/Downloads
wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz --no-check-certificate
tar zxfv Python-2.7.6.tgz
cd Python-2.7.6
./configure --prefix=$HOME/python/2.7.6 --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath=/home/bodl-dmt-svc/python/2.7.6/lib"
make
make install
cd ..
wget https://pypi.python.org/packages/source/d/distribute/distribute-0.6.49.tar.gz
tar zxfv distribute-0.6.49.tar.gz
~/python/2.7.6/bin/python distribute-0.6.49/distribute_setup.py
~/python/2.7.6/bin/easy_install pip
~/python/2.7.6/bin/pip install virtualenv
```

Setup the buildout cache
------------------------
```bash
mkdir /home/bodl-dmt-svc/.buildout
cd /home/bodl-dmt-svc/.buildout
mkdir eggs
mkdir downloads
mkdir extends
echo "[buildout]
eggs-directory = /home/bodl-dmt-svc/.buildout/eggs
download-cache = /home/bodl-dmt-svc/.buildout/downloads
extends-cache = /home/bodl-dmt-svc/.buildout/extends" >> ~/.buildout/default.cfg
```

Create a virtualenv and run the buildout
----------------------------------------

```bash
cd ~/sites/bodl-dmt-svc
~/python/2.7.6/bin/virtualenv .
. bin/activate
pip install zc.buildout
pip install distribute
buildout init
buildout -c development.cfg
```

Run Tests
---------

```bash
python src/dmt.manifestcompiler/dmt/manifestcompiler/importFiles.py -p src/dmt.manifestcompiler/dmt/manifestcompiler/test/images/ -t jp2 -i http://example.com/images/ -m http://example.com/meta/ -ht 500 -wt 500

python src/dmt.manifestcompiler/dmt/manifestcompiler/importMETS.py -p src/dmt.manifestcompiler/dmt/manifestcompiler/test/xml/mets.xml -i http://example.com/images/ -m http://example.com/meta/ -ht 500 -wt 500

```