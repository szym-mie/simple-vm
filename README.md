# Simple VM

### Complete package: bytecode assembler + virtual machine

I was going to write something longer here, but I will just give instructions and let anyone explore this project for themselves instead.

IMPORTANT: Windows support for VM was not tested. Currently the code uses standard library only.

### Instructions

How to assemble and run the example program:
```sh
./svm-asm.sh -i in.svm
./svm-vm svm.out
```

See available instructions and directives:
```sh
./svm-asm.sh --man
```

