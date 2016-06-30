#!/usr/bin/python
# -*- coding: utf-8 -*-
# ************************************************************************
#
# (C) COPYRIGHT 2016 TECHNOLUTION BV, GOUDA NL
# | =======          I                   ==          I    =
# |    I             I                    I          I
# |    I   ===   === I ===  I ===   ===   I  I    I ====  I   ===  I ===
# |    I  /   \ I    I/   I I/   I I   I  I  I    I  I    I  I   I I/   I
# |    I  ===== I    I    I I    I I   I  I  I    I  I    I  I   I I    I
# |    I  \     I    I    I I    I I   I  I  I   /I  \    I  I   I I    I
# |    I   ===   === I    I I    I  ===  ===  === I   ==  I   ===  I    I
# |                 +---------------------------------------------------+
# +----+            |  +++++++++++++++++++++++++++++++++++++++++++++++++|
#      |            |             ++++++++++++++++++++++++++++++++++++++|
#      +------------+                          +++++++++++++++++++++++++|
#                                                         ++++++++++++++|
#                                                                  +++++|
#
# ************************************************************************

import threading
import traceback
import sys
import os
import time

rxlock = threading.RLock()

class RxThread(threading.Thread):
    def __init__(self, path, tmp_path):
        super(RxThread, self).__init__()
        self.path = path
        self.tmp_path = tmp_path
        self.stop = False
        self.BUFFER_SIZE = 1024
        self.daemon = True
            
    def _stop(self):
        self.stop = True      
            
    def run(self):
        print "starting RX thread"
        while(not(self.stop)):
            try:
                time.sleep(0.01)
                rxlock.acquire()
                try:
                    if os.path.exists(self.tmp_path) and not os.path.exists(self.path):  
                        os.rename(self.tmp_path, self.path)
                finally:
                    rxlock.release()
            except Exception, E:
                print "RX error %r" % E
                traceback.print_exc(file=sys.stdout)
