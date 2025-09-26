# Exception propagation in concurrency models

Exceptions in worker threads NOT propagating is the default behavior across Python concurrency models.


- `threading` primitives: `.Thread`
- `concurrent.futures` module provide a high-level interface for async. exacuting callables.
- `concurrent.futures` primitives: `.as_completed`
- why it is important to run `.join()` on thread? after `.start()`?
- howto using threading wrap blocking teask e.g. `time.sleep` to run it in concurrent way
- does `future.rsult()` call is blocking? I think yes.


## Threading intro

- by default new thread run as non-daemon, inherit from main thread. `002`
- main program run as non-deamon. `003`
- Interpreter lifecycle calls `threading._shutdown` at the finish of the main program; it is not handled by the `atexit` module.

- `_thread_shutdown()` is a C-level fn. called at the very end of `threading._shutdown()`
- `_thread` module is implementd in `cpython/Modules/_threadmodule.c` file. It is intended to be used as a Python-exposed C function for the `_thread` module.
- `ThreadPoolExecutor` submit and collect results examples. **005**
- **005** there is trick taht make it hard to read, `as_completed` takes `fs: Iterable` The sequnce of Futures, in code example dict is passed BUT with keys as futures which when iterate -> sequence of Futures. 
- **006** shows that feature`.result()` call is blocking
- how to catch exception in thread, **007**, refactor `time.sleep(2)` part into `as_completed()`
- numbering of task is wrong -> now I see why usefull dict{future: data} **008**