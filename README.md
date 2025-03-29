# Simple VM

### Complete package: bytecode assembler + virtual machine

I was going to write something longer here, but I will just give instructions on how to build and use assembler and virtual machine and let anyone explore this project for themselves instead.

IMPORTANT: Windows support for VM was not tested. However, the code uses standard library only for now.

### Requirements

- Python 3.5+
- Clang/GCC, change using `CC` variable in `./vm/makefile` 
- Make

### Building the virtual machine

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
./svm-vm.sh svm.out
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

loop:
dec
ez?
jez loop:
// it works if zero is left on the stack
```

### Expanding the instruction set

In the `/asm/res` path, you can find JSON instruction set files. They contain
all instructions that the VM should be able to decode and all the documentation
about each one of them.

Here is `i32` instruction from `instruction_set_0.json`:

```json
{
  "id": "0x01",
  "name": "i32",
  "doc": "put one 32 bit integer on stack",
  "params": [
    {
      "name": "val",
      "doc": "integer value"
    }
  ],
  "consumed": [],
  "produced": [
    {
      "name": "val",
      "doc": "integer value"
    }
  ]
}
```

By running the following command:
```sh
./svm-gen.sh -i asm/res/instruction_set_0.json
```
You would get .c and .h files containing C code implementation templates for
the instruction set:
```c
void i32_01(loc_t *loc, struct stack *st, const word_t *pv)
{
    // 'i32' code here
}
```

