# Exception propagation in concurrency models

Exceptions in worker threads NOT propagating is the default behavior across Python concurrency models.

- howto using threading wrap blocking teask e.g. `time.sleep` to run it in concurrent way

## Threading intro

- by default new thread run as non-daemon, inherit from main thread. `002`
- main program run as non-deamon. `003`
- Interpreter lifecycle calls `threading._shutdown` at the finish of the main program; it is not handled by the `atexit` module.

- `_thread_shutdown()` is a C-level fn. called at the very end of `threading._shutdown()`
- `_thread` module is implementd in `cpython/Modules/_threadmodule.c` file. It is intended to be used as a Python-exposed C function for the `_thread` module.