# Exception propagation in concurrency models

Exceptions in worker threads NOT propagating is the default behavior across Python concurrency models.


- `threading` primitives: class `.Thread`.Ciekawa podejście do konstrukora, który przyjmuje jedynie kwargs. What are main methods? `.start()` and `.join()`
- dlaczego konstruktor `.Thread` sypie błędem przy tupli z intem, `(1)` **012** GOTCHA `(1)` vs. `(1,)`
- ciekawy trick na przegląd istotnych obiektów "exportowanych" przez moduł -> przegląd listy `__all__` e.g. `threading.py`.
- `concurrent.futures` module provide a high-level interface for async. exacuting callables. 
- `concurrent.futures` primitives: `.as_completed`
- why it is important to run `.join()` on thread? after `.start()`?
- howto using threading wrap blocking teask e.g. `time.sleep` to run it in concurrent way
- does `future.rsult()` call is blocking? I think yes.
- how to return work from thread?
- how to communicate between threads? `queue.Queue`
- `queue.Queue` is Python primary thread-safe data structure for commuxnication between threads.
- producer-consumer pattern
- why `q.task_done()` is important? i w jaki sposób śledzi który element z kojeki jest teraz "obrabiany"?
- naturlane jest myślenie o jednej kolejce i kilku workerach, ale kolejka może być jedynie łacznikiem pomiędzy kilkoma instancjami(wątkami) producentów a multi-workerami
- `g.get()` without timeout will block forever if queue empty ? Zawsze do zastanowienia się jak oznaczyć że nie będzie więcej pracy dla consumera czyli jak odblolować `q.get()`?


## Assignments

Show me:
- that by default main prog. wait for thread to finish. **009**
- that raised exception in thread do not propagate to main prog. **010**



## Takeaway

- by default new thread run as non-daemon, inherit from main thread. **002**
```python
# threading.py
        if daemon is not None:
            if daemon and not _daemon_threads_allowed():
                raise RuntimeError('daemon threads are disabled in this (sub)interpreter')
            self._daemonic = daemon
        else:
            self._daemonic = current_thread().daemon # inherit daemon True/False from current thread
```
- main program run as non-deamon. `003`
- Interpreter lifecycle calls `threading._shutdown` at the finish of the main program; it is not handled by the `atexit` module.
- `_thread_shutdown()` is a C-level fn. called at the very end of `threading._shutdown()`
- `_thread` module is implementd in `cpython/Modules/_threadmodule.c` file. It is intended to be used as a Python-exposed C function for the `_thread` module.
- `ThreadPoolExecutor` from `concurrent.futures` lib. submit and collect results examples. **005**
- **005** there is trick taht make it hard to read, `as_completed` takes `fs: Iterable` The sequnce of Futures, in code example dict is passed BUT with keys as futures which when iterate -> sequence of Futures.
- **006** shows that feature`.result()` call is blocking
- how to catch exception in thread, **007**, refactor `time.sleep(2)` part into `as_completed()`
- numbering of task is wrong -> now I see why usefull dict{future: data} **008**
- when thread raise eception it will be printed into stderr BUT will not stop main prog. **010**, debuger jest na tyle sprytny że zatrzymuje działąnie programu, natomiast runtime np. `uv run [.py]` puszcza dalej.
- `q.tack_done()` jedynie decrementuje counter kolejki, ma znaczenie jedynie dla `q.join()` kiedy moża odblokować główny wątek. **011**
- multi workers, one queue **012**
- multi producer-consumer pattern with queue as communication data structure **013**


## Comprehensive Learning Path

### Foundation Level (Week 1) - Files 000-003

**Learning Objectives:**
1. **Understand Thread Creation and Execution** (000_threading.py)
   - Learn Thread class instantiation with target and args
   - Understand start() vs direct function calls
   - Master the critical importance of join() for synchronization

2. **Master Thread Lifecycle Management** (001_threading_daemon.py, 002_threading_daemon.py)
   - Understand daemon vs non-daemon thread behavior
   - Learn when threads terminate vs keep program alive
   - Explore sys.exit() behavior with active threads

3. **Explore Main Thread Properties** (003_threading_main.py)
   - Understand main thread characteristics
   - Learn thread hierarchy and inheritance

**Practical Exercises:**
1. Create a thread that downloads a file (simulate with time.sleep)
2. Create both daemon and non-daemon threads, observe program termination
3. Measure execution time with and without join() calls

### Intermediate Level (Week 2) - Files 004-006

**Learning Objectives:**
1. **Program Termination Understanding** (004_atexit.py)
   - Learn about atexit handlers vs thread cleanup
   - Understand Python interpreter shutdown sequence

2. **ThreadPoolExecutor Fundamentals** (005_threading_executor.py)
   - Master submit() vs map() methods
   - Understand Future objects and result collection
   - Learn as_completed() for result processing as they finish

3. **Blocking Behavior Mastery** (006_concurrent_futures.py)
   - Understand when future.result() blocks vs returns immediately
   - Learn optimal result collection strategies

**Key Concepts to Master:**
- Future Objects: State management (done(), cancelled(), result())
- Resource Pooling: How ThreadPoolExecutor manages worker threads
- Result Collection Patterns: Order-preserving vs completion-order processing
- Context Managers: Automatic resource cleanup with `with` statements

**Practical Exercises:**
1. Use ThreadPoolExecutor to fetch multiple URLs concurrently
2. Process a list of files with different execution patterns
3. Measure sequential vs concurrent execution times

### Advanced Level (Week 3) - Files 007-008

**Learning Objectives:**
1. **Exception Handling in Concurrent Environments** (007_threadpoolexec_exception.py)
   - Understand why exceptions don't propagate from worker threads
   - Learn how exceptions are stored in Future objects
   - Master exception retrieval and handling patterns

2. **Advanced Exception Patterns** (008_threadpoolexec_exception.py)
   - Implement exception handling with as_completed()
   - Learn robust error handling in concurrent systems
   - Understand partial failure scenarios

**Critical Concepts:**
- Exception Isolation: Worker threads vs main thread exception handling
- Future Exception Storage: How failed futures store exception information
- Graceful Degradation: Handling partial failures in concurrent operations
- Error Aggregation: Collecting and reporting multiple concurrent failures

**Practical Exercises:**
1. Process files with some expected to fail, handle gracefully
2. Check multiple services, handle individual failures
3. Build a concurrent pipeline with error recovery mechanisms

### Mastery Level - Beyond the Codebase

**Advanced Topics for Further Exploration:**

1. **Synchronization Primitives**
   - threading.Lock, RLock, Semaphore, Condition
   - Queue.Queue for thread-safe communication
   - threading.Event for coordination

2. **Alternative Concurrency Models**
   - asyncio for I/O-bound tasks
   - multiprocessing for CPU-bound tasks
   - Comparison of threading vs asyncio vs multiprocessing

3. **Performance Optimization**
   - Thread pool sizing strategies
   - GIL (Global Interpreter Lock) implications
   - Memory management in concurrent programs

4. **Production Patterns**
   - Structured logging in concurrent applications
   - Monitoring and observability
   - Error handling and circuit breaker patterns

### Common Pitfalls and Best Practices

**Critical Pitfalls to Avoid:**
1. Forgetting join(): Always join threads unless they're daemon threads for cleanup tasks
2. Exception Swallowing: Always check Future.result() or use proper exception handling
3. Resource Leaks: Always use context managers with ThreadPoolExecutor
4. Race Conditions: Understand shared state access patterns

**Best Practices:**
1. Use ThreadPoolExecutor over Thread: For most concurrent tasks
2. Handle Exceptions Explicitly: Never ignore potential Future exceptions
3. Size Thread Pools Appropriately: Match pool size to task characteristics
4. Use as_completed(): For optimal result processing in most scenarios

### Recommended Learning Sequence

1. **Week 1**: Master files 000-003, focus on basic threading concepts
2. **Week 2**: Work through files 004-006, build ThreadPoolExecutor expertise
3. **Week 3**: Deep dive into files 007-008, master exception handling patterns
4. **Week 4**: Build a complete project combining all concepts
5. **Ongoing**: Explore advanced topics and alternative concurrency models