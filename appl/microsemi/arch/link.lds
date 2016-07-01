OUTPUT_ARCH( "riscv" )

_STACK_SIZE = DEFINED(_STACK_SIZE) ? _STACK_SIZE : 1024;
_HEAP_SIZE = DEFINED(_HEAP_SIZE) ? _HEAP_SIZE : 0;

MEMORY 
{
	flash (rx)	: ORIGIN = 0x60020000, LENGTH = 128K
	ram	  (xrw)	: ORIGIN = 0x80000000, LENGTH = 16K
}

SECTIONS
{
/*  . = 0x60020000; */
  .text : 
  {
    *entry.o(.text)
    *(.text)
  } > flash

  . = ALIGN(4);
  /* read only data segment */
  .srodata : {
    _gp = . + 0x800;
    *(.srodata.cst16) *(.srodata.cst8) *(.srodata.cst4) *(.srodata.cst2)
    *(.srodata*)
    . = ALIGN(4);
  } > flash

  __text_end__ = .; 
  _flash_data_start = .;
  /* data segment */
  .data : AT(_flash_data_start) { 
	   . = ALIGN(4);
	_data_start = .; 
    /* __flash_init_data_start__ = __text_end__; */
	*(.data) 
    *(.sdata .sdata.* .gnu.linkonce.s.*)
	   . = ALIGN(4);
	_data_end = .;
  } > ram /* AT>flash */
  
  
  /*. = 0x80000000;*/
  
  _data = .;
  _bss_start = .;

  /* bss segment */
  .sbss : {
    . = ALIGN(4);
    *(.sbss .sbss.* .gnu.linkonce.sb.*)
    *(.scommon)
    . = ALIGN(4);
  } > ram
  .bss : { 
	  . = ALIGN(4);
	*(.bss) 
	  . = ALIGN(4);
  } > ram
  _bss_end = .; 

  /* End of uninitalized data segement */

    /* Generate Stack and Heap definitions */

    .heap : {
       . = ALIGN(8);
       _heap = .;
       _heap_start = .;
       . += _HEAP_SIZE;
       _heap_end = .;
    } > ram

    .stack : {
       _stack_end = .;
       . += _STACK_SIZE;
       . = ALIGN(8);
       _stack = .;
       __stack = _stack;
    } > ram

  _end = .;
}

