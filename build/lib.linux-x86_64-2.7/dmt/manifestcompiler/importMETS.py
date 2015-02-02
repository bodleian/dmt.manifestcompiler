#!/usr/bin/python

# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
#
# Bodleian Library, BDLSS, Oxford University, 
#
# Author: C T Butcher
# Desc: Command line tool to take a METS XML file.
# From this it will generate a IIIF compliant JSON manifest for viewing 
# via Mirador and a Loris/IIP image server 
#
# Changes:
#
# v.1.0 beta - 28.01.15
#
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************

import os, sys
import argparse
from lxml import etree
import json as json

from factory import ManifestFactory

__author__ = 'Calvin Butcher'

parser = argparse.ArgumentParser(
    description='This is a script to import a METS XML file and export a IIIF compliant JSON maifest.')

parser.add_argument(
    '-p',
    '--path', 
    help='Path and name of METS XML file',
    required=True)

parser.add_argument(
    '-i',
    '--baseimguri', 
    help='Base image URI, e.g. http://iiif-dev.bodleian.ox.ac.uk/loris/', 
    required=True)

parser.add_argument(
    '-m',
    '--basemetadatauri', 
    help='Base metadata URI, e.g. http://iiif-dev.bodleian.ox.ac.uk/iiif/metadata/', 
    required=True)

parser.add_argument(
    '-ht',
    '--height', 
    help='Image height required', 
    required=True)

parser.add_argument(
    '-wt',
    '--width', 
    help='Image width required', 
    required=True)

args = parser.parse_args()


class import_mets_export_iiif_json:

# *********************************************************************
    def __init__(self, args):
        self.path = args.path
        self.baseimguri = args.baseimguri
        self.basemetadatauri = args.basemetadatauri
        self.width = args.width
        self.height = args.height

# *********************************************************************     
    def create_manifest (self):
        """create manifest"""
        # to be set in sysargs or via imagemagick
        imageWidth = int(self.width)
        imageHeight = int(self.height)
        identifier = "test"

        fh = file(self.path)
        data = fh.read()
        fh.close()
        dom = etree.XML(data)
        metsNS = 'http://www.loc.gov/METS/'
        modsNS = 'http://www.loc.gov/mods/v3'
        xlinkNS = 'http://www.w3.org/1999/xlink'
        ALLNS = {'mets':metsNS, 'mods':modsNS, 'xlink':xlinkNS}

        # Extract basic info
        identifier = dom.xpath('/mets:mets/mets:dmdSec/mets:mdWrap[@MDTYPE="MODS"]/mets:xmlData/mods:mods/mods:recordInfo/mods:recordIdentifier/text()', namespaces=ALLNS)[0]
        mflabel = dom.xpath('/mets:mets/mets:structMap[@TYPE="LOGICAL"]/mets:div[@TYPE="manuscript"]/@LABEL', namespaces=ALLNS)[0]
        manifestType = 'sc:Manifest'

        # Extract image info
        images = dom.xpath('/mets:mets/mets:fileSec/mets:fileGrp/mets:file[@MIMETYPE="image/jpeg"]', namespaces=ALLNS)
        struct = dom.xpath('/mets:mets/mets:structMap[@TYPE="PHYSICAL"]/mets:div[@TYPE="physSequence"]/mets:div', namespaces=ALLNS)

        imageHash = {}
        for img in images:
        	imageHash[img.xpath('./@ID', namespaces=ALLNS)[0]] = img.xpath('./mets:FLocat/@xlink:href', namespaces = ALLNS)[0]

        # Configure the factory
        fac = ManifestFactory()
        fac.set_base_metadata_uri(self.baseimguri)
        fac.set_base_image_uri(self.basemetadatauri + identifier + '/')
        fac.set_iiif_image_conformance(1.1, 1)

        # Build the Manifest
        mf = fac.manifest(ident="manifest", label=mflabel)
        mf.attribution = "Provided by the Bodleian Library, Oxford University"
        mf.viewingHint = "paged" if manifestType == "PAGEDOBJECT" else "individuals"
        mf.description = "Description of Manuscript Goes Here"

        # And walk through the pages
        seq = mf.sequence(ident="normal", label="Normal Order")
        for st in struct:
        	# Find label, and image ID
            label = st.xpath('./@ORDERLABEL', namespaces=ALLNS)[0]
            image = imageHash[st.xpath('./mets:fptr[1]/@FILEID', namespaces=ALLNS)[0]]

            # Build the Canvas
            cvs = seq.canvas(ident="c%s" % image,label=label)
            cvs.set_hw(imageHeight, imageWidth)

            # Build the Image Annotation
            anno = cvs.annotation(ident="a%s" % image)
           
            img = anno.image(ident="%s" % image, iiif=True)
            img.set_hw(imageHeight, imageWidth)

        # Serialize 
        mfjs = mf.toJSON()
        srlzd = json.dumps(mfjs, sort_keys=True, indent=2)

        # write to textfile  
        text_file = open(mflabel.replace(" ", "") + ".json", "w")
        text_file.write(srlzd)
        text_file.close()

        return srlzd

# ********************************************************************* 
    def execute (self):
        """load files into dict and run manifest factory"""

        json = self.create_manifest()

        return json

# ********************************************************************* 
if __name__ == '__main__':
    
    manifest = import_mets_export_iiif_json(args).execute()

    print manifest
