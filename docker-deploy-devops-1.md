# DevOps Project Notes — AWS, Docker, Kubernetes Setup

## AWS IAM User

**devops-user**
```
devops-learning1#
```

**Root user**
```
arjun.feup@gmail.com / SpaceshiP1#
```

### Console Sign-in Details (Shared with Team Member)

Console sign-in URL:
```
https://078145931846.signin.aws.amazon.com/console
```

User name:
```
devops-user
```

Console password:
```
devops-learning1#
```

---

## Step 1: Launch an EC2 Instance

An EC2 instance is essentially a server (a server is essentially a computer with its own OS, like Linux, Windows, macOS, RedHat, RAM, etc.).

Remember, the more RAM we have on the EC2 instance, the more tools we can install on it, like Docker, kubectl, eksctl, Terraform, Helm, etc. So make sure to increase the RAM while launching the instance itself.

This project is set up with more than 20 microservices, so a free-tier instance with limited resources cannot run this project. This means 8GB of storage is not enough — it has to be 30GB minimum (needs to be verified).

**Note:**
- `kubectl` is the official command-line tool to communicate with a Kubernetes API server (the Kubernetes cluster's control plane) and manage cluster resources.
- `eksctl` is the command-line tool that automates and simplifies the creation, management, and operation of Kubernetes clusters on Amazon Elastic Kubernetes Service (EKS).

Choose an instance type that provides at least 2 vCPUs and 8GB RAM.

Whenever we need to connect to secure services like EC2, we can do so with private/public keys, so we need to generate a key pair while launching the EC2 instance itself.

A `.pem` file is used to store and transfer cryptographic keys, digital certificates, and certificate chains. It can be used with the OpenSSH tool.

### Other Concepts

OpenSSH is a tool used for secure remote login, system administration, and file transfers over untrusted networks.

- **SSH** — means Secure Shell
- **OpenSSH** — open-source implementation of SSH

### Command to Connect to the EC2 Instance via Terminal (using SSH)

```bash
ssh -i devops-demo.pem ubuntu@51.20.70.121
```

- `devops-demo.pem` is the private key file downloaded while creating the EC2 instance.
- `ubuntu` is the operating system selected while creating the instance.
- `51.20.70.121` is the public IP address (public IPv4 address) generated when the instance is created, viewable in its details.

The above command will fail initially because the `devops-demo.pem` file needs the appropriate permissions, so we do this:

```bash
cd Downloads/
chmod 400 devops-demo.pem   # Either give 400 or 600 permission.
ssh -i devops-demo.pem ubuntu@51.20.70.121
```

Now we're connected to the EC2 instance from the terminal.

```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

### Step 2: Install Docker Engine

Install Docker Engine for Linux from the official site (not Docker Desktop).

### Step 3: Install kubectl

Install kubectl for Linux from the official site.

### Step 4: Install Terraform

Install Terraform for Linux from the official site.

Terraform version installed: `1.16.3`

### Step 5: Clone and Run the Project

Clone the repo inside the instance and run `docker compose up`. If a memory issue arises, it means memory is not enough.

We need to resize the volume and resize the file system too.

**a. Resize the volume:**

Go to the instance details → Storage tab → select volume (from block devices) → Modify volume (from Actions dropdown) → change size to 30GB (from 8GB).

Wait 5–6 minutes for the "Volume state (In-use)" to turn green from greyed out.

**b. Resize the file system (in the instance terminal):**

Check how much of the `/dev/root` file system mounted on `/` is used, and its size:

```bash
df -h   # currently 99% used, size 6.7G, no change in file system yet
```

Check the blocks:

```bash
lsblk
```

```
NAME         MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
loop0          7:0    0 28.2M  1 loop /snap/amazon-ssm-agent/13009
loop1          7:1    0   74M  1 loop /snap/core22/2411
nvme0n1      259:0    0   30G  0 disk 
├─nvme0n1p1  259:1    0  6.9G  0 part /   ### This is what we want to increase in size
├─nvme0n1p13 259:2    0 1023M  0 part /boot
├─nvme0n1p14 259:3    0    4M  0 part 
└─nvme0n1p15 259:4    0  106M  0 part /boot/efi
```

This shows `nvme0n1` has a 30GB size, which is the volume we set from the EC2 instance, so that's good. But just below it, `nvme0n1p1` has 6.9GB and is mounted on `/`, so this size has not increased. We need to grow this partition of the file system to as close to 30GB as possible.

For that, we need to install `cloud-guest-utils`:

```bash
sudo apt install cloud-guest-utils
# It already exists.
```

Now run this command to increase the partition size:

```bash
sudo growpart /dev/nvme0n1 1
```

Note: `nvme0n1` is the partition name/ID, then a space, then `1`, meaning the first partition itself. This will increase the partition size.

Now check again:

```bash
lsblk
```

It will now show `nvme0n1p1` has 28.9GB, so its size has increased:

```
NAME         MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
loop0          7:0    0 28.2M  1 loop /snap/amazon-ssm-agent/13009
loop1          7:1    0   74M  1 loop /snap/core22/2411
nvme0n1      259:0    0   30G  0 disk 
├─nvme0n1p1  259:1    0 28.9G  0 part /   <---- This fs increased in size.
├─nvme0n1p13 259:2    0 1023M  0 part /boot
```

Update the file system:

```bash
sudo resize2fs /dev/nvme0n1p1
```

This will update the file system disk size to 30GB.

Verify the size increased:

```bash
df -h   # it will now show "/dev/root" has size 28GB
```

Now run:

```bash
docker compose up -d
```

All the containers that were stopped because of low memory are suddenly working.

### Step 6: Access the Web Store

From the official documentation ([opentelemetry.io docs](https://opentelemetry.io/docs/demo/docker-deployment/#verify-the-web-store-and-telemetry)):

Web store: `http://localhost:8080/`

This means the project is available on port `8080`. Since we already installed this project on the EC2 instance and already started Docker in the previous step, we now need to copy the public IPv4 address and access it in HTTP mode, adding the `8080` port:

```
http://51.20.70.121:8080/
```

It will not work, because by default, when we create an EC2 instance, there is a security group attached to the instance that acts as a firewall and does not allow any inbound traffic. The default behavior of this security group is to block any incoming requests.

But why can SSH connect to this EC2 instance? Because when we created this EC2 instance, its security group's inbound rules allowed port 22, and port 22 is the port for SSH.

Therefore, the security group and inbound rules are very important for an instance, as they control which ports/requests can interact with the EC2 instance. Because of this, port `8080` is blocked, as it is not allowed in the inbound rules of the security group.

Incoming traffic is called **ingress**.

- On the AWS EC2 instance, click the "Security" tab.
- Under "Inbound rules," scroll right on the first item and click the security group link. This opens another page.
- Click the "Security group ID" value, then click "Edit inbound rules." Here you'll see that port 22 is defined for SSH, as discussed.
- Click "Add rule." From the Type dropdown, select "All traffic" for now. For Source, select "Anywhere," "IPv4," "IPv6," or a custom IP address. We select "IPv4" for now, and save the rules.

Now the link `http://51.20.70.121:8080/` will work on reload, since we've defined the inbound rule in the security group.

---

## How DevOps Teams Work Within a Company

A company or large product can have around 20 microservices, divided among different development teams. For example, one dev team might work on Payment, Checkout & flagd services, while another works on 1–2 services each. This is how microservices are split among an organization's dev teams.

As a DevOps engineer, you will most likely work with 1–2 dev teams, meaning 4–6 microservices. At a startup, this number can be higher. In any case, you will not typically work with every microservice in the organization unless the application is very simple.

### What Does a DevOps Engineer Do With These Microservices?

The first thing they do is containerize the microservices using Docker, so understanding the Docker lifecycle is very important.

The typical Docker lifecycle occurs in 3 stages. If we're given the Payment microservice to containerize, we implement it in 3 stages:

a. Set up the Dockerfile.
b. Create the Docker image — via the `docker build` command.
c. Create and run the Docker container — via the `docker run` command.

This is where the dev team and DevOps engineer collaborate to create the Dockerfile. Some information is required, such as how the developer builds the application, and this info is shared with the DevOps engineer via docs, a `readme.md` file per service, or a Confluence page describing how to build the application, required environment variables, and any additional steps.

If the developer doesn't share this info, we have to work with them to request it — e.g., "I'm writing the Dockerfile for this service and I need some information for it."

### How Do We Start Containerizing a Service/Project?

Do we jump straight into writing the Dockerfile? Definitely not. First, we go to the project/microservice repository root, then to `src/services` (the independent microservice/project), and check its individual readme file.

Check `product-catalog` from this link: [ultimate-devops-project-demo/src/product-catalog](https://github.com/iam-veeramalla/ultimate-devops-project-demo/tree/main/src/product-catalog), and check its individual readme file.

In an organization, not all microservices are in a single repo — a group of microservices may be in one repo, some in others, and a single microservice can also have its own repo.

Next, go to the project and:

```bash
cd src
cd product-catalog
```

Reading the readme file, it says:

**Local Build** — To build the service binary, run:

```bash
export PRODUCT_CATALOG_PORT=<any-unique-port>
go build -o product-catalog .
```

Then run:

```bash
export PRODUCT_CATALOG_PORT=8088
go build -o product-catalog .   # generates the output binary named "product-catalog"
```

Next:

```bash
ls -ltr   # shows a "product-catalog" output binary file in the current microservice folder
```

Run the output binary:

```bash
./product-catalog
```

Output:

```
INFO[0000] Loaded 10 products
INFO[0000] Product Catalog gRPC server started on port: 8088
```

**What we've learned so far:**
- We learned to build a Go binary locally on our machine (via the EC2 instance, but it's just like doing it locally).
- Next, we'll start on the Docker lifecycle: creating the Dockerfile, creating the Docker image, and creating/running the Docker container.

We'll delete the existing Dockerfile present in [this path](https://github.com/iam-veeramalla/ultimate-devops-project-demo/tree/main/src/product-catalog) so we can create it ourselves:

```bash
rm -rf Dockerfile
```

---

## Containerization of First Microservice (Product Catalog — Golang)

We need a base image of Golang:

```dockerfile
FROM golang:1.22-alpine AS builder
```

We'll also write a multi-stage Docker build — the first stage is `builder`, the second is `runner`. It's better DevOps practice to create a multi-stage Docker build and only copy the binary into the next stage.

Next, it's good practice to select a work directory, so we know where our commands are being executed. This acts as the directory for the Dockerfile and Docker command execution:

```dockerfile
WORKDIR /usr/src/app
```

(Equivalent to `mkdir /usr/src/app && cd /usr/src/app`.)

Next, we need to do something like `npm install` for JS, but in Go we have a dependency file, `go.mod`, and we can install it with:

```bash
go mod download
```

We'll also run a build command to create the binary file:

```bash
go build -o <build_file_name> .
```

`.` means the entire source code in the above command. `<build_file_name>` is the name we want to give the built file.

So we place these commands in the Dockerfile:

```dockerfile
RUN go mod download
RUN go build -o product-catalog ./
```

We'll put built files in the `/go/bin` directory, as it's normally where binaries are placed. We can choose any other directory, but sometimes that directory may not exist, so it's better to use the same name as the service, e.g., `product-catalog`. `./` means the source code.

The above commands won't work yet, because we need to copy the source code into the Docker image too, with this command placed just after the work directory setting:

```dockerfile
COPY . .
```

We need to copy everything from the local directory into the Docker directory and then run commands inside it for things to work correctly.

Normally, for a single-build approach, we'd write an `ENTRYPOINT`/`CMD` to run the binary above and finish the Dockerfile. But since this is a multi-stage build, we'll create a new stage here and take something from the previous stage.

### Understanding Multi-Stage Builds in Detail

The first stage handles binary creation. While this can involve up to 10 stages in complex setups, we'll look at a simplified two-stage version here.

We create binaries by downloading all the files and dependencies — you might use the root user here, and do anything else you want.

In the last stage of the Docker build, we'll use a distroless image, a scratch image, or a minimal base image with very few binaries, making it lightweight with almost zero unwanted binaries. In Linux, reducing unwanted binaries or shared libraries significantly reduces the chance of vulnerabilities.

That's why, in the last stage of a multi-stage Docker build, we use a very lightweight image with only the basic system dependencies (no application dependencies), copy in the binaries created in the previous stage, and just execute that binary. No build is performed in this stage — this is the stage that runs as a container. Everything from stage 1 is removed except the copied binaries, which is why the final Docker image size is reduced.

Next, for the second stage of the multi-stage build, we choose the `alpine` image, which is very lightweight:

```dockerfile
FROM alpine AS release

WORKDIR /usr/src/app
```

(Also choose a work directory in the second stage, as good practice.)

We'll also copy the binaries generated in the previous stage into this stage:

```dockerfile
COPY --from=builder /usr/src/app/product-catalog ./
```

This copies the binary from the builder image's location (`/usr/src/app/product-catalog`) and pastes it into the current work directory location (`/usr/src/app`, represented here as `./`).

Since `product-catalog` is where the binary is built, and it's inside stage 1's `/usr/src/app` directory, when copying from that builder stage we reference the full path as `/usr/src/app/product-catalog`.

We'll expose the port, as we did when running the app locally:

```dockerfile
EXPOSE ${PRODUCT_CATALOG_PORT}
```

And run the final command to start the server:

```dockerfile
ENTRYPOINT ["./product-catalog"]
```

The service's readme file states that when this service runs, the output should look like:

```
INFO[0000] Loaded 10 products
INFO[0000] Product Catalog gRPC server started on port: 8088
```

The "10 products" comes from the `products/products.json` file, so we'll copy this file too, just after the work directory setting:

```dockerfile
COPY ./products ./products
```

Now we run this Dockerfile to see if it works as expected, via the `docker build` command:

```bash
docker build -t abhishekf5/product-catalog:v1 .
```

- `abhishekf5` — Docker Hub username
- `product-catalog` — the service name we're trying to build
- `v1` — version 1 of that tag
- `.` — current directory of the Dockerfile we're trying to build

**The Docker image builds successfully.**

We check it with:

```bash
docker images                       # lists all images
docker images | grep abhishek       # lists only images with "abhishek" in the tag
```

### Docker Lifecycle: Running the Image

We've created the Dockerfile and the Docker image. Now we need to run this image as a container:

```bash
docker run abhishekf5/product-catalog:v1
```

This will error, since we haven't set the `PRODUCT_CATALOG_PORT` environment variable:

```
time="2026-09-20T10:46:24Z" level=info msg="Loaded 10 products"
time="2026-09-20T10:46:24Z" level=fatal msg="Environment Variable Not Set: \"PRODUCT_CATALOG_PORT\""
```

We fix this by editing the Dockerfile and adding the environment variable:

```dockerfile
ENV PRODUCT_CATALOG_PORT 8088
EXPOSE ${PRODUCT_CATALOG_PORT}
```

Then rebuild the image with a different version tag, so as not to use any caching from the previous image:

```bash
docker build -t abhishekf5/product-catalog:v2 .
```

Then run it:

```bash
docker run abhishekf5/product-catalog:v2
```

Output:

```
time="2026-09-20T10:59:07Z" level=info msg="Loaded 10 products"
time="2026-09-20T10:59:07Z" level=info msg="Product Catalog gRPC server started on port: 8088"
```

Everything worked out perfectly, matching the documentation/readme file.

**The `product-catalog` service is containerized successfully.**

---

## Containerization of Another Microservice (Ad Service — Java)

We now use a Java-based microservice: the Ad service.

Move to the current directory inside `src`:

```bash
cd src/ad   # https://github.com/iam-veeramalla/ultimate-devops-project-demo/tree/main/src/ad
```

Check the readme file for this microservice on how to run it locally. Every developer should provide instructions on how to run the application locally before containerizing it.

The prerequisite for containerizing / implementing the Docker lifecycle is learning to build the application locally first — this makes it much easier to write the Dockerfile. Do not jump into writing the Dockerfile before taking this approach.

Reading the readme file, we understand this Java application is built using Gradle. Java applications are typically built using either Maven or Gradle:

```
Java ----> Gradle
 |
 |------> Maven
```

In the repo, there's an important file, `gradlew` — the Gradle wrapper. This script typically starts the Gradle daemon (server), which:

- downloads the dependencies
- compiles the program
- builds the application

We need to execute this Gradle wrapper.

First, since it's a Java project, check if Java is installed:

```bash
java --version
```

If not present, install it:

```bash
sudo apt install openjdk-21-jre-headless
```

JDK 21 was chosen because the documentation says at least JDK 17 is required, and a higher version wasn't preferred either. As a DevOps engineer, you should go through the documentation of each service you work with.

```bash
./gradlew   # check if we have permission to run this wrapper file
```

We currently have permission.

Sometimes, when a project has just been cloned, we may not have permission — in that case:

```bash
chmod +x ./gradlew   # grant execute permission
./gradlew             # execute the wrapper file
```

```bash
./gradlew installDist
```

This command does several things:
- Starts the Gradle daemon
- Installs dependencies
- Compiles the code
- Builds the application

The built application is saved in a particular directory, provided by the developer:

```
./build/install/opentelemetry-demo-ad/bin/Ad
```

In the previous Go application, we wrote the build command as:

```bash
go build -o <Build directory> .
```

Here, `./gradlew installDist` already builds the application too, which we can see with:

```bash
ls -lr
```

This displays the `/build` folder, and within it, the executables:

```bash
ls -lr ./build/install/opentelemetry-demo-ad/bin/Ad
```

(`Ad` is the executable file that runs the application for us.)

```bash
export AD_PORT=9099   # set this port as per docs
export FEATURE_FLAG_GRPC_SERVICE_ADDR=featureflagservice:50053   # set feature flags

./build/install/opentelemetry-demo-ad/bin/Ad   # run the executable
```

Output:

```
Ad service started, listening on 9099 trace_id= span_id= trace_flags=
```

Build created successfully.

### Dockerfile Write-Up

First, delete the existing Dockerfile:

```bash
rm -rf Dockerfile
vim Dockerfile
```

...so we can write it from scratch.

We take the base image first. For Java apps, the popular one is `eclipse-temurin:21-jdk`. Here, "21" matches the JDK version installed locally.

```dockerfile
FROM eclipse-temurin:21-jdk AS builder
```

Set the work directory:

```dockerfile
WORKDIR /usr/src/app
```

Copy all the Gradle and source files in one shot:

```dockerfile
COPY . .
COPY ./pb ./proto
```

(Copies the `pb` folder into a new `proto` folder.)

Give execute permission to the `gradlew` wrapper and try to run it:

```dockerfile
RUN chmod +x ./gradlew
RUN ./gradlew
```

Next, install dependencies and build:

```dockerfile
RUN ./gradlew installDist -PprotoSourceDir=./proto
```

Now, stage 2 of the multi-stage Docker build:

```dockerfile
FROM eclipse-temurin:21-jdk AS release
```

Here, we can't use `alpine` as the base image, as we did for the Go service. Go is a special case: Go build files are self-contained binaries, meaning even on a machine without Go installed, the build file can run. This is not the case with Java — to execute a JAR file, you need a Java runtime, since Java is not a self-contained language.

If we insisted on using Alpine, we'd need to install a JRE on top of it, which gets messy. Instead, we choose an existing lightweight base image that already has a JRE:

```
eclipse-temurin:21-jre   (note: -jre, not -jdk)
```

Set the work directory:

```dockerfile
WORKDIR /usr/src/app
```

Copy the build executable from the builder stage:

```dockerfile
COPY --from=builder /usr/src/app/build/install/opentelemetry-demo-ad/bin/Ad .
```

This alone won't work — from the previous build image we also need the source code, so instead we do:

```dockerfile
COPY --from=builder /usr/src/app .
```

Run the executable:

```dockerfile
ENTRYPOINT ["./build/install/opentelemetry-demo-ad/bin/Ad"]
```

Build this Dockerfile into an image:

```bash
docker build -t abhishekf5/adservice:v1 .
```

Then run it:

```bash
docker run abhishekf5/adservice:v1
```

This should work fine — the Java microservice is now containerized as well.

---

## Containerization of Another Microservice (Recommendation Service — Python)

Move to the recommendation service:

```bash
cd src/recommendation   # https://github.com/iam-veeramalla/ultimate-devops-project-demo/tree/main/src/recommendation
```

Read the readme.md file to understand how to build this application. Unfortunately, this readme doesn't have much info, so we need to work with a developer to understand how to build it locally, in order to replicate the steps in the Dockerfile — or try to understand the code ourselves.

For example, Python projects have a `requirements.txt` file containing the list of dependencies, similar to `go.mod` in Golang or `pom.xml` in Java/Maven projects.

Also, from the project we find a file called `recommendation_server.py` — the main file of the project, per naming convention.

Delete the Dockerfile from the project, since we'll write it from scratch:

```bash
rm -rf Dockerfile
vim Dockerfile
```

### Dockerfile Write-Up

We select the base image `python:3.12`, specifically its slim version, `python:3.12-slim-bookworm`. We also need to confirm with the developer that the application works with version 3.12 — Python applications are usually backward-compatible, but it's still worth verifying.

```dockerfile
FROM python:3.12-slim-bookworm AS base
```

Set the work directory:

```dockerfile
WORKDIR /usr/src/app
```

Since `requirements.txt` has the dependencies, copy it into the image:

```dockerfile
COPY requirements.txt ./
```

In Python, we install dependencies with the `pip` command. As a best practice, upgrade pip first before installing:

```dockerfile
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
```

We previously only copied `requirements.txt`, but we need the whole project inside Docker:

```dockerfile
COPY . .
```

We won't do a multi-stage build here, so the next step is running the Python project. In Python, it's `python` followed by the main file — similar to Node.js, where it's `node` followed by the main file:

```dockerfile
ENTRYPOINT ["python", "recommendation_server.py"]
```

Build the image, per the Docker lifecycle:

```bash
docker build -t abhishekf5/recommendationservice:v1 .
```

Run it:

```bash
docker run abhishekf5/recommendationservice:v1
```

While running it, we get an error that the environment variable `OTEL_SERVICE_NAME` is not defined — this is fine for now, since the main goal is being able to build images. When we deploy to Kubernetes, we'll pass it in. Also, when running via Docker Compose, this will be fixed, since we'll provide it there.

It's very easy to containerize an application using Docker, regardless of whether the language is Java, Python, Go, or anything else.

---

## Docker Init: A Simple Way of Writing a Dockerfile

The `docker init` functionality is available in Docker Desktop but not in Docker Engine. To clarify: Docker Desktop can be installed on macOS/Windows, and Docker Engine on Linux.

So on the EC2 instance (a Linux machine), we don't have `docker init` — we need to run it locally and then paste the result into the EC2 Linux machine.

`docker init` is a command that, when run, asks a series of questions and then generates a Dockerfile for us. We still need to manually review it to verify everything checks out.

Let's do this locally on a Mac machine. Clone this repo: [ultimate-devops-project-demo](https://github.com/iam-veeramalla/ultimate-devops-project-demo).

Move to the project, then the shipping project:

```bash
cd src/shipping
docker init
```

- First, it asks whether it can overwrite `.dockerignore`, `Dockerfile`, `compose.yaml`, etc. — we say **yes**.
- Second, it asks whether our project is in a specific language (it also auto-detects). We selected **Rust**.
- It then asks for the Rust version to use — we give the latest version, or ask the dev team. Here we say **1.85.0**.
- It asks for the default file (`src/main.rs`) — we select it.
- It asks for a port number — we give **7077**.

That's it — the Dockerfile is created and ready for review.

However, you need prior experience writing Dockerfiles in case you encounter any issues that need fixing.

We check the generated Dockerfile by trying to build it, without any tag:

```bash
docker build .
```

The build didn't work, as `docker init` just gives a template — we need to check it and fix it as needed.

---

## Push the Container Image to a Registry

We push to a registry either to share it with other people on the team/company, or to deploy it to a server — deployment happens by pulling/pushing images from a registry.

**Popular registries:**
- Docker Hub
- ECR (Elastic Container Registry, AWS)
- GHCR (GitHub Container Registry)
- ACR (Azure Container Registry)

`docker push` is not specific to Docker Hub only — while Docker Hub is the default, images can be pushed to any of the registries above.

The first thing we need to do is log in to the container registry:

```bash
docker login docker.io
docker login quay.io
```

Check the Docker images you want to push:

```bash
docker images
```

Then push:

```bash
docker push arjunfeup/product-catalog:v1
```

(`arjunfeup` is the username — remember it.)

You'll find your pushed images in the Repositories section at [hub.docker.com](https://hub.docker.com/).

We can push another image:

```bash
docker push arjunfeup/adservice:v1
```

But if we try to push directly without the username prefix:

```bash
docker push adservice:v2
```

...we get "push access denied." So we need to follow the pattern `username/repository:version`.

### How Container Images Are Managed in a Company

Company name: **stargate**

We tag the images as:

```bash
docker build -t stargate/product-catalog:v1
```

Here, `stargate` is the organization name, `product-catalog` is the microservice name, followed by the version — similar to before, except we use the organization name instead of a personal username.

**Real example:** The official Nginx image is named `nginx/nginx-ingress`, where `nginx` is the organization name and `nginx-ingress` is the image name.

---

## Why Do We Need Docker Compose?

We already learned that with a Dockerfile, we can build application images and run them as containers.

Docker dockerizes one thing. A Dockerfile builds one image, and `docker run` starts one container — that's it. Docker itself doesn't know or care that your app also needs a database, a cache, a queue, etc.

Docker Compose manages multiple containers that need to work together as one system, defined in a single YAML file, started/stopped/networked together with one command.

Instead of running multiple services with multiple commands, Docker Compose can start all of them with a single command.

### Why You Need Both — the Realistic Company Scenario

This is exactly how it snowballs in practice:

- App starts with one container → plain Docker is enough.
- A dependency is added (DB, cache, queue, another microservice) → now you need multiple containers coordinated → Compose.
- As dependencies keep growing (Postgres, Redis, a mail-catcher for local dev, maybe a second internal service), the `docker-compose.yml` just grows with them — one file, one command, still `docker compose up`.

### How to Write a Docker Compose File

We write a YAML file, `docker-compose.yaml`, with 3 top-level objects:

- `services`
- `network`
- `volume`

Each of these parent objects has its own properties.

`services` contains multiple service definitions, each with either an `image` or `build` key. `image` is for ready-made base images, such as Redis, Postgres, etc. `build` is used when we need to build images for our own app, by providing the Dockerfile location:

```yaml
services:
  Ad:
    build:
      Dockerfile: src/app/Dockerfile

  redis:
    image: redis-1.23
```

We also provide a `depends_on` key if there's a dependency, such as a backend depending on a DB and Redis. We can also add environment variables:

```yaml
services:
  Ad:
    build:
      Dockerfile: src/app/Dockerfile
    environment:
      PORT: 300
```

We use these commands to start the containers:

```bash
docker compose up -d   # "-d" is detached mode, so a lot of logs aren't shown
docker compose down    # stops and deletes the containers and the private network it created
```
