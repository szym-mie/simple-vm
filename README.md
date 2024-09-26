# Simple VM

### Complete package: bytecode assembler + virtual machine

I was going to write something longer here, but I will just give instructions on how to build and use assembler and virtual machine and let anyone explore this project for themselves instead.

IMPORTANT: Windows support for VM was not tested. Currently the code uses standard library only.

### Requirements

- Python 3.5+
- Clang/GCC, change using `CC` variable in `./vm/makefile` 
- Make

### Building

How to build virtual machine:
```sh
cd vm
make release
# make debug # if you need debugging symbols in the binary
```

### Running

How to assemble and run the example program:
```sh
./svm-asm.sh -i in.svm
./svm-vm svm.out
```
After running, remaining stack content will be displayed, this is the only way to get results back for now.

See available instructions and directives:
```sh
./svm-asm.sh --man
```

### Examples

#### Looping (loop.svm)

Loop and do nothing until counter is zero.
```
// counter
i32 5
// loop start : loc 1
dec // decrement
ez? // if zero put '1' on stack, '0' otherwise (doesn't consume previous value)
jez 1 // if not zero jump back to loop start
```