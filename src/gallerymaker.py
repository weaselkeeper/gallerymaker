#!/usr/bin/env python

""" Create a series of html files that will allow chrome to play all the m4v
files in this directory """

import os
import sys
import argparse

def gallery_subdir(dir):
    """ If there are subdirs, check for m4v files, if so, recurse into them,
    and build gallery """
    vids = os.listdir(dir)
    hasvids = 0
    for _file in vids:
        if _file.endswith('.m4v'):
            hasvids = 1
    if hasvids:
        return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir,name))]
    else:
        return []

def get_options():
    """ command-line options """
    parser = argparse.ArgumentParser(description='Pass cli options')
    parser.add_argument('-d', '--dir', action = "store")
    parser.add_argument('-r', '--recurse', action = "store_true")
    args = parser.parse_args()
    args.usage = 'gallerymaker [options]'
    return args


def get_videolist(moviedir):
    """ Build a list of the video files """
    videolisting = []
    vids = os.listdir(moviedir)
    for _file in vids:
        if _file.endswith('.m4v'):
            videolisting.append(_file)
    return videolisting


def create_html(videofile,moviedir,sep):
    """ make do the html for video thingy"""
    header = """
<!doctype html>
<html>
        <head>
            <title>Movietime!</title>
                <meta charset="utf-8">
        </head>
    <body>
<video controls>
    "<source src="/"""

    footer = """
"/></video>
    </body>
</html>
"""

    # Create the subdir for the movie html pages if it doesn't exist
    # Then write the file to that subdir.  We put the html files in a subdir
    # to avoid clotting up the movie dir. 

    page = moviedir + sep + videofile.split('.')[0] + ".html"
    subdir = os.path.dirname(page)
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    movie_page = open(page, 'w')
    movie_page.write(header)
    movie_page.write(videofile)
    movie_page.write(footer)
    movie_page.close()


def create_index(videolist,moviedir,sep):
    """ create the index.html, pointing at all the individual ones"""
    template_header = """
<!doctype html>
<html>
        <head>
            <title>Movietime!</title>
                <meta charset="utf-8">
        </head>
    <body>
                """
    template_footer = """
    </body>
</html>
"""
    indexfile = os.path.join(moviedir,'index.html')
    index = open(indexfile,'w')
    index.write(template_header)
    if args.recurse:
        for dir in gallery_subdir(moviedir):
            tag = '<a href=' + dir + '/index.html>' + dir + '</a></br>'
            index.write(tag)
    for video in videolist:
        tag = '<a href="page/' + video.split('.')[0] + '.html">' + video + '</a></br>'
        index.write(tag)
        create_html(video,moviedir,sep)
    index.write(template_footer)
    index.close()

if "__main__" in __name__:
    args = get_options()
    if args.dir:
        moviedir = args.dir
    else:
        moviedir = './'
    vids = get_videolist(moviedir)
    create_index(vids,moviedir,'/page/')
    if args.recurse:
        # find any subdirs that contain movie files
        for dir in gallery_subdir(moviedir):
            print dir
            dir = os.path.join(moviedir,dir)
            vids = get_videolist(dir)
            create_index(vids,dir,'/')
