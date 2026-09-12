# Learn Docker

## What is Docker?

Docker is a tool for developing, shipping, and running applications. I will not go into too much detail at this point.

## Why do we need Docker?

We can develop applications without Docker, but it primarily solves 2 major problems:

1. **Collaborative environment** — allows us to work in a team without environment conflicts.
2. **Deployment with minimal configuration** — allows us to deploy Docker containers with minimal configurations.

### 1. Collaborative environment (within a team)

Many times, when we are installing and configuring a project (Node.js, MongoDB, Redis) on our computer — say Windows/Linux — we face some errors and need to debug and fix them, while it works completely fine on other colleagues' Mac/Linux setups.

This might happen because of some previously installed dependencies, or something entirely new because of OS-level conflicts. As different colleagues have different environments, these conflicts arise.

So the **first problem** is that we need to put in extra effort to set up the project.

The **second problem** is version drift: say a team member joins after 6 months and installs different versions of the project tools — like MongoDB 7, Node 21, or Redis 7. Then there is a high probability of errors happening again. The project might not run on the first try because the environments of the two team members are not the same. Then we need to consult and fix those versions.

So the main problem is: **when we have multiple environments, replicating them is very difficult.** This core problem is solved by Docker.

Docker solves this by running a standardized Linux container on top of any host OS (Windows/Mac/Linux).

### 2. Deployment with minimal configurations

Even if the team sets up the config locally, all those local configurations also need to be done on the cloud (AWS, Google Cloud, Azure). And even then, there is no guarantee that the Node.js application will run there on the first try.

If we're using auto-scaling, we'd need to repeat this setup across all machines — Docker avoids this by letting you build the image once and run the identical container everywhere, which is a pain without it.

In a big team or open-source projects, it becomes very difficult to communicate to everyone what changes they need to make when they face some specific problem during setup.

## How Docker solves this problem

Docker has a concept of **containers**, where we configure everything: define the OS (operating system), specify tools like Node.js, MongoDB, Redis, etc., copy the project inside it and install it.

We can share it with our team or our crowd (open-source people) since we can create multiple copies of this container. This container will run on any machine — Linux, Windows, or macOS — with the same tools and the same configuration (versions etc.) everywhere, meaning we replicate the same environment everywhere.

The concept of **containers** is very powerful: they are lightweight, and we can quickly create them, deploy them on the cloud, destroy them, and even share them with other team members.

Every container has its own OS, its own tools, and its own configurations. That's the concept of Docker.

## Docker setup

1. Install **Docker Desktop**. It has both a CLI (command-line interface) and a GUI (graphical user interface), so we can work with commands and also see things visually in the tool.

2. When we talk about Docker, we have the concept of the **Docker daemon**, which is the core tool of Docker that does all the work — spinning up containers, creating containers, scaling up containers, destroying containers, pulling images, building images, etc. Docker Desktop is the GUI that shows the current state of our machine.

3. Check if it is installed by running `docker` or `docker -v`.

## Docker images vs Docker containers

- When we talk about Docker, we talk about Docker **images** and Docker **containers**.
- To run images, we need containers. Each container is isolated.
- Every machine has some kind of OS running on it. Similarly, "images" are like the operating system and the "container" is like the machine — so we need containers to run images.
- We can have multiple containers running multiple images inside them. Each one is isolated and cannot talk to the others without port mapping — meaning 2 computers running Windows inside them have their own data and, by default, it is not shareable between them. Also, these 2 containers have different container IDs.
- We can run the same image in multiple containers as well.
- Data in one container is not accessible from other containers.
- We can create containers without images, but we'd have to do a lot of hard work, and it is not practical for daily software distribution.
- Normally we prefer the **alpine** version of different Docker images, which have small sizes.
- There are 2 kinds of images:
  - **Base images** — like `ubuntu`, `node:20`, `postgres:alpine`.
  - **Derived (custom) images** — whenever we build our application's image with Docker, we are essentially building a derived/custom image. It builds on top of a base image + Node install + some commands to run the app.
- We write a **Dockerfile** to package our application into a container. Essentially, the Docker daemon creates our app's image, then pushes it into a container and runs it.
- Our app can have external components like MongoDB (or Postgres), Redis, or other tools. To manage how these services interact with our application container, we write a **docker-compose.yml** file.

## Docker commands

### Basic Docker commands (Docker CLI)

#### 1. `docker run -it ubuntu`

- It will try to pull the `ubuntu` image (if not already present in the system) from **Docker Hub**. Docker Hub is a registry of all the base images that can be used while building complex Docker setups — similar to the npm registry.
- `-it` means **interactive environment**: the moment we add this flag, the above command will pull the Ubuntu image (if not present), run it in a container, and log us inside that container's terminal.
- `CTRL + D` — helps us come out of the interactive terminal.

```bash
juhigupta@MacBookPro ~ % docker run -it node:26

Status: Downloaded newer image for node:26

Welcome to Node.js v26.8.2.

Type ".help" for more information.

>
```

#### 2. `docker run ubuntu`

It will fetch the image and build it into a container, but:

- it will **not** run it inside the container, and
- it will **not** log us inside the container terminal — we need to manually run it inside.

```bash
juhigupta@MacBookPro ~ % docker run node:22

Unable to find image 'node:22' locally

22: Pulling from library/node

1396473b793d: Download complete

Status: Downloaded newer image for node:22

juhigupta@MacBookPro ~ %
```

To summarise:

- The `docker run` command pulls an image and runs it in a container (if the `-it` flag is there).
- Without the `-it` flag, the Docker daemon still pulls the image and builds it into a container but does not run it.
- Keep in mind that different Docker containers do not share data with each other, and each Docker container is an isolated environment (OS (Linux) + tools like Node.js, etc.) — even from our own machine. Our machine cannot talk to a Docker container unless there is a port mapping (port sharing) between our machine and the specific container.

#### 3. `docker container ls` vs `docker ps`

- Both commands show us the currently running containers on our machine — not stopped containers.

#### 4. `docker start <container_name_or_ID>`

- It can start a container that is currently stopped.

#### 5. `docker stop <container_name_or_ID>`

- It can stop a currently running container.

#### 6. `docker exec <container_name> ls`

- This command executes some command inside the container **while staying outside** the container.
- The `-it` flag sends us inside the container terminal.

#### 7. `docker exec -it <container_name> bash`

- This command executes commands inside the container **while staying inside** it.
- If we type further commands here — like `ls` or `mkdir data-1/` — we are typing inside the container terminal, not on our machine's main terminal.

#### 8. Pulling Node directly

If we need a Node image, we can either install Ubuntu and then install Node on it, or we can directly pull the `node` image from Docker Hub. This Node image is essentially a Linux container with Node already installed on it.

- `docker run -it node`
- This Node is running inside a Docker container, which is completely isolated from the Node installed on our machine itself.

## How we use Docker to dockerise our application

- Dockerising our app simply means building/running our app inside a Docker container.
- For that, we need to write a **Dockerfile** and specify different configurations.
- Please note that building/running a Docker container does not mean we can talk with it — we need to do port mapping so that our machine can talk to the Docker container.
- Our app can have multiple parts — our app, then Redis, then Postgres, etc. To allow communication between these different services, we write a `docker-compose.yml` file.
- We can even push our custom Docker images to Docker Hub and share them with entire teams. We can also deploy this image on AWS cloud.

In the Dockerfile, the first thing we do is fetch a **base image** — like the Node.js image or `node:alpine` — as our app needs Node.js to work:

```dockerfile
FROM node

COPY package.json package.json
COPY package-lock.json package-lock.json
COPY main.js main.js

RUN npm install

ENTRYPOINT ["node", "main.js"]
```

- The `COPY` command takes `<source> <destination>`: the source is the current host app (outside the container), and the destination is inside the Docker container.
- `ENTRYPOINT` means: whenever someone runs this container, run this command.

Now this Dockerfile config needs to be **converted to an image** with this command:

```bash
docker build -t youtube-nodejs .
```

- `-t` means a **tag** — `youtube-nodejs` is the name of the image we are building.
- `.` means the path where the image should be generated — `.` means the current repository.

Now we run this image inside a container:

```bash
docker run -it youtube-nodejs
```

It will run the container, but if we try to access this Node.js app from the browser or Postman, it will not work — we haven't done port mapping. For full access, we do this:

```bash
docker run -it -p 8000:8000 youtube-nodejs
```

Now it will work from the browser or Postman on port 8000.

### How caching works with Docker

- Suppose in the above `main.js` file we did not change anything. The next time we try to run the container, it will be very fast because caching is working here.
- But if we make some changes in `main.js`, then the steps/commands **above** that line in the Dockerfile are cached and will not re-execute — only the lines from there down will be rebuilt:

```dockerfile
COPY main.js main.js

RUN npm install

ENTRYPOINT ["node", "main.js"]
```

So the **ordering of the commands is very important**. This is called **layer caching** — each step is like a layer.

## How multiple containers work internally (talk to each other)

- Suppose we are running a Node.js application inside a container. Since Node.js is a server, it will run on some port — for example, 8000 — but this port is **inside the container**. If we try to talk to it from outside, like a browser at `http://localhost:8000`, it will not work, because that port is running inside a container. We need to **expose** it to be able to talk to it from the browser or Postman. This is also called **PORT MAPPING**.
- The command looks like this:

```bash
docker run -it -p 1025:1025 node
```

- The `-p` flag means PORT MAPPING, and `1025:1025` is the mapping between the host machine port and the container port: `<HOST_MACHINE_PORT>:<CONTAINER_PORT>`.
- After doing this, we can access it from the browser or Postman at `http://localhost:1025`.
- This is how we pass environment variables into a Docker container from the outside shell:

```bash
docker run -it -p 1025:1025 -e key1=value1 -e key2=value2 node
```

- The `-e` flag followed by `key=value` is how we pass environment variables.

## Docker Compose

- For a real-world app, we might run multiple containers with individual ports, like:
  - Node.js app — port 4000
  - Postgres — port 6000
  - Redis — port 4567
  - Mailhog — port 2345
- We would need to individually run each container with 3–4 different commands, but that is not a good approach.
- The solution is **Docker Compose**. With it, we can set up, create, and destroy multiple containers — including our Node.js app container (created using a Dockerfile), a Postgres container, a Redis container, etc.
- We write a `docker-compose.yml` file like this:

```yaml
version: "3.8"

services:
  app:
    build: . # "build a custom image using the Dockerfile in this folder"
    ports:
      - "3000:3000"

  postgres:
    image: postgres # hub.docker.com
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_DB: review
      POSTGRES_PASSWORD: password

  redis:
    image: redis
    ports:
      - "6379:6379"
```

We can run all the services defined in the above config file with this command:

```bash
docker compose up
```

With one command, we have set up our entire infrastructure.

```bash
docker compose down
```

This will stop the running services.

### Monorepo projects

If we have a monorepo project — like `apps/app` containing the frontend project and `apps/api` containing the backend project — we can write a Dockerfile for both frontend and backend in their respective folders:

- Frontend: `apps/app/Dockerfile.frontend` (or simply `apps/app/Dockerfile`)
- Backend: `apps/api/Dockerfile.backend` (or simply `apps/api/Dockerfile`)

Remember to give the path in the `docker-compose.yml` file like below:

```yaml
services:
  api:
    image: jobboard/api:1.0.0
    build:
      context: .
      dockerfile: apps/api/Dockerfile # file path — backend
    ports:
      - "3001:3001"

  web:
    image: jobboard/web:1.0.0
    build:
      context: .
      dockerfile: apps/web/Dockerfile # file path — frontend
    ports:
      - "3000:3000"
    depends_on:
      - api
```

## Why we need both a Dockerfile and a docker-compose.yml

Both exist together, connecting to what we already covered:

**Dockerfile = "How do I build *my* custom image?"** Only needed for the images nobody has already built for you — your Node app, basically, since it depends on your specific code and dependencies.

**docker-compose.yml = "Which containers do I run, and how do they connect?"** For each service, Compose needs to know where its image comes from. It has two options:

```yaml
services:
  app:
    build: . # "build a custom image using the Dockerfile in this folder"
    ports:
      - "3000:3000"

  mongo:
    image: mongo:7 # "just pull this ready-made image, no build needed"

  redis:
    image: redis:7 # same — no Dockerfile needed for this either
```

Notice the difference: `app` has `build: .` because *you* need to define what goes into it (that's what your Dockerfile is for). `mongo` and `redis` just use `image:` because they're already fully-built images sitting on Docker Hub — nobody needs to write a Dockerfile for Mongo; MongoDB's own team already did that.

**So the rule of thumb:** if a service is *your custom code*, you need a Dockerfile to define its image, and Compose references that Dockerfile via `build:`. If a service is *off-the-shelf software* (Mongo, Redis, Postgres, Nginx), you skip the Dockerfile entirely and Compose just pulls the `image:` directly.

That's the full connection: the Dockerfile builds one image. Compose orchestrates many containers — some built from your Dockerfile, some pulled ready-made — and wires them together on a shared network, as we talked about earlier.
