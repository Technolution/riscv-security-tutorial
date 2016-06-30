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
import os
import wx
import mainwindow

#tx_queue = Queue()

class TextTxEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, text=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self.text = text

class TxThread(threading.Thread):
    def __init__(self, path, parent):
        super(TxThread, self).__init__()
        self._parent = parent
        self.path = path
        self.stop = False
        self.BUFFER_SIZE = 1024
        self.daemon = True
            
    def _stop(self):
        self.stop = True      
            
    def run(self):
        print "starting TX thread"
        self.tx_pipe = os.open(self.path, os.O_RDONLY)
        while(not(self.stop)):
            try:
                text = os.read(self.tx_pipe, self.BUFFER_SIZE)
                print ".", text
                #self.stream.AppendText(text)
                evt = TextTxEvent(mainwindow.myEVT_TEXT_TX, -1, text)
                wx.PostEvent(self._parent, evt)
                #tx_queue.put(text)
            except Exception, E:
                print "TX error %r" % E
