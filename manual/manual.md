RISCV Security demo
=======
Virtualbox setup
-----------
* Extract virtualbox image.
* Make sure the programmer is selected as usb device in virtualbox.  Go to Settings > USB > Add USB Filter > Microsemi Embedded FLashPro5.

![Usb-virtualbox](img/usb-virtualbox.png?raw=true "Usb-virtualbox")

Get code
-----------
* Open terminal


    $git clone  https://github.com/Technolution/riscv-security-tutorial.git
Program FPGA
-----------
    $./start_FPExpress
* Click New..
* Select programming job file: riscv-security-tutorial/fpga/sf2_1_full.job

![Settings terminal](img/settings-terminal.png?raw=true "Settings terminal")
* Click the large RUN button
Make FreeRTOS application
	$ cd riscv-security-tutorial/appl/
$ export MAKETARGET=microsemi
$ make

Make exploit
-----------
	$ cd riscv-security-tutorial/exploit/
	$ make

Make payload
-----------
	$ cd riscv-security-tutorial/payload/
	$ make

Open serial terminal
-----------
	$ cd riscv-security-tutorial/tools/terminal
	$ ./wxTerminal.pyw
* Select port: /dev/ttyUSB2
* Leave the other settings as is.

![Settings terminal](img/settings-terminal.png?raw=true "Settings terminal")

Try application commands
-----------
	rush
	normal
	stats

Upload exploit & payload
-----------
* Tools > Upload blob..
* Select riscv-security-tutorial/exploit/work/exploit.raw 
* See ready4payload

![exploit](img/exploit.png?raw=true "exploit")
* Tools > Upload blob..
* Select riscv-security-tutorial/payload/work/payload.raw
* See HACKED

![HACKED](img/hacked.png?raw=true "HACKED")

