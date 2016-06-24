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
/* Kernel includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "timers.h"
#include "FreeRTOSConfig.h"


#include "clib.h"
#include "serial.h"

#define RX_FILE  "run/spike/rx_file"
#define TX_FILE  "run/spike/tx_pipe"

/*-----------------------------------------------------------*/
static QueueHandle_t xRxQueue;
static QueueHandle_t xTxQueue;

static void vSerialRxTask(void *pvParameters);
static void vSerialTxTask(void *pvParameters);


/*-----------------------------------------------------------*/
xComPortHandle xSerialPortInitMinimal(unsigned long ulWantedBaud, unsigned portBASE_TYPE uxQueueLength)
{
    (void)ulWantedBaud;
    
	/* Create the rx and tx queues. */
	//dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
	xRxQueue = xQueueCreate(uxQueueLength, (unsigned portBASE_TYPE) sizeof(signed char));
	//dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
	xTxQueue = xQueueCreate(uxQueueLength + 1, (unsigned portBASE_TYPE) sizeof(signed char));
	//dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
    
    /* background task to perform the actual port read & write */   
	//dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
    xTaskCreate(vSerialRxTask, "SerialRxTask", configMINIMAL_STACK_SIZE, NULL, 1, NULL );
	//dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());
    xTaskCreate(vSerialTxTask, "SerialTxTask", configMINIMAL_STACK_SIZE, NULL, 1, NULL );
	//dbprintf("\nFree heapsize %d\n", xPortGetFreeHeapSize());

    /* we only support one serial port for now */
    return (void *)1;
}

/** vSerialPutString
 * 
 * NOTE: This implementation does not handle the queue being full as no
 * block time is used! 
 */
void vSerialPutString(xComPortHandle pxPort, const signed char * const pcString, unsigned short usStringLength)
{
    (void)pxPort;
    unsigned short i;

	/* Send each character in the string, one at a time. */
    for(i = 0; i < usStringLength; i++){
		xSerialPutChar( pxPort, pcString[i], 0);
	}
}

signed portBASE_TYPE xSerialGetChar(xComPortHandle pxPort, signed char *pcRxedChar, TickType_t xBlockTime)
{
    (void)pxPort;
    return xQueueReceive(xRxQueue, pcRxedChar, xBlockTime);
}


signed portBASE_TYPE xSerialPutChar(xComPortHandle pxPort, signed char cOutChar, TickType_t xBlockTime)
{
    (void)pxPort;
    return xQueueSend(xTxQueue, &cOutChar, xBlockTime); 
}    

portBASE_TYPE xSerialWaitForSemaphore(xComPortHandle xPort)
{
    (void)xPort;
    return 0;
}

void vSerialClose(xComPortHandle xPort)
{
    /* FIXME: should call close right here */
    (void)xPort;
    return;
}


/***********************************************************************
 * The two background tasks
 **********************************************************************/
static void vSerialRxTask(void *pvParameters)
{
    (void)pvParameters;
	/* open the rx channel from the host system in the simulator
	 * note that this will block until a writer has sent data to the pipe
	 */
    
    static char cRxChar[16] __attribute__((aligned(64)));
    for(;;){
        vTaskDelay(100);
        int rx_file = open(RX_FILE, O_RDONLY | O_NONBLOCK, 0);
        if(rx_file > 0){
            int len = 0;
            do{
                len = read(rx_file, cRxChar, sizeof(cRxChar));
                for(int i = 0; i < len; i++){
                    char c = cRxChar[i];
                    if(xQueueSend(xRxQueue, &c, portMAX_DELAY) != pdPASS){
                        dbprintf("error putting rx value in queue\n");
                    }
                }
            }while(len > 0);
            unlink(RX_FILE, 0);
        }
    }
}

static void vSerialTxTask(void *pvParameters)
{   
    (void)pvParameters;
    dbprintf("t0\n");
   	/* open the tx channel from the host system in the simulator
	 * note that this will block until a reader is connected to the pipe
	 */
	int tx_pipe = open(TX_FILE, O_WRONLY | O_NONBLOCK, 0);

    char cOutChar __attribute__((aligned(64))) = 0;
    for(;;){
       if(xQueueReceive(xTxQueue, &cOutChar, 1000) == pdPASS){
            write(tx_pipe, &cOutChar, 1);
        }
    }
}
