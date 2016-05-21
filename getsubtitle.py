#!/usr/bin/python
import sys
import os
import hashlib
import urllib

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
    url = "http://api.thesubdb.com/"
    action = "?action=download&language=pt&hash="
    subtitle = urllib.URLopener()
    subtitle.addheader('user-agent','SubDB/1.0 (getsubtitle.py/0.1; http://github.com/emsilva)')
    subtitle_name = rename_to_srt(filename)
    subtitle.retrieve(url + action + video_hash, subtitle_name)


def main(argv):
    MOVIE_EXTENSIONS = ['mp4','mkv']
    if len(argv) == 1:
        print "Not enough arguments"
        return
    else:
        for filename in argv[1:]:
            if os.path.exists(filename):
                if filename.endswith(tuple(MOVIE_EXTENSIONS)):
                    download_subtitle(filename)
                else:
                    print filename + " is not a movie file."
            else:
                print "File " + filename + " does not exist!"

if __name__ == "__main__":
    main(sys.argv)
