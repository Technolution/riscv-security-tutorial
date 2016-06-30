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
/*
 *
 */

/* Kernel includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "timers.h"

/* Common demo includes. */
#include "cmd_handler.h"
#include "led.h"
#include "tunnel.h"

#include "freertos_hooks.h"

/* RISCV includes */
#include "clib.h"


/* A block time of zero simply means "don't block". */
#define mainDONT_BLOCK						( 0UL )

/*-----------------------------------------------------------*/
extern int systrap;
extern int systrapval;

int main( void ){
	dbprintf("start main\n"); 

	initLeds();

	dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
	dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
	
	/* create the tasks */
	InitCmdHandlerTask();
	InitTunnelTask();

	/* Start the kernel.  From here on, only tasks and interrupts will run. */
	dbprintf("Free heapsize %d\n", xPortGetFreeHeapSize());
	vTaskStartScheduler();

	/* Exit FreeRTOS */
	return 0;
}

