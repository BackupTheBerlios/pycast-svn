# Written by Bram Cohen
# see LICENSE.txt for license information

import BitTorrent.download
from threading import Event

def dummychoose(default, size, saveas, dir):
    return saveas

def dummydisplay(dict):
    print dict#str(float(int(dict['fractionDone'] * 1000)) / 10)

def dummyerror(message):
    pass

def download(url, file, maxUploadRate):
    ev = Event()
    def fin(ev = ev):
        ev.set()
    
    params = ['--url', url, '--max_upload_rate', maxUploadRate, '--saveas', file]   
    BitTorrent.download.download(params, dummychoose, dummydisplay, fin, dummyerror, ev, 80)
