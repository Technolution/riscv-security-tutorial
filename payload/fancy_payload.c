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

void payload(void);

extern int start;

void payload(void){

	const char * hacked = "\n##     ##    ###     ######  ##    ## ######## ########  \r\n"
	"##     ##   ## ##   ##    ## ##   ##  ##       ##     ## \r\n"
	"##     ##  ##   ##  ##       ##  ##   ##       ##     ## \r\n"
	"######### ##     ## ##       #####    ######   ##     ## \r\n"
	"##     ## ######### ##       ##  ##   ##       ##     ## \r\n"
	"##     ## ##     ## ##    ## ##   ##  ##       ##     ## \r\n"
	"##     ## ##     ##  ######  ##    ## ######## ########  \r\n";


    //printf("\n\n%s\n\n",hacked);
	int num = 0;
    for(;;){
        setLeds(0x9700, 0);

		for(int a = 0;a<10;a++){
			printf("\f");
			for(int i = 0;i<(a+10);i++){
				printf("\n");
			}
			printf("%s",hacked);
			vTaskDelay(100);
		}
		for(int a = 10;a>0;a--){
			printf("\f");
			for(int i = 0;i<(a+10);i++){
				printf("\n");
			}
			printf("%s",hacked);
			vTaskDelay(100);
		}
    }
}
