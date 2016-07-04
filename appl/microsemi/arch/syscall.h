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
/**
 * @file
 * @author  Jonathan Hofman <jonathan.hofman@technolution.nl>
 *
 * @brief   This file is based upon diverse low level stubs implementing
 *          diverse syscalls. The file is made based on numerous examples
 *          from the RISC-V codebase.
 */

#ifndef SYSCALL_H
#define SYSCAL_H

void write_hex(int fd, uint32_t hex);
void _exit(int code);
//void *sbrk(ptrdiff_t incr);
//static int stub(int err);
//int open(const char* name, int flags, int mode);
//int openat(int dirfd, const char* name, int flags, int mode);
//int close(int fd);
//int execve(const char* name, char* const argv[], char* const env[]);
//int fork();
//int fstat(int fd, struct stat *st);
//int getpid();
int isatty(int fd);
//int kill(int pid, int sig);
//int link(const char *old_name, const char *new_name);
///off_t lseek(int fd, off_t ptr, int dir);
ssize_t read(int fd, void* ptr, size_t len);
//int stat(const char* file, struct stat* st);
//clock_t times(struct tms* buf);
//int unlink(const char* name);
///int wait(int* status);
ssize_t write(int fd, const void* ptr, size_t len);

#endif
