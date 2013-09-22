#!/usr/bin/env python

"""

License: GPL V2 See LICENSE file
Author: Jim Richardson
email: weaselkeeper@gmail.com

"""
PROJECTNAME='gallerymaker'

""" Create a series of html files that will allow chrome to play all the m4v
files in this directory """

import os
import sys
import argparse
from ConfigParser import SafeConfigParser
import logging
try:
    from pymongo import Connection
except ImportError as e:
    print 'Failed import of pymmongo, system says %s' % e
    sys.exit(1)


logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%y.%m.%d %H:%M:%S')

console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.WARN)
logging.getLogger(PROJECTNAME).addHandler(console)
log = logging.getLogger(PROJECTNAME)

def run():
    """ Set up defaults, init stuff, do the needful, the usual"""
    log.debug('In run function')
    #Default config location.
    CONFIGFILE = os.path.join('/etc', PROJECTNAME,PROJECTNAME +'.conf')
    if os.path.isfile(CONFIGFILE):
        config = CONFIGFILE
    else:
        log.debug("config unknown, but currently we don't care, as we don't use it")
    vids = get_videolist(moviedir)
    # we assume moviedir is docroot.
    create_index(vids,moviedir,'/page/')
    if args.recurse:
        # find any subdirs that contain movie files
        for dir in gallery_subdir(moviedir):
            filedir = os.path.join(moviedir,dir)
            subdir = os.path.join(moviedir,dir)
            vids = get_videolist(subdir)
            create_index(vids,filedir,'/page/',dir)

def gallery_subdir(dir):
    """ If there are subdirs, check for m4v files, if so, return list of them
    to build gallery with """
    vids = os.listdir(dir)
    hasvids = 0
    for _file in vids:
        # This isn't very efficient at all.  Should stop if one file is correct.
        if _file.endswith('.m4v'):
            hasvids = 1
    if hasvids:
        return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir,name))]
    else:
        return []


def get_videolist(moviedir):
    """ Build a list of the video files """
    videolisting = []
    vids = os.listdir(moviedir)
    for _file in vids:
        if _file.endswith('.m4v'):
            videolisting.append(_file)
    return videolisting


def create_movie_html(videofile,moviedir,sep,docroot_subdir):
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

    movie_index_page = moviedir + sep + videofile.split('.')[0] + ".html"
    subdir = os.path.dirname(movie_index_page)
    log.debug('tracking some moves %s %s %s' % (movie_index_page, videofile,
              subdir))
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    movie_page = open(movie_index_page, 'w')
    movie_page.write(header)
    moviefile_loc = os.path.join(docroot_subdir, videofile)
    movie_page.write(moviefile_loc)
    log.debug( 'moviefile location relative to docroot  %s' % moviefile_loc)
    movie_page.write(footer)
    movie_page.close()


def create_index(videolist,moviedir,sep,docroot_subdir='/'):
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
        create_movie_html(video,moviedir,sep,docroot_subdir)
    index.write(template_footer)
    index.close()

if "__main__" in __name__:

    """ command-line options """
    parser = argparse.ArgumentParser(description='Pass cli options')
    parser.add_argument('-c', '--config', action = "store",
        help='Specify a path to an alternate config file')
    parser.add_argument('-d', '--dir', action = "store")
    parser.add_argument('-r', '--recurse', action = "store_true")
    parser.add_argument('-D', '--debug', action = 'store_true')
    args = parser.parse_args()
    args.usage = 'gallerymaker [options]'

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARN)
    if args.dir:
        moviedir = args.dir
    else:
        moviedir = './'

    """ And go """
    log.debug('off to run()')
    run()

