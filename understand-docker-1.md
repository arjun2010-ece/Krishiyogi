# Learn Docker

# What is docker ?

Docker is a tool for developing, shipping, and running applications. I will not go in too much detail at this point.

# Why do we need docker ?

We can develop application without docker but it primarily solves 2 major problems.

a. Allow us to work in collaborative environment (within a team)

b. Allow us to deploy docker containers with minimal configurations.

a. Allow us to work in collaborative environment

Many a times when we are installing and configuring project(nodejs, mongodb, redis) in our computer say windows/linux we face some errors and need to debug and fix it while it is working completely fine in other colleagues mac/linux setup.

It might happen because of some previously installed dependencies or something entirely new because of some Os level conflicts.

As different colleagues have different environments so this conflicts arise.

So first problem is we need to put extra effort to setup the project.

Second problem is when we install project say a team member joins after 6 months and he installs different version of project tools like: mongodb 7, node 21 or redis 7 then there is a high probability of error happening again. 

This project might not run in first try because the environment of both team members is not same.

Then we need to consult and fix those versions.

So the main problem is when we have multiple enviornments, replicating it is very difficult. This core problem is solved by DOCKER.

Docker solves this by running a standardized Linux container on top of any host OS (Windows/Mac/Linux).

b. Allow us to deploy docker containers with minimal configurations.

Even if they setup the config locally then all those local configuration they need to do on cloud(AWS, Google cloud, azure) also. And even then there is no guarrantee that node.js application will run there on first try. 

If we're using auto-scaling, we'd need to repeat this setup across all machines --- Docker avoids this by letting you build the image once and run the identical container everywhere, which is a pain without it.

In a big team or open source projects, it become very difficult to communicate everyone what changes they need to make when they face some specific problem while setup.

# How docker solves this problem ?

Docker has a concept of **containers** where we configure everything like define the OS(operating system),

specify tools like Node.js, mongodb, redis etc, copy the project inside it and install it.

And we can share it with our team or our crowd (open-source people) as we can create multiple copies of this container. This container will run on any machine on linux, windows or macos: same tool, same configuration (versions etc) everywhere, meaning replicatng the same environment everywhere.

The concept of **containers** is very powerful as they are lightweight and we can quickly create it, deploy it on cloud, destroy it and even share it with other team members.

Every container has their own OS and its own tools and its own configurations.

Thats the concept of docker.

# Docker setup

1\. Install docker desktop and it has CLI(cmd line interface) and GUI(graphical user interface) both.

So we can work with commands and see it visually in tools also.

2\. Also when we talk about docker then we have a concept of **docker daemon** which is the core tool of docker which does the whole work like spinup container, create containers, scaleup containers, destroy containers. Also pulling up the images, building the images etc.

Another is docker desktop which is the GUI which shows the current state of our machine.

3\. Check if it is installed by firing "docker" or "docker -v"

# Docker images vs docker container

- When we talk about docker, we talk about docker images and docker containers.

- For running IMAGES, we need Containers. And each Containers are isolated.

- We know that every machine has some kind of OS(operating system) running on it. Similarly "images" are like operating system and machine is like "containers" so we need containers to run images.

- We can have multiple containers running multiple images inside it and they each are isolated and can not talk with each other without port mapping. Meaning 2 computers running windows inside it have their own data and by default not sharable with each other. ALso these 2 containers have diff container IDs.

- Also, we can run the same image in multiple containers also.

Data in one container is not accessible from other containers.

- We can create containers without images also but we need to do a lot of hard stuff and it is not practical for daily software distribution.

- Normally we prefer alpine version of diff docker images which has small sizes.

- Also, there is 2 kinds of images: 

- One is base image like ubuntu, node:20 etc, postgres:alpine and

- Other is derived image or custom image.

- Meaning whenever we are building our applications IMAGE with docker then essentially we are building a Derived or Custom image. It builds on top of base image + node + node install + some commands to run app.

And we write "Dockerfile" to package our applications into a containers. Essentially docker daemon creates our apps image and then push into a container and then run it.

- Our app can have external components like mongodb(or postgres), redis or other tool and we need to write a "docker-compose.yml" file to manage these services interaction with our application container.

# Docker Commands

## Basic Docker Commands (Docker CLI)

1\. ```docker run -it ubuntu```

- It will try to pull ubuntu image(if not already present in the system) from docker hub (Docker hub is a registry of all the base images that can be used  while building complex docker setup similar to npm registry).

- ```-it``` means interactive environment meaning the moment we put this flag then the above command will pull ubuntu image if not present and RUN it in a container and then log us inside that container terminal.

- ```CTRL + D``` --> It helps comes out of the below interactive terminal.

```
juhigupta@MacBookPro ~ % docker run -it node:26

Status: Downloaded newer image for node:26

Welcome to Node.js v26.8.2.

Type ".help" for more information.

>

```

2\. docker run ubuntu

- It will only fetch the image and build it in a container but 

a. will not RUN it inside the container and 

b. it will NOT log us inside the container terminal.

c. we need to manually run it inside.

```
juhigupta@MacBookPro ~ % docker run node:22

Unable to find image 'node:22' locally

22: Pulling from library/node

1396473b793d: Download complete 

Status: Downloaded newer image for node:22

juhigupta@MacBookPro ~ %
```

* The above docker run command pulls an image and runs it in a container (if -it flag is there)

* Without -it flag, docker daemon still pulls an image and build it in a container but does not run it.

* Keep it in mind that different docker containers do not share data with each other and each docker container is an isolated environment (OS(linux) + tools like node.js etc) even from our own machine meaning our machine can not talk with a docker container unless there is a port mapping(port sharing) between our machine and specific container.

3\. ```docker container ls``` vs ```docker ps```

- Both the command will show us the current running containers on our machine. Not the stopped container.₹

4\. ```docker start <container_name> or <ID>```

- It can start the container which is stopped currently.

5\. ```docker stop <container_name> or ID```

- It can stop the container which is stopped currently.

6\. ```docker exec <container_name> ls```

- This command will execute some commands inside container WHILE staying outside the container.

- ```-it``` flag will send us inside the container terminal.

7\. ```docker exec -it <container_name> bash```

- This command will execute some commands inside container WHILE staying INSIDE the container.

- If we type further commands here like: ```ls``` or ```mkdir data-1/``` then we are typing inside the container terminal not on our machines main terminal.

9\. If we need to install node image then either we install ubuntu and then install node on it or we can directly pull node image from docker hub. This node image essentially is a linux container with node already installed on it.

- ```docker run -it node```

- This node is running inside a docker container, which is completely isolated from the node installed on our machine itself.

# How we use docker to dockerise our application

- Dockerising our app simply means building/running our app inside a docker container.

- For that we need to write a "Dockerfile"and specify different configurations.

- Please write that building/running a docker container does not mean we can talk with each other, we need to do port mapping so that our machine can talk with the docker container.

- Our app can have multiple parts also like our app, then redis, then postgres etc etc

So for allowing the communications between these different services we write a docker-compose.yml file

- Normally we prefer alpine version of diff docker images which has small sizes.

- Also, there is 2 kinds of images: 

- One is base image like ubuntu, node:20 etc, postgres:alpine and

- Other is derived image or custom image.

- Also we can even push our custom docker images to docker hub also and can share with entire teams too.

Also we can deploy this image on AWS cloud also.

- In the Dockerfile,

* The first thing we do is fetch a BASE IMAGE like nodejs image or node-alpine as our app needs node.js to work

```

FROM node

COPY package.json package.json

COPY package-lock.json package-lock.json

COPY main.js main.js

RUN npm install

ENTRYPOINT ["node", "main.js"]

```

* Copy command has <source> <destination>, source is current host app(outside container), and destination is inside docker container.

* ENTRYPOINT means whenever someone run this <container> then run this command.

* The above "Dockerfile" config now needs to be CONVERTED to a image with this command:

docker build -t youtube-nodejs .

- ```-t``` means a TAG and ```youtube-nodejs``` is the name of the image that we are building

- ```.``` means the path of IMAGE where it should generate, ```.``` means current repository.

* Now we have to run this image inside a container so we fire this command:

```docker run -it youtube-nodejs```

It will run the container but if we try to access this node.js from browser or postman app then it will not work as we have not done port mapping.

So for full access, we do this:

```docker run -it -p 8000:8000 youtube-nodejs```

Now it will work from browser or postman on port 8000.

## How caching works with docker

- Suppose in the above main.js file we did not change anything so next time we try to run the container it willbe very fase as caching is working here.

- But if we make some changes in main.js file then the steps or commands above this line in dockerfile is cached and will not execute, only line from below will be re-built and will take time for these only:

```

COPY main.js main.js

RUN npm install

ENTRYPOINT ["node", "main.js"]

```

So the ordering of the commands is very important. And these are called layer caching. 

And each step is like a layer.

# How these multiple containers work internally (talk to each other)

- Suppose we are running node.js application inside a container. But since node.js is a server so it will run on some port for ex, 8000 but this port is inside the container. If we try to talk with it from outside, like browser as "http://localhost:8000" then it will not work because that port is running inside a container, and we need to expose it for it to be able to talk from browser or postman.

It is also called PORT MAPPING.

- command looks like this:

```docker run -it -p 1025:1025 node```

- ```-p``` flag means PORT MAPPING and 1025:1025 is the mapping between host machine port to container port. ```<HOST_MACHINE PORT> : < CONTAINER PORT>```

- After doing this we can access this image from browser or postman like :

```http://localhost:1025```

- This is how we pass environment variables inside docker container from outside shell:

```docker run -it -p 1025:1025 -e key1=value1 -e key2=value2 node```

* ```-e```  flag followed by ```key=value``` is the way to pass environment variables.

# Docker compose

- For a real world app, we might install mutiple containers with individual ports like 

* nodejs app, port:4000

* postgres, port:6000

* Redis, port 4567

* Mailhog, port 2345

And we need to individually RUN each containers with 3/4 different commands but that is not a good approach.

And we have a solution called "docker compose".

With this, we can setup, create and destroy multiple containers including our nodejs app container(created using Dockerfile), postgres container, redis container etc.

- We write a ```docker-compose.yml``` file like this:

```

version: "3.8"

services:

  app:

    build: .    # "build a custom image using the Dockerfile in this folder"

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

And we can run all the services defined in above config file with this command:

* ```docker compose up```

So, with one command we have SETUP our entire INFRASTRUCTURE.

* ```docker compose down```

  - it will close above running services.

# Why we need both Dockerfile and docker-compose.yml file ?

Yes --- and here's why both exist together, connecting to what we already covered:

**Dockerfile = "how do I build *my* custom image."** Only needed for the images nobody has already built for you --- your Node app, basically, since it depends on your specific code and dependencies.

**docker-compose.yml = "which containers do I run, and how do they connect."** For each service, compose needs to know where its image comes from. It has two options:

```yaml

services:

  app:

    build: .          # "build a custom image using the Dockerfile in this folder"

    ports:

      - "3000:3000"

  mongo:

    image: mongo:7     # "just pull this ready-made image, no build needed"

  redis:

    image: redis:7      # same --- no Dockerfile needed for this either

```

Notice the difference: `app` has `build: .` because *you* need to define what goes into it (that's what your Dockerfile is for). `mongo` and `redis` just use `image:` because they're already fully-built images sitting on Docker Hub --- nobody needs to write a Dockerfile for Mongo, MongoDB's own team already did that.

**So the rule of thumb:** if a service is *your custom code*, you need a Dockerfile to define its image, and compose references that Dockerfile via `build:`. If a service is *off-the-shelf software* (Mongo, Redis, Postgres, Nginx), you skip the Dockerfile entirely and compose just pulls the `image:` directly.

That's the full connection: Dockerfile builds one image. Compose orchestrates many containers --- some built from your Dockerfile, some pulled ready-made --- and wires them together on a shared network, as we talked about earlier.

