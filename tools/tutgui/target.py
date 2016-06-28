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

import rx
import tx
import led

class Target(object):
    def __init__(self):      
        # our UART consists of a RX and TX path as seen from the target
        self.TX_FIFO_PATH = "../../appl/run/spike/tx_pipe"
        self.RX_FILE_PATH = "../../appl/run/spike/rx_file"
        self.RX_TMP_FILE_PATH = "../../appl/run/spike/_rx_file"
        self.LD_FIFO_PATH = "../../appl/run/spike/ld_pipe"
        self.BUFFER_SIZE = 1024
   
    def start_threads(self, stream, parent):
        self.rx_thread = rx.RxThread(self.RX_FILE_PATH, self.RX_TMP_FILE_PATH)
        self.tx_thread = tx.TxThread(self.TX_FIFO_PATH, parent)
        self.led_thread = led.LedThread(self.LD_FIFO_PATH, parent);
        self.rx_thread.start()
        self.tx_thread.start()
        self.led_thread.start()
    
    def uart_read(self):
        return os.read(self.tx_pipe, self.BUFFER_SIZE)
        
    def uart_write(self, data):
        print ">>> %s" % data
        rx.rxlock.acquire()
        try:
            rx_file = open(self.RX_TMP_FILE_PATH, 'a+', 0)
            rx_file.write(data)
            rx_file.close()
        finally:
            rx.rxlock.release()

