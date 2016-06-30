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

import wx
import threading
import os
import time
import mainwindow

class LED(wx.Control):
    def __init__(self, parent, id=-1, colors=[wx.Colour(175, 175, 175), wx.Colour(10, 220, 10), wx.Colour(220, 10, 00)],
                 pos=(-1,-1), style=wx.NO_BORDER):
        size = (80, 17)
        wx.Control.__init__(self, parent, id, pos, size, style)
        self.MinSize = size
        
        self._colors = colors
        self._state = [-1, -1, -1, -1]
        self.bmp = [1,1,1,1]
        self.SetState(0, 0)
        self.SetState(1, 0)
        self.SetState(2, 0)
        self.SetState(3, 0)        
        self.Bind(wx.EVT_PAINT, self.OnPaint, self)
                
    def SetState(self, index, value):
        if index < 0:
            raise ValueError, 'Cannot have a negative index.'
        elif value >= len(self._state):
            raise IndexError, 'There is no LED with index %d.' % value
        
        if value < 0:
            raise ValueError, 'Cannot have a negative state value.'
        elif value >= len(self._colors):
            raise IndexError, 'There is no state with an index of %d.' % value
        elif value == self._state[index]:
            return
        
        self._state[index] = value
        base_color = self._colors[value]
        light_color = change_intensity(base_color, 1.15)
        shadow_color = change_intensity(base_color, 1.07)
        highlight_color = change_intensity(base_color, 1.25)
        
        ascii_led = '''
        000000-----000000      
        0000---------0000
        000-----------000
        00-----XXX----=00
        0----XX**XXX-===0
        0---X***XXXXX===0
        ----X**XXXXXX====
        ---X**XXXXXXXX===
        ---XXXXXXXXXXX===
        ---XXXXXXXXXXX===
        ----XXXXXXXXX====
        0---XXXXXXXXX===0
        0---=XXXXXXX====0
        00=====XXX=====00
        000===========000
        0000=========0000
        000000=====000000
        '''.strip()
        
        xpm = ['17 17 5 1', # width height ncolors chars_per_pixel
               '0 c None', 
               'X c %s' % base_color.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii'),
               '- c %s' % light_color.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii'),
               '= c %s' % shadow_color.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii'),
               '* c %s' % highlight_color.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii')]
        
        xpm += [s.strip() for s in ascii_led.splitlines()]
        
        self.bmp[index] = wx.BitmapFromXPMData(xpm)
        
        self.Refresh()
        
    def GetState(self):
        return self._state
    
    State = property(GetState, SetState)
    
    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp[0], 0, 0, True)
        dc.DrawBitmap(self.bmp[1], 20, 0, True)
        dc.DrawBitmap(self.bmp[2], 40, 0, True)
        dc.DrawBitmap(self.bmp[3], 60, 0, True)
        
def change_intensity(color, fac):
    rgb = [color.Red(), color.Green(), color.Blue()]
    for i, intensity in enumerate(rgb):
        rgb[i] = min(int(round(intensity*fac, 0)), 255)
        
    return wx.Colour(*rgb)

class LedChangeEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, index=None, value=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self.index = index
        self.value = value

class LedThread(threading.Thread):
    def __init__(self, path, parent):
        super(LedThread, self).__init__()
        self._parent = parent
        self.path = path
        self.stop = False
        self.BUFFER_SIZE = 1024
        self.daemon = True
            
    def _stop(self):
        self.stop = True      
            
    def run(self):
        print "starting LED thread"
        self.ld_pipe = os.open(self.path, os.O_RDONLY)
        while(not(self.stop)):
            try:
                time.sleep(0.01)
                ledstr = os.read(self.ld_pipe, self.BUFFER_SIZE)
                print "|||>", ledstr
                for i in range(0, 4):
                    state = int(ledstr[i])
                    print "|||>", state, ledstr
                    evt = LedChangeEvent(mainwindow.myEVT_LED_CHANGE, -1, i, state)
                    wx.PostEvent(self._parent, evt)
                    #print "* %s" % ledstr
                
            except Exception, E:
                print "ld error %r" % E
