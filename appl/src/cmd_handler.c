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

#include <stdio.h>
#include <string.h>

#include "clib.h"

/* Kernel includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "timers.h"

/* Common demo includes. */
#include "cmd_handler.h"
#include "serial.h"

static void vCmdHandlerTask( void *pvParameters );


xComPortHandle xComPort = NULL;
int blink = 0; 

int serial_putchr(int ch){
    if(xComPort != NULL){
        if (xSerialPutChar(xComPort, ch, 10) == pdTRUE) {
            return ch;
        }
    }

    return EOF;
}

void InitCmdHandlerTask(void){
	xComPort = xSerialPortInitMinimal(9600, 16);
    xTaskCreate(vCmdHandlerTask, "CmdHandlerTask", configMINIMAL_STACK_SIZE, NULL, 1, NULL );
}    
    

static int ReceiveCmd(char* buf){
	unsigned short idx = -1;

    /* accumulate characters until the enter is hit */
    do{
    	/* increment index pointer for each character increment */
        idx++;

        if(xSerialGetChar(xComPort, (signed char *)&buf[idx], portMAX_DELAY) == pdFALSE){
            continue;
        } 

        /* echo the character back to the terminal */
        xSerialPutChar(xComPort, buf[idx], 0);

        /* handle the hit of an backspace by shifting the idx back */
/*        if(buf[idx] == '\b'){
            idx -= 2;
        }
*/
        /* add a zero terminator on the end of the string, so we can print it for debugging */
        buf[idx + 1] = '\0';
        dbprintf("cmd = '%s', idx = %d\n", buf, idx);
    }while((buf[idx] != '\n') && (buf[idx] != '\r'));

    /* return the command string without the new line, so we have only the command */
    buf[idx] = '\0';

    /* return the length of the string */
    return idx + 1;
}    

static void ExecCmd(char *buf){
    if(!strcmp(buf, "faster")){
        blink++;
    } else if (!strcmp(buf, "slower")){
        blink--;
    } else if (!strcmp(buf, "stats")){
        printf("blink speed : %d\n", blink);
    } else {
        dbprintf("unkown command\n");
        printf("unknown command\n");
    }
}

    
static void HandleCmd(void){
	char cmd_str[256];

	memset(cmd_str, 0, sizeof(cmd_str));
	ReceiveCmd(cmd_str);
	ExecCmd(cmd_str);
}
    
static void vCmdHandlerTask( void *pvParameters ){
    (void)pvParameters;

	for(;;){
        printf("target> ");
        HandleCmd();
	}
}
