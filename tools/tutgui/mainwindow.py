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
import led
import target
import terminalwindow

myEVT_LED_CHANGE = wx.NewEventType()
EVT_LED_CHANGE = wx.PyEventBinder(myEVT_LED_CHANGE, 1)

myEVT_TEXT_TX = wx.NewEventType()
EVT_TEXT_TX = wx.PyEventBinder(myEVT_TEXT_TX, 1)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):        
       
        wx.Frame.__init__(self, parent, title=title, size=(800,475), pos=(960,0))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        #self.control.OnChar = self.OnChar        

        #self.control.Bind(wx.EVT_CHAR, self.OnChar, self)
        statusbar = self.CreateStatusBar() # A StatusBar in the bottom of the window
        self.led = led.LED(statusbar, pos=(5,3))
        
        self.dut = target.Target()
        self.term = terminalwindow.TerminalWindow(self, self.dut)
        #term.ForkCommand('bash', ['bash'])
        #term.Bind(wxterm.EVT_TERM_CHILD_EXIT, self.OnExit)

        self.dut.start_threads(self.term, self)
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
        self.led.SetState(event.index, event.value)    
        
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
