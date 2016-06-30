OUTPUT_ARCH( "riscv" )

MEMORY 
{
	flash (rx)	: ORIGIN = 0x60020000, LENGTH = 128K
	ram	  (xrw)	: ORIGIN = 0x80000000, LENGTH = 64K
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
	_data_start = .; 
    /* __flash_init_data_start__ = __text_end__; */
	*(.data) 
    *(.sdata .sdata.* .gnu.linkonce.s.*)
	_data_end = .;
  } > ram /* AT>flash */
  
  
  /*. = 0x80000000;*/
  
  _data = .;
  _bss_start = .;

  /* bss segment */
	. = ALIGN(4);
  .sbss : {
    *(.sbss .sbss.* .gnu.linkonce.sb.*)
    *(.scommon)
  } > ram
  . = ALIGN(4);
  .bss : { 
	*(.bss) 
  } > ram
  _bss_end = .; 

  /* End of uninitalized data segement */
  _end = .;
  _heap_end = .;
}

