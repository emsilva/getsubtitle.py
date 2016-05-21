#!/usr/bin/python
import sys
import os
import hashlib
import urllib

class bc:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'
    SUCCESS = OKGREEN + '[OK] ' + ENDC
    ERROR = FAIL + '[FAIL] ' + ENDC

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def rename_to_srt(filename):
    (prefix, sep, suffix) = filename.rpartition('.')
    new_filename = prefix + '.srt'
    return new_filename

def download_subtitle(filename):
    video_hash = get_hash(filename)
    url = 'http://api.thesubdb.com/'
    action = '?action=download&language=pt&hash='
    subtitle = urllib.URLopener()
    subtitle.addheader('user-agent','SubDB/1.0 (getsubtitle.py/0.1; http://github.com/emsilva)')
    subtitle_name = rename_to_srt(filename)
    colored_subtitle_name = bc.UNDERLINE + subtitle_name + bc.ENDC
    subtitle.retrieve(url + action + video_hash, subtitle_name)
    subtitle.close
    if os.path.exists(subtitle_name):
        print bc.SUCCESS + 'File ' + colored_subtitle_name + ' downloaded successfuly.'

def main(argv):
    MOVIE_EXTENSIONS = ['mp4','mkv']
    if len(argv) == 1:
        print bc.ERROR + 'Not enough arguments'
        return
    else:
        for filename in argv[1:]:
            if os.path.exists(filename):
                if filename.endswith(tuple(MOVIE_EXTENSIONS)):
                    download_subtitle(filename)
                else:
                    print bc.ERROR + 'File ' + bc.UNDERLINE + filename + bc.ENDC + ' is not a movie file.'
            else:
                print bc.ERROR + 'File ' + bc.UNDERLINE + filename + bc.ENDC + ' does not exist!'

if __name__ == '__main__':
    main(sys.argv)
