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
------------

to be contd.