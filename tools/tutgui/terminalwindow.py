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

class TerminalWindow(wx.TextCtrl):
    def __init__(self, parent, dut, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 allow_underline=True, allow_bold=True, allow_italic=True):

        self.dut = dut
        #wx.TextCtrl.__init__(self, parent, id, pos, size)
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE)

        self.__font = wx.Font(10, wx.TELETYPE, wx.NORMAL, wx.NORMAL)

        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        #self.SetBackgroundColour(wx.BLACK)

        #self.SetFont(self.__font)

        # create one of the stock (built-in) cursors
        cursor = wx.StockCursor(wx.CURSOR_IBEAM)

        # set the cursor for the window
        self.SetCursor(cursor)

        #self.Bind(wx.EVT_WINDOW_CREATE, self.__terminal)
        wx.CallAfter(self.__terminal, None)
        

    def __terminal(self, evt):
        w, h = self.GetSize()

        #self.__resize(w, h)
        self.Bind(wx.EVT_CHAR, self.__on_char)
        self.Bind(wx.EVT_TEXT_PASTE, self.OnPaste)
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKey)

    def OnKey(self, evt):
        keycode = evt.GetKeyCode()
        # ENTER
        if keycode == 13:
            keycode = 10
        if keycode < 128:
            c = chr(keycode).lower()
            print("onkey %s" % c)            
            self.dut.uart_write(c)
        else:
            print("onkey %i, 0x%08x" % (keycode, keycode))            
        
        #evt.Skip()

    def OnPaste(self, evt):
        if not(wx.TheClipboard.IsOpened()):
            wx.TheClipboard.Open()
             
        if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)): 
            data = wx.TextDataObject() 
            if wx.TheClipboard.GetData(data): 
                text = data.GetText() 
                print len(text)
                self.dut.uart_write(text)
                #for char in text:
                #    self.dut.uart_write(char)
                #    time.sleep(0.1)

#        print "PASTE but nothing happens"

    def __on_char(self, event):
        keycode = event.GetUnicodeKey() or event.GetKeyCode()
        
        print "}}} %d, 0x%04x" % (keycode, keycode)
        
        # On my box arrows with modifiers works ok inside vim when TERM=xterm
        # With TERM=linux inside vim does not work without a map ex:
        # :map <ESC>[1;5C <C-Right>
        #print keycode
        if event.ControlDown() and event.ShiftDown():
            if keycode == 3:  # SHIFT-CTRL-C
                text_selected = self.__text_from_selection()
                self.__clipboard_put(text_selected)

            elif keycode == 22:  # SHIFT-CTRL-V
                text = self.__clipboard_get()
                if text:
                    os.write(self.__io, text.encode('utf-8'))
            event.Skip()
            return

        char = None
        #print keycode
        if keycode == wx.WXK_UP:
            if event.ControlDown():
                char = "\033[1;5A"
            elif event.AltDown():
                char = "\033[1;3A"
            else:
                char = "\033[A"
        elif keycode == wx.WXK_DOWN:
            if event.ControlDown():
                char = "\033[1;5B"
            elif event.AltDown():
                char = "\033[1;3B"
            else:
                char = "\033[B"
        elif keycode == wx.WXK_RIGHT:
            if event.ControlDown():
                char = "\033[1;5C"
            elif event.AltDown():
                char = "\033[1;3C"
            else:
                char = "\033[C"
        elif keycode == wx.WXK_LEFT:
            if event.ControlDown():
                char = "\033[1;5D"
            elif event.AltDown():
                char = "\033[1;3D"
            else:
                char = "\033[D"
        elif keycode == wx.WXK_PAGEUP:
            char = "\033[5~"
        elif keycode == wx.WXK_PAGEDOWN:
            char = "\033[6~"
        elif keycode == wx.WXK_END:
            char = "\033[4~"
        elif keycode == wx.WXK_HOME:
            char = "\033[1~"
        elif keycode == wx.WXK_INSERT:
            char = "\033[2~"
        elif keycode == wx.WXK_DELETE:
            char = "\033[3~"
        elif keycode < 256:
            char = unichr(keycode)

        if char:
            print char
            #os.write(self.__io, char.encode('utf-8'))
            self.dut.uart_write(char)
        #event.Skip()

        #if keycode == wx.WXK_TAB:
        #    return
        #event.Skip()

