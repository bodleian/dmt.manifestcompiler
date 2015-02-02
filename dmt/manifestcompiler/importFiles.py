#!/usr/bin/python

# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
#
# Bodleian Library, BDLSS, Oxford University, 
#
# Author: C T Butcher
# Desc: Command line tool to take folder path of a group of images of type 
# given. From this it will generate a IIIF compliant JSON manifest for viewing 
# via Mirador and a Loris/IIP image server 
#
# Changes:
#
# v.1.0 beta - 26.01.15
#
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************

import os, glob
import argparse

from factory import ManifestFactory

__author__ = 'Calvin Butcher'

parser = argparse.ArgumentParser(
    description='This is a script to read a dir of images and export a IIIF compliant JSON maifest.')

parser.add_argument(
    '-p',
    '--path', 
    help='Path of image files',
    required=True)

parser.add_argument(
    '-t',
    '--imgtype',
    help='Types of files (e.g. tif, jpg, jp2, bmp)', 
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


class import_files_export_iiif_json:

# *********************************************************************
    def __init__(self, args):
        self.path = args.path
        self.fileType = args.imgtype
        self.baseimguri = args.baseimguri
        self.basemetadatauri = args.basemetadatauri
        self.width = args.width
        self.height = args.height

# *********************************************************************     
    def load_filenames_into_list (self):
        """load filenames into list"""
        fileList = glob.glob(self.path + '/*.' + self.fileType)

        return fileList

# *********************************************************************     
    def create_manifest (self, imgfiles):
        """create manifest"""
        # to be set in sysargs or via imagemagick
        imageWidth = int(self.width)
        imageHeight = int(self.height)
        identifier = "test file import"

        # setup factory
        factory = ManifestFactory() 
        factory.set_base_metadata_uri("http://www.example.org/metadata/")
        factory.set_base_image_uri("http://www.example.org/iiif/")
        factory.set_iiif_image_info(version="2.0", lvl="2")

        # setup manifest
        mf = factory.manifest(label="Manifest")
        mf.viewingHint = "paged"
        mf.set_metadata({"test label":"test value", "next label":"next value"})
        mf.attribution = "Provided by Bodleian Library, Oxford, using ManifestFactory code from the Houghton Library, Harvard University"
        mf.viewingHint = "paged"
        mf.description = "Description of Manuscript Goes Here"

        seq = mf.sequence() 

        # loop through images in path
        for img in imgfiles:

            # get path, full image name and extension
            imgPath, imgFullName = os.path.split(img)
            imgName, imgExt = os.path.splitext(imgFullName)

            # Mostly identity will come from incrementing number (f1r, f1v,...)
            # or the image's identity

            cvs = seq.canvas(ident="c%s" % imgName, label="Canvas %s" % imgName)  
            cvs.set_hw(imageWidth, imageHeight)
            anno = cvs.annotation() 
            al = cvs.annotationList("foo") 

            # for demo purposes adds choices
            img = factory.image(imgFullName, iiif=True)
            img2 = factory.image(imgName+'b'+imgExt, iiif=True)
            chc = anno.choice(img, [img2])

        json = mf.toString(compact=False)

        # write to text file
        text_file = open(identifier.replace(" ", "") + ".json", "w")
        text_file.write(json)
        text_file.close()

        return json

# ********************************************************************* 
    def execute (self):
        """load files into dict and run manifest factory"""

        imgfiles = self.load_filenames_into_list()
        json = self.create_manifest(imgfiles)

        return json

# ********************************************************************* 
if __name__ == '__main__':
    
    manifest = import_files_export_iiif_json(args).execute()

    print manifest

