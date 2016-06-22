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

/* a very naive implementation for a LED PWM. Because we manually stop
 * and restart the timers we will see some period jitter.
 */
 
#define LED_PWM_TICKS (50)	

int dutyCycle = 10; // FIXME

void vCreateLedTasks( void )
{

}

static void vLedPwmTask( void *pvParameters )
{
	TickType_t xLastWakeTime;
	const TickType_t xFrequency = LED_PWM_TICKS;

    // Initialise the xLastWakeTime variable with the current time.
    xLastWakeTime = xTaskGetTickCount();

    for(;;){
        // Wait for the next cycle.
        vTaskDelayUntil( &xLastWakeTime, xFrequency );		
		ledOn();
		vTaskDelay(dutyCycle);
		ledOff();
    }	
}

void ledOn(void){
	//TODO JHO: fix led on
}

void ledOff(void){
	//TODO JHO: fix led on
}
	
