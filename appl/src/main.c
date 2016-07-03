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

extern unsigned long __data_start;
extern unsigned long __data_end;
extern unsigned long __flash_data_start;

volatile int test = 0xABC505;

int main( void ){
	dbprintf("start main\n");

	dbprintf("test = 0x%08x\n", test);
	test = test + 8;
	dbprintf("test = 0x%08x\n", test);

	printf("__data_start: 0x%08x\n__data_end: 0x%08x\n", &__data_start, &__data_end);
/*
	for (unsigned long i = (unsigned long)&_data_start; i <= (unsigned long)&_data_end; i += 4){
		printf("0x%08x: 0x%04x\n", i, *((unsigned short *)i));
		printf("0x%08x: 0x%04x\n", i, *((unsigned short *)(i + 2)));
		printf("0x%08x: 0x%08x\n", i, *((unsigned long *)i));
	}

	int j = 0;
	for (unsigned long i = (unsigned long)&_data_start; i <= (unsigned long)&_data_end; i += 4){
		*((unsigned long *)i) = j;
		j++;
	}

	for (unsigned long i = (unsigned long)&_data_start; i <= (unsigned long)&_data_end; i += 4){
		printf("0x%08x: 0x%04x\n", i, *((unsigned short *)i));
		printf("0x%08x: 0x%04x\n", i, *((unsigned short *)(i + 2)));
		printf("0x%08x: 0x%08x\n", i, *((unsigned long *)i));
	}

	j = 0;
	for (unsigned long i = (unsigned long)&_data_start; i <= (unsigned long)&_data_end; i += 4){
		*((unsigned long *)i) = (&_flash_data_start)[j];
		j++;
	}

	for (unsigned long i = (unsigned long)&_data_start; i <= (unsigned long)&_data_end; i += 4){
		printf("0x%08x: 0x%04x\n", i, *((unsigned short *)i));
		printf("0x%08x: 0x%04x\n", i, *((unsigned short *)(i + 2)));
		printf("0x%08x: 0x%08x\n", i, *((unsigned long *)i));
	}
*/
	initLeds();

	dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
	
	/* create the tasks */
	InitCmdHandlerTask();
	dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
	InitTunnelTask();

	/* Start the kernel.  From here on, only tasks and interrupts will run. */
	dbprintf("Free heapsize %d\n", xPortGetFreeHeapSize());
	vTaskStartScheduler();

	/* Exit FreeRTOS */
	return 0;
}

