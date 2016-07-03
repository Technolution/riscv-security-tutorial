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
#include "shared.h"

#define MAX_RX_DATA_SIZE 256

/*-----------------------------------------------------------*/
static QueueHandle_t xRxQueue;
static QueueHandle_t xTxQueue;

//static void vSerialRxTask(void *pvParameters);
static void vSerialTxTask(void *pvParameters);


/*-----------------------------------------------------------*/
xComPortHandle xSerialPortInitMinimal(unsigned long ulWantedBaud, unsigned portBASE_TYPE uxQueueLength)
{
	/* Create the rx and tx queues. */
	xRxQueue = xQueueCreate(uxQueueLength, sizeof(signed char));
	xTxQueue = xQueueCreate(uxQueueLength, sizeof(signed char));
    
    /* background task to perform the actual port read & write */   
    //xTaskCreate(vSerialRxTask, "SerialRxTask", configMINIMAL_STACK_SIZE, NULL, 2, NULL );
    xTaskCreate(vSerialTxTask, "SerialTxTask", configMINIMAL_STACK_SIZE, NULL, 2, NULL );

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

void UartRxRdyHandler(void)
{
    uint8_t rx_data[MAX_RX_DATA_SIZE] = {0};
	uint8_t rx_size = 0;

	rx_size = UART_get_rx( &g_uart, rx_data, sizeof(rx_data) );
	for(int i = 0; i < rx_size; i++){
		xQueueSendFromISR(xRxQueue, &rx_data[i], NULL);
	}
}


//static void vSerialRxTask(void *pvParameters)
//{
//    (void)pvParameters;
//
//    uint8_t rx_data[MAX_RX_DATA_SIZE] = {0};
//    for(;;){
//        uint8_t rx_size = UART_get_rx( &g_uart, rx_data, sizeof(rx_data) );
//		for(int i = 0;i < rx_size;){
//			if(xQueueSend(xRxQueue, &rx_data[i],1000) == pdPASS){
//				i++;
//			}
//		}
//		if(rx_size == 0){
//	        vTaskDelay(10);
//		}
//    }
//}

static void vSerialTxTask(void *pvParameters)
{   
    (void)pvParameters;

    char cOutChar = 0;
    for(;;){
       if(xQueueReceive(xTxQueue, &cOutChar, 10000) == pdPASS){
		    UART_send(&g_uart, (const uint8_t *)&cOutChar, 1);
        }
    }
}
