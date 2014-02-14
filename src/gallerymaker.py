#!/usr/bin/env python

"""

License: GPL V2 See LICENSE file
Author: Jim Richardson
email: weaselkeeper@gmail.com

"""
PROJECTNAME = 'gallerymaker'

# Create a series of html files that will allow chrome to play all the m4v
# files in this directory

import os
import sys
import argparse
import logging

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
    vids = get_videolist(moviedir)
    # we assume moviedir is docroot.
    log.debug('Creating top level index with %s, %s ', vids, moviedir)
    create_index(vids, moviedir)
    if args.recurse:
        # find any subdirs that contain movie files
        for _dir in gallery_subdir(moviedir):
            filedir = os.path.join(moviedir, _dir)
            vids = get_videolist(filedir)
            log.debug(' in run(), dealing with variables %s %s %s',
                    filedir, vids, _dir)
            create_index(vids, filedir, _dir)
    log.debug('leaving run()')

def gallery_subdir(_dir):
    """ If there are subdirs, check for m4v files, if so, return list of them
    to build gallery with """
    log.debug('in gallery_subdir()')
    vids = os.listdir(_dir)
    hasvids = 0
    for _file in vids:
        # Stop if one file is correct.
        if _file.endswith('.m4v'):
            hasvids = 1
            break
    if hasvids:
        if args.debug:
            for name in os.listdir(_dir):
                log.debug('found %s in %s ', name, _dir)
        return [name for name in os.listdir(_dir)
            if os.path.isdir(os.path.join(_dir, name))]
    else:
        log.debug('leaving gallery_subdir()')
        return []
    log.debug('leaving gallery_subdir(), apparantly, this is not a subdir')


def get_videolist(_moviedir):
    """ Build a list of the video files """
    log.debug('in get_videolist()')
    videolisting = []
    vids = os.listdir(_moviedir)
    for _file in vids:
        if _file.endswith('.m4v'):
            videolisting.append(_file)
    log.debug('leaving get_videolist()')
    return videolisting


def create_movie_html(videofile, subdir=''):
    """ make do the html for video thingy"""
    log.debug('in create_movie_html()')
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

    # Write the index file for a movie to the topdir

    movie_index_page = moviedir + videofile.split('.')[0] + ".html"
    log.debug('tracking some movies %s %s ', movie_index_page, videofile)
    movie_page = open(movie_index_page, 'w')
    if args.dryrun:
        log.debug('writing header %s', header)
    else:
        movie_page.write(header)

    moviefile_loc = os.path.join(subdir, videofile)
    if args.dryrun:
        log.debug('writing moviepage %s', moviefile_loc)
    else:
        movie_page.write(moviefile_loc)

    log.debug('moviefile location relative to docroot  %s', moviefile_loc)

    if args.dryrun:
        log.debug('writing moviepage %s', moviefile_loc)
    else:
        movie_page.write(footer)
    movie_page.close()
    log.debug('leaving create_movie_html()')


def create_index(videolist, _moviedir, subdir=''):
    """ create the index.html, pointing at all the individual ones"""
    log.debug('entering create_index()')
    template_header = """
<!doctype html>
<html>
        <head>
            <title>Movietime Index!</title>
                <meta charset="utf-8">
        </head>
    <body>
                """
    template_footer = """
    </body>
</html>
"""
    indexfile = os.path.join(_moviedir, 'index.html')
    if args.dryrun:
        log.debug('writing header %s', template_header)
    else:
        index = open(indexfile, 'w')
        index.write(template_header)
    if args.recurse:
        for _dir in gallery_subdir(_moviedir):
            log.debug('found subdir %s containing 1+ movie files', _dir)
            tag = '<a href=' + _dir + '/index.html>' + _dir + '</a></br>'
            if args.dryrun:
                log.debug('writing tag %s', tag)
            else:
                index.write(tag)
    for video in videolist:
        videoname = video.split('.')[0]
        tag = '<a href="/' + videoname + '.html">' +  videoname + '</a></br>'
        if args.dryrun:
            log.debug('writing tag %s', tag)
        else:
            index.write(tag)
            index.write('\n')
        create_movie_html(video, subdir)
    if args.dryrun:
        log.debug('writing footer %s', template_footer)
    else:
        index.write(template_footer)
    index.close()
    log.debug('leaving create_index()')

if "__main__" in __name__:

    # some command-line options
    parser = argparse.ArgumentParser(description='Pass cli options')
    parser.add_argument('-c', '--config', action="store",
        help='Specify a path to an alternate config file')
    parser.add_argument('-d', '--dir', action="store")
    parser.add_argument('-r', '--recurse', action="store_true")
    parser.add_argument('-D', '--debug', action='store_true')
    parser.add_argument('-n', '--dryrun', action='store_true')
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

    log.debug('off to run()')
    run()

