#!/usr/bin/env python

""" Create a series of html files that will allow chrome to play all the m4v
files in this directory """

import os
import sys


def get_videolist():
    """ Build a list of the video files """
    videolisting = []
    vids = os.listdir('./')
    for _file in vids:
        if _file.endswith('.m4v'):
            videolisting.append(_file)
    return videolisting


def create_html(videofile):
    """ make do the html for video thingy"""


def create_index(videolist):
    """ create the index.html, pointing at all the individual ones"""

if "__main__" in __name__:
    vids=get_videolist()
    print vids

