# Difference Between Docker's CMD and ENTRYPOINT

We have a Node project with 2 files:

**index.js**
```js
console.log("Hello, World!- From CMD");
```

**main.js**
```js
console.log("Hello, World!- From ENTRYPOINT");
```

---

## Case 1: CMD Usage

My Dockerfile looks like this:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
CMD ["node", "index.js"]
```

Here I'm using `CMD` as the main command to run the main server or script.

I build this image as:

```bash
docker build -t node-test:v1 .
```

### Now the Real Test Is Visible Here

When we run this command to run the container:

```bash
docker run node-test:v1
```

I get:

```
Hello, World!- From CMD
```

If I pass an additional argument to the above `docker run`:

```bash
docker run node-test:v1 main.js
# We also have a main.js file in the project
```

I get:

```js
console.log("Hello, World!- From ENTRYPOINT");
```

So if in the Dockerfile we provide commands using `CMD`, it can be overwritten by the `docker run` command when we pass an additional argument.

Also, if we fire this command instead:

```bash
docker run node-test:v1 sh
```

It goes inside the container as:

```
/app #
```

So if our goal is to be able to verify things inside the container, use `CMD`.

---

## Case 2: ENTRYPOINT Usage

My Dockerfile looks like this:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
ENTRYPOINT ["node", "index.js"]
```

Here I'm using `ENTRYPOINT` as the main command to run the main server or script.

I build this image as:

```bash
docker build -t node-test:v2 .
```

### Now the Real Test Is Visible Here

When we run this command to run the container:

```bash
docker run node-test:v2
```

I get:

```
Hello, World!- From CMD
```

If I pass an additional argument to the above `docker run`:

```bash
docker run node-test:v2 main.js
# We also have a main.js file in the project
```

I get:

```
Hello, World!- From CMD
```

So if in the Dockerfile we provide commands using `ENTRYPOINT`, the extra argument is not used to overwrite the command, but is appended to it:

```
node index.js main.js
```

But since Node always executes the first script, we can verify that the second script gets appended by updating our `index.js`:

**index.js**
```js
console.log("Hello, World!- From CMD");
console.log("Arguments:", process.argv);
```

So the above `docker run` gets me:

```
Hello, World!- From CMD
Arguments: [ '/usr/local/bin/node', '/app/index.js', 'main.js' ]
```

This confirms that `main.js` gets appended.

If we fire this command instead:

```bash
docker run node-test:v2 sh
```

It effectively becomes:

```
node index.js sh
```

So Docker does not launch `sh` (shell). It starts `index.js`, passing `"sh"` as an argument:

```js
process.argv
// ["/usr/local/bin/node", "/app/index.js", "sh"]
```

So if you want to run the shell to verify something, you need to use `CMD`.

---

## Case 3: ENTRYPOINT & CMD Usage

`CMD` becomes the default arguments to `ENTRYPOINT`, and can be overridden at runtime.

**Dockerfile:**

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
ENTRYPOINT ["node", "index.js"]
CMD ["--port", "3000"]
```

**Build:**

```bash
docker build -t node-test:v3 .
```

**Run:**

```bash
docker run -it node-test:v3
```

```
Hello, World!- From CMD
Arguments: [ '/usr/local/bin/node', '/app/index.js', '--port', '3000' ]
```

If we fire:

```bash
docker run -it node-test:v3 --port 4000
```

...it gives us:

```
Hello, World!- From CMD
Arguments: [ '/usr/local/bin/node', '/app/index.js', '--port', '4000' ]
```

So it replaces the default `CMD` arguments.

---

## When to Use CMD

Use `CMD` when the command is a sensible default but you expect it may change:

```dockerfile
CMD ["node", "index.js"]
```

Then:

```bash
docker run node-test:v2
# runs: node index.js

docker run -it node-test:v2 sh
# runs: sh shell instead
```

## When to Use ENTRYPOINT

Use `ENTRYPOINT` when the command is fixed (and will not change), and any command-line values passed at runtime should either not exist, or if they do exist, they act only as arguments to the defined `ENTRYPOINT` command.

Then:

```bash
docker run node-test:v2 --port 3000
# runs: node index.js --port 3000
```

You can still deliberately replace the fixed command when needed:

```bash
docker run --entrypoint sh -it node-test:v2
```

But that is an explicit override.

To inspect any container — whether it uses `CMD` or `ENTRYPOINT` — you can override the entrypoint:

```bash
docker run --rm -it --entrypoint sh node-test:v2
```

A common production pattern combines both:

```dockerfile
ENTRYPOINT ["node", "index.js"]
CMD ["--port", "3000"]
```
