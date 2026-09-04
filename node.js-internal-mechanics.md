# Node.js internal mechanics

1. Understand what is a program vs process vs threads
2. OS scheduler decide which thread will run on which core(inside CPU).
3. The Node process itself
4. Why your JS thread can't just "wait"
5. libuv — the mediator between your JS thread and the OS
6. The event loop — how the result gets back to you
7. I/O-bound work vs CPU-bound work
8. Worker threads — giving yourself a second real thread
9. Child processes — a separate process entirely
10. How isolated processes talk anyway

## Layer 0: What is a program?
This is the static code stored on our hard drive like index.js or any js file.
It isn't actively doing anything yet.

## Layer 1: What is a process?

- A **process** is a running program with its own isolated slice of memory (& resources) (address space): its own heap, stack, global variables, open file handles. 
- Two processes cannot see each other's memory directly. 
- When you run `node app.js`, the OS creates one process for it.

## Layer 2: What is a thread?

- A **thread** is a unit of execution *inside* a process. Inside the process, a thread is the actual worker executing the instructions line by line.

- A process can have multiple threads, and all threads inside the same process **share the same memory** (heap, globals) but each thread gets its own **call stack** (its own record of "what function is running, what called it").

Why does this matter: shared memory means threads can communicate instantly (just read a shared variable) but also means they can corrupt each other's data if two threads write to the same thing at once — that's a race condition. This is *the* core tradeoff in all multithreaded programming.

## Layer 3: The OS scheduler and the CPU

Your machine has a fixed number of CPU cores. The OS scheduler's job is to decide which thread, from all threads across all processes on the machine, gets to run on a core at any given moment. It gives each thread a tiny time slice, then swaps it out (**context switch**) for another. Context switching costs real time (saving/restoring registers, stack pointers) — this is *why* having thousands of OS threads is expensive: the OS spends more time swapping between them than doing useful work.

**This is the actual problem Node was designed to avoid.**


## Layer 4: The Node process itself

When you run `node app.js`, the OS creates **one process**. Inside that process, Node/V8 (the JS engine) creates:

- **1 main thread** — this is where your JS code (the "call stack") actually executes, one line at a time.
- **libuv's thread pool** — a small set of *additional* OS threads (default 4), living inside the same Node process, purely for offloading certain blocking work (explained below).
- Some other internal V8 background threads (garbage collection, JIT compilation) — usually invisible to you, not part of "your" concurrency model.

So already: "Node is single-threaded" is really "**your JS callback code** runs on one thread," not "the Node process only has one thread." The process has several; you only ever write code for one of them.

## Layer 5: Why your JS thread can't just "wait"

If your one JS thread calls a blocking operation (like `readFileSync`), that thread literally halts — the call stack sits there until the disk responds. Nothing else can run: no other request gets handled, no timer fires, nothing. This is the failure mode Node is built entirely around avoiding.

## Layer 6: libuv — the mediator between your JS thread and the OS

libuv is a C library Node is built on. It sits between your single JS thread and the operating system, and its job is exactly this handoff:

1. Your JS thread calls something async, e.g. `fs.readFile('x', cb)`.
2. Instead of doing the work itself, your JS thread just **registers** the request with libuv and immediately moves on to the next line of code — the call stack is free again.
3. libuv figures out *how* to actually get that work done without blocking your JS thread. It has two strategies, and which one it uses depends on what kind of work it is:

   **(a) True async OS support exists** (most networking): libuv hands the request to the OS's native async I/O facility — epoll (Linux), kqueue (macOS), IOCP (Windows). The OS itself watches the network socket and does the waiting — no extra thread needed at all. The OS interrupts libuv when data's ready.

   **(b) No good async OS API exists** (most filesystem calls, DNS lookups, some crypto): libuv can't offload this to the OS asynchronously, so it fakes it — it takes one of its own **thread pool** threads (from layer 3) and runs the *blocking* call there instead. That pool thread sits and waits (blocked), but it's not your JS thread, so your JS thread stays free.

Either way, your JS thread never blocks — libuv either delegates to the OS's async machinery, or blocks a *disposable* pool thread on your behalf.

## Layer 7: The event loop — how the result gets back to you

libuv runs the **event loop**, a `while(true)` cycle on your main thread with distinct phases (timers, I/O callbacks, idle, poll, check, close). Every time an I/O operation finishes (OS notifies libuv, or a pool thread finishes its blocking call), libuv doesn't run your callback immediately — it queues it. The event loop, on its next relevant phase, pulls queued callbacks and executes them **one at a time on your single JS thread**.

This is the piece that makes it click: **the waiting is parallel (OS + thread pool), but the actual execution of your callback code is always serial**, because there's only one JS call stack. Concurrency (many things in-flight) ≠ parallelism (many things executing simultaneously) — Node gives you the first, not the second, for your own code.

## Layer 8: Now the I/O vs CPU distinction makes sense structurally

- If the work is **waiting on something external** (disk, network, another server) → it can be offloaded (path 4 or 5) → call stack stays free → this is what "async" is good at.

- If the work is **pure computation** (a loop, a calculation, no external thing to wait on) → there's nothing to hand off, because nobody else is doing the waiting for you — the call stack itself has to grind through it → it blocks everything else until done.

- **I/O-bound work** = work where the *waiting* is outsourced (step 5a or 5b) and your thread is free during it. This is what the whole libuv/event-loop machine is optimized for. Thousands of concurrent I/O ops cost you almost nothing on the main thread.
- **CPU-bound work** = work where there's no "outsourcing" possible — a `for` loop crunching numbers *is* the work, it can't be handed to the OS to wait on, because nothing is being waited on, it's being computed. If you do this on the main thread, you block the one thread everything depends on. libuv's thread pool doesn't save you here either, because the thread pool is only used by Node's own built-in async APIs (fs, dns, some crypto) — your own custom CPU-heavy function never automatically goes there.

## Layer 9: Worker threads — giving yourself a second real thread

`worker_threads` lets *you* (not libuv internally) spin up an additional real OS thread, with its own V8 instance, its own event loop, its own call stack — genuinely parallel to your main thread, running on a different CPU core if available. You use this for your own CPU-bound work. Since threads normally share memory (layer 1's risk), Node sidesteps the danger by not sharing JS objects directly — you pass messages via `postMessage()` (data is copied/serialized) or explicitly opt into shared memory via `SharedArrayBuffer` when you truly need it.

## Layer 10: Child processes — a separate process entirely

`child_process` goes up a level from threads to full processes (layer 0): a completely separate memory space, separate V8 instance, can even be a non-Node program (Python script, shell command). Heavier to start than a worker thread (new process = new OS-level allocation), but fully isolated — a crash in the child can't corrupt the parent's memory.

## Layer 11: IPC — how isolated processes talk anyway

Because child processes don't share memory (that's the whole point of process isolation from layer 0), `child_process.fork()` sets up a **pipe** between parent and child — literally an OS-level communication channel. `.send()`/`.on('message')` serialize JS objects to JSON, push them through the pipe, and the other side deserializes them. It's the same fundamental idea as worker `postMessage()`, just crossing a process boundary instead of a thread boundary — because when memory isn't shared, message-passing is the only option left.

---

**The full chain, now connected end to end:**

OS has cores + a scheduler → context switching is expensive → Node avoids piling up OS threads by running your JS on **one thread** → but one thread can't block-and-wait → **libuv** intercepts async calls and offloads the *waiting* to either the OS's native async I/O or a small internal **thread pool** → completed work gets queued → the **event loop** drains that queue back onto your one JS thread, one callback at a time → this model is free for **I/O-bound** work (waiting is outsourced) but breaks for **CPU-bound** work (computing can't be outsourced, only parallelized) → for CPU-bound work you deliberately reach for **worker threads** (real parallel thread, message-passed) or **child processes** (real parallel process, IPC-connected) to get actual multi-core execution instead of relying on the illusion of concurrency the event loop provides.
