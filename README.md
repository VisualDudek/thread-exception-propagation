# Exception propagation in concurrency models

Exceptions in worker threads NOT propagating is the default behavior across Python concurrency models.


- Interpreter lifecycle calls `threading._shutdown` at finish main program, it is not handled by `atexit` module.