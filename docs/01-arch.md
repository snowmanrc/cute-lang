
# Architecture

### Overview

`Cute` is a 64-bit register-based virtual machine toolchain consisting of two components:

1. `compiler`: Compiles `.ct` text files into `.cute` executable images.
2. `engine`: The runtime that loads and executes `.cute` images.


### Toolchain Pipeline
```
Source Code (.ct)
		|
	    v
┌────────────────────┐
│    Cute Compiler   │  (Compiling code file/s to a single image file)
└────────────────────┘
		|
		v
Executable Image (.cute)
		|
		v
┌────────────────────┐
│    Cute Runtime    │  (Executing image file)
└────────────────────┘
```

### Project Structure
``` bash
.
├── Compiler # Main Cute Compiler
│   ├── orchestration # sets up and calls everything
│   ├── lexing  # converts source code into lexemes 
│   ├── parsing # parses tokens to construct an ast
│   ├── resolution # name resolution and operation resolution
│   ├── codegen # converting AST to bytecode
│   └── defs # common definitions required by the compiler
│
├── Engine # Main Engine Source Code
│   ├── common # common headers needed throughout the engine
│   ├── core # heart of the runtime
│   ├── image # image loading and management
│   ├── objects # objects subsystem, gc, object defintions and manager
│   └── utils # small utils needed in the engine
│
├── main # Main binary entry point: cute
│
├── dev # Place for testing
│
├── editor # tooling for editors
│
└── docs # Documentation
    └── records # list of recorded design choices
```

### Building

It is required that you build the engine using either `gcc` or `clang`.
The build system recommended is `ZeroBuild`.
See more on how to build [here](07-building.md).