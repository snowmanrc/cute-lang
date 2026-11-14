
# Building Cute

The required compiler is `gcc` or `clang`.

> [!NOTE]
> The project uses the `zero-build` build system (which I made myself :p). It is recommended you install that before building `Cute`. It's just a python package away.
> 
> Check out zero-build here: [zero-build](https://github.com/kxmtkw/ZeroBuild)


To build, first clone the repository and `cd` into the repo root.


### With CMake
First, create the build files:
```bash
cmake -B build 
```
Then build:
```bash
cmake --build build
```

### With ZeroBuild
Just run:
```bash
zero make
```
This will build inside `.build` directory. The executables can be found in `.build/bin`