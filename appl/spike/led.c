/*
  (C) COPYRIGHT 2016 TECHNOLUTION B.V., GOUDA NL
  =======          I                   ==          I    =
     I             I                    I          I
|    I   ===   === I ===  I ===   ===   I  I    I ====  I   ===  I ===
|    I  /   \ I    I/   I I/   I I   I  I  I    I  I    I  I   I I/   I
|    I  ===== I    I    I I    I I   I  I  I    I  I    I  I   I I    I
|    I  \     I    I    I I    I I   I  I  I   /I  \    I  I   I I    I
|    I   ===   === I    I I    I  ===  ===  === I   ==  I   ===  I    I
|                 +---------------------------------------------------+
+----+            |  +++++++++++++++++++++++++++++++++++++++++++++++++|
     |            |             ++++++++++++++++++++++++++++++++++++++|
     +------------+                          +++++++++++++++++++++++++|
                                                        ++++++++++++++|
                                                                 +++++|
 */

#include "led.h"

#include "FreeRTOS.h"
#include "clib.h"

int led_pipe;
int led_state[4] = {0, 0, 0, 0};

void initLeds(void) {
	led_pipe = open("run/spike/ld_pipe", O_WRONLY | O_NONBLOCK, 0);
	dbprintf("ld_pipe = 0x%08x\n", led_pipe);
}

void setLed(int index, int state) {
	//dbprintf("Setting led %d to %d\n", index, state);

	led_state[index] = state;
}

void writeLeds(void) {
	char writeBuffer[100];
	sprintf(writeBuffer, "%d%d%d%d", led_state[0], led_state[1], led_state[2], led_state[3]);
	write(led_pipe, writeBuffer, sizeof(writeBuffer));
}
