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

	const char * hacked = "\n##     ##    ###     ######  ##    ## ######## ########  \n"
	"##     ##   ## ##   ##    ## ##   ##  ##       ##     ## \n"
	"##     ##  ##   ##  ##       ##  ##   ##       ##     ## \n"
	"######### ##     ## ##       #####    ######   ##     ## \n"
	"##     ## ######### ##       ##  ##   ##       ##     ## \n"
	"##     ## ##     ## ##    ## ##   ##  ##       ##     ## \n"
	"##     ## ##     ##  ######  ##    ## ######## ########  \n";


    for(;;){
        setLeds(0x9700, 0);

		for(int a = 0;a<10;a++){
			printf("\f");
			for(int i = 0;i<a;i++){
				printf("\n");
			}
			printf("%s",hacked);
			vTaskDelay(100);
		}
		for(int a = 10;a>0;a--){
			printf("\f");
			for(int i = 0;i<a;i++){
				printf("\n");
			}
			printf("%s",hacked);
			vTaskDelay(100);
		}
    }
}
