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

#include "freertos_hooks.h"

/* RISCV includes */
#include "syscalls.h"
#include "clib.h"

/* The period after which the check timer will expire provided no errors have
been reported by any of the standard demo tasks.  ms are converted to the
equivalent in ticks using the portTICK_PERIOD_MS constant. */
#define mainCHECK_TIMER_PERIOD_MS			( 5000UL / portTICK_PERIOD_MS )

/* A block time of zero simply means "don't block". */
#define mainDONT_BLOCK						( 0UL )

/*-----------------------------------------------------------*/

/*
 * The check timer callback function, as described at the top of this file.
 */
static void prvCheckTimerCallback( TimerHandle_t xTimer );
static void ledTimerCallback(__attribute__ ((unused)) TimerHandle_t xTimer );


/*-----------------------------------------------------------*/
extern int systrap;
extern int systrapval;

int led_pipe;

int main( void ){
	TimerHandle_t xCheckTimer = NULL;
	dbprintf("start main\n"); 

	led_pipe = open("run/spike/ld_pipe", O_WRONLY | O_NONBLOCK, 0);
	dbprintf("ld_pipe = 0x%08x\n", led_pipe);

	dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
	dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
	
	/* create the tasks */
	InitCmdHandlerTask();

	
	/* Create the software timer that performs the 'check' functionality,
	as described at the top of this file. */
	xCheckTimer = xTimerCreate( "CheckTimer",					/* A text name, purely to help debugging. */
								( mainCHECK_TIMER_PERIOD_MS ),	/* The timer period, in this case 3000ms (3s). */
								pdTRUE,							/* This is an auto-reload timer, so xAutoReload is set to pdTRUE. */
								( void * ) 0,					/* The ID is not used, so can be set to anything. */
								ledTimerCallback			/* The callback function that inspects the status of all the other tasks. */
							  );
	dbprintf("Free heapsize %d\n", xPortGetFreeHeapSize());

	/* If the software timer was created successfully, start it.  It won't
	actually start running until the scheduler starts.  A block time of
	zero is used in this call, although any value could be used as the block
	time will be ignored because the scheduler has not started yet. */
	if( xCheckTimer != NULL )
	{
		xTimerStart( xCheckTimer, mainDONT_BLOCK );
	}

	/* Start the kernel.  From here on, only tasks and interrupts will run. */
	dbprintf("Free heapsize %d\n", xPortGetFreeHeapSize());
	vTaskStartScheduler();

	/* Exit FreeRTOS */
	return 0;
}
/*-----------------------------------------------------------*/

static void ledTimerCallback(__attribute__ ((unused)) TimerHandle_t xTimer )
{
	static char* led_off = "0\n";
	static char* led_on = "1\n";
	
	static int led = 0;

	write(led_pipe, led ? "0" : "1", sizeof("0")); 
	led =~ led;
}
