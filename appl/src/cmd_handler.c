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

#include "tunnel.h"

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
	xComPort = xSerialPortInitMinimal(9600, 1024);
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
        printf("[%d] = 0x%02x\n", idx, buf[idx]);

        /* handle the hit of an backspace by shifting the idx back */
        /* if(buf[idx] == '\b'){
            idx -= 2;
        }*/
    }while((buf[idx] != '\n') && (buf[idx] != '\r'));

    /* send a '\r' when we exited on a '\n */
    //if(buf[idx] == '\n'){
    //    xSerialPutChar(xComPort, '\r', 0);
    //}

    /* return the command string without the new line, so we have only the command */
    buf[idx] = '\0';

    mdump(buf, 300);

    /* return the length of the string */
    return idx + 1;
}    

static void ExecCmd(char *buf){
    if(!strcmp(buf, "normal")){
        setGreenTimeMs(2000);
        setWaitTimeMs(2000);
    } else if (!strcmp(buf, "rush")){
        setGreenTimeMs(6000);
        setWaitTimeMs(2000);
    } else if (!strcmp(buf, "stats")){
        printf("Green time : %d ms\n", getGreenTimeMs());
        printf("Wait time  : %d ms\n", getWaitTimeMs());
    } else if (!strcmp(buf, "debug")){
    	register int *sp asm("sp");
    	extern void *pxCurrentTCB;

    	printf("@cmd_str = 0x%08x\n", (unsigned int)buf);
    	printf("pxCurrentTCB = 0x%08x\n", (unsigned int) pxCurrentTCB);
    	printf("sp = 0x%08x\n", (unsigned int)sp);
    } else if (!strcmp(buf, "dump")) {
    	unsigned int i = (unsigned int)buf;
    	for(;i < (unsigned int)&buf + 300; i += 4){
    		printf("[0x%08x] = 0x%08x\n", i, *((unsigned int *) i));
    	}
    } else if (!strcmp(buf, "mdump")) {
    	mdump(buf, 300);
    } else if (!strcmp(buf, "fdump")) {
    	extern void *pxCurrentTCB;
    	mdump((void *)((unsigned int)pxCurrentTCB - 1024), 1024 + 256);
    } else {
        printf("\nunknown command, '%s'\n\n", buf);
        printf("*************************************************\n");
        printf("* The following commands are available:\n");
        printf("* > normal\n");
        printf("*      use short delays, to optimize waiting times\n");
        printf("* > rush\n");
        printf("*      use long delays, to optimize througput during rush hours\n");
        printf("* > stats\n");
        printf("*      print current wait time and green wait time\n");
        printf("*************************************************\n");
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
