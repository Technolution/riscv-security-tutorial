#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>
#include <unistd.h>

#include "encoding.h"
#include "shared.h"
#include "FreeRTOS.h"

//#include "clib.h"

extern plic_instance_t g_plic;
extern uint8_t* ucHeap;


uintptr_t handle_trap(uintptr_t mcause, uintptr_t epc)
{
	write(1, "trap\n", 5);
	printf("mcause : 0x%08x\nepc    : 0x%08x\n", mcause, epc);

	mdump(0x80000000, 32 * 1024);

    _exit(1 + epc);
    return epc;
}

/*
void __attribute__ ((naked)) handle_interrupt()
{
	printf("interrrupt");

}


void is_tick_timer_interrupt()
{
	return PLIC_claim_interrupt(&g_plic) == INT_DEVICE_TIMER0;
}



void hanlde_interrupt(unsigned int int_id)
{

}

*/

void _init(void)
{
  UART_init( &g_uart, COREUARTAPB0_BASE_ADDR, BAUD_VALUE_57600, (DATA_8_BITS | NO_PARITY) );


  extern int main(int, char**);
  const char *argv0 = "hello";
  char *argv[] = {(char *)argv0, NULL, NULL};

  exit(main(1, argv));
}
