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
import traceback
import sys
import wx
#import wxterm
#import wx.lib.agw.hypertreelist as wxl
import os
import atexit
import errno
import threading
import time
from Queue import Queue
import subprocess

rxlock = threading.RLock()
tx_queue = Queue()

myEVT_LED_CHANGE = wx.NewEventType()
EVT_LED_CHANGE = wx.PyEventBinder(myEVT_LED_CHANGE, 1)
class LedChangeEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, state=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self.state = state

myEVT_TEXT_TX = wx.NewEventType()
EVT_TEXT_TX = wx.PyEventBinder(myEVT_TEXT_TX, 1)
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
                evt = TextTxEvent(myEVT_TEXT_TX, -1, text)
                wx.PostEvent(self._parent, evt)
                #tx_queue.put(text)
            except Exception, E:
                print "tx error %r" % E
        
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
                #if not os.path.exists(self.tmp_path):
                    #data = q.get()
                    #print "<<< %s" % data
                    #print "--- %s, %s" % (data, type(data))
                    #call("bash", "echo bla > rx_file")
                    #f = open(self.tmp_path, 'w', 0)
                    #f.write(str(data))
                    #f.close()
                    #os.rename(self.tmp_path, self.path)
                    #cmd = "echo %s > %s" % (data, self.path)
                    #cmd = "mv %s %s" % (self.tmp_path, self.path)
                    #os.system(cmd)
                    #time.sleep(1)
            except Exception, E:
                print "rx error %r" % E
                traceback.print_exc(file=sys.stdout)



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
        print "starting TX thread"
        self.ld_pipe = os.open(self.path, os.O_RDONLY)
        while(not(self.stop)):
            try:
                time.sleep(0.01)
                ledstr = os.read(self.ld_pipe, 1024)
                state = 1 if ledstr[0] == '1' else 0
                #print "|||>", state, ledstr
                evt = LedChangeEvent(myEVT_LED_CHANGE, -1, state)
                wx.PostEvent(self._parent, evt)
                #print "* %s" % ledstr
                
            except Exception, E:
                print "ld error %r" % E

class Target(object):
    def __init__(self):
        #self.LED_FIFO_PATH = "ld_pipe"
        
        # our UART consists of a RX and TX path as seen from the target
        self.TX_FIFO_PATH = "../../appl/run/spike/tx_pipe"
        self.RX_FILE_PATH = "../../appl/run/spike/rx_file"
        self.RX_TMP_FILE_PATH = "../../appl/run/spike/_rx_file"
        self.LD_FIFO_PATH = "../../appl/run/spike/ld_pipe"
        self.BUFFER_SIZE = 1024

    def open_pipes(self, stream, parent):
        self.start_threads(stream, parent)
        #self.led_pipe = os.open(self.LED_FIFO_PATH, os.O_RDONLY)
        #self.rx_pipe = os.open(self.RX_FIFO_PATH, os.O_WRONLY)
        #os.write(self.rx_pipe, "aaa")
    
    def start_threads(self, stream, parent):
        self.rx_thread = RxThread(self.RX_FILE_PATH, self.RX_TMP_FILE_PATH)
        self.tx_thread = TxThread(self.TX_FIFO_PATH, parent)
        self.led_thread = LedThread(self.LD_FIFO_PATH, parent);
        self.rx_thread.start()
        self.tx_thread.start()
        self.led_thread.start()
    
    def uart_read(self):
        return os.read(self.tx_pipe, self.BUFFER_SIZE)
        
    def uart_write(self, data):
        print ">>> %s" % data
        rxlock.acquire()
        try:
            rx_file = open(self.RX_TMP_FILE_PATH, 'a+', 0)
            rx_file.write(data)
            rx_file.close()
        finally:
            rxlock.release()
       #os.rename(self.tmp_path, self.path)
        
        #q.put(data)
        #rxlock.acquire()
        #try:
            #rx_file = open(self.RX_TMP_FILE_PATH, 'a+')
            #rx_file.write(data)
            #rx_file.flush()
            #rx_file.close()
        #finally:
            #rxlock.release()




def change_intensity(color, fac):
    rgb = [color.Red(), color.Green(), color.Blue()]
    for i, intensity in enumerate(rgb):
        rgb[i] = min(int(round(intensity*fac, 0)), 255)
        
    return wx.Colour(*rgb)    

class LED(wx.Control):
    def __init__(self, parent, id=-1, colors=[wx.Colour(220, 10, 10), wx.Colour(250, 200, 0), wx.Colour(10, 220, 10)],
                 pos=(-1,-1), style=wx.NO_BORDER):
        size = (17, 17)
        wx.Control.__init__(self, parent, id, pos, size, style)
        self.MinSize = size
        
        self._colors = colors
        self._state = -1
        self.SetState(0)
        self.Bind(wx.EVT_PAINT, self.OnPaint, self)
        
    def SetState(self, i):
        if i < 0:
            raise ValueError, 'Cannot have a negative state value.'
        elif i >= len(self._colors):
            raise IndexError, 'There is no state with an index of %d.' % i
        elif i == self._state:
            return
        
        self._state = i
        base_color = self._colors[i]
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
        
        self.bmp = wx.BitmapFromXPMData(xpm)
        
        self.Refresh()
        
    def GetState(self):
        return self._state
    
    State = property(GetState, SetState)
    
    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0, True)
        
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


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,475), pos=(960,0))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        #self.control.OnChar = self.OnChar
        

        #self.control.Bind(wx.EVT_CHAR, self.OnChar, self)
        statusbar = self.CreateStatusBar() # A StatusBar in the bottom of the window
        self.led = LED(statusbar, pos=(5,3))

        
        self.dut = Target()
        self.term = TerminalWindow(self, self.dut)
        #term.ForkCommand('bash', ['bash'])
        #term.Bind(wxterm.EVT_TERM_CHILD_EXIT, self.OnExit)

        self.dut.open_pipes(self.term, self)
        #s = wx.BoxSizer(wx.VERTICAL)
        #s.Add(self.term, 1, wx.EXPAND, 0)
        #self.SetSizer(s)


        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(EVT_LED_CHANGE, self.OnLedChange)
        self.Bind(EVT_TEXT_TX, self.OnTextTx)
        self.Bind(wx.EVT_TEXT_PASTE, self.OnPaste)



        self.Show(True)
    
    def OnPaste(self, evt):
        print "pasta"
    
    def OnExit(self, event):
        self.GetParent().Close()        
 
    def OnChar(self, event):
        print event
        self.control.append("event" + event)
         
    def OnLedChange(self, event):
        self.led.SetState(event.state)    
        
    def OnTextTx(self, event):
        print "event text: %s" % event.text
        for c in event.text:
            print "--> '%c', %d, 0x%4x" % (c, ord(c), ord(c))
            if ord(c) == 8: # backspace
                print self.term.Value
                #self.term.Value = self.term.Value[:-1]
                self.term.Remove(self.term.GetLastPosition()-1, self.term.GetLastPosition())
            else:
                self.term.AppendText(c)
            
        #self.term.AppendText(event.text)    
        
    def OnAbout(self,e):
        #x = "\x13\x01\x01\xf7\xef\x00\x80\x00o\x00\x00\x00\x13\x01\x01\xff#4\x11\x00\xb7\x97\x01\x08\x13\x85\x07\xa7\x17\xf3\xfe\xf7\xe7\x00\x83\x13\x13\x00\x00\x00\x830\x81\x00\x13\x01\x01\x01g\x80\x00\x00\x00\x00\x00\x00I own you!!\x00\x00\x00\x00\x0000000000000000000000000000000000000000000000000000000000000000008\x8a\x01\x08"
        exploit = open('../../exploit/work/exploit.raw', 'rb').read()
        for char in exploit:
            self.dut.uart_write(char)
        self.dut.uart_write('\n')
    
        
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        #dlg = wx.MessageDialog( self, "A small text editor", "About Sample Editor", wx.OK)
        #dlg.ShowModal() # Show it
        #dlg.Destroy() # finally destroy it when finished.
        #self.term.WriteText('hello')

    def OnExit(self,e):
        self.Close(True)  # Close the frame.




app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()
