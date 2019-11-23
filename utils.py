from __future__ import print_function

import logging
import sys
import os
import subprocess

def initlog(conf):
    logfilename = conf.get('logfilename', 'ui') or "/tmp/thermuilog.txt"
    loglevel = conf.get('loglevel', 'ui') or 2
    loglevel = int(loglevel)
    if loglevel > 5:
        loglevel = 5
    if loglevel < 1:
        loglevel = 1 
    llmap = {1:logging.CRITICAL, 2:logging.ERROR, 3:logging.WARNING,
             4:logging.INFO, 5:logging.DEBUG}
    loglevel = llmap[loglevel] if loglevel in llmap else logging.WARNING
    logging.basicConfig(filename=logfilename, level=loglevel,
                        format='%(asctime)s - %(name)s:%(lineno)d: %(message)s')
