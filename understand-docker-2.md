# Data Persistence in Docker Containers

- A Docker container has its own small, temporary filesystem — either an Alpine Linux filesystem or a Node.js Linux filesystem. Basically, a container is a Linux container at its core, even if it can be a stripped-down version.

- If the container stops, its files still exist but won't be available. As soon as it starts, its files become available.

```bash
docker stop my-app
docker start my-app
```

- But if the container is removed, its internal files are removed too:

```bash
docker rm my-app
```

- For example, if MongoDB stores data inside its container:

```
container filesystem
└── /data/db
    └── users, orders, products...
```

Removing that container can remove the database data as well. That is dangerous.



# Docker Data Persistence: Volumes and Bind Mounts

To prevent data loss, Docker provides two primary mechanisms for data persistence: **Docker Volumes** and **Bind Mounts**.

## 🔒 Part 1: Docker Volumes (Best for Production & Databases)

Docker Volumes are completely managed by Docker and isolated from the core host file system.

### Step 1: Create a managed volume

```bash
docker volume create my_volume
```

Verify that the volume was created:

```bash
docker volume ls
```

### Step 2: Start a container with the volume attached

```bash
docker run -d --name app_volume -v my_volume:/app nginx
```

### Step 3: Write data inside the container

```bash
docker exec app_volume bash -c "echo 'Persistent data from Volume' > /app/data.txt"
```

Verify the file exists inside:

```bash
docker exec app_volume cat /app/data.txt
```

### Step 4: Simulate a crash / Destroy the container

```bash
docker rm -f app_volume
```

### Step 5: Attach the same volume to a NEW container

```bash
docker run -d --name app_volume_new -v my_volume:/app nginx
```

### Step 6: Verify data persistence

```bash
docker exec app_volume_new cat /app/data.txt
```

**Result:** You will see `Persistent data from Volume`. The data survived the total destruction of the original container!

### Cleanup Part 1

```bash
docker rm -f app_volume_new
docker volume rm my_volume
```

## 📂 Part 2: Bind Mounts (Best for Local Development)

Bind Mounts directly link a folder on your host machine to a directory inside the container.

### Step 1: Create a local directory on your host machine

```bash
mkdir -p ~/docker_lab/html
echo "<h1>Hello from Local Host (V1)</h1>" > ~/docker_lab/html/index.html
```

### Step 2: Start an Nginx container using the bind mount

```bash
docker run -d --name web_server -v ~/docker_lab/html:/usr/share/nginx/html -p 8080:80 nginx
```

### Step 3: Test access in your browser or terminal

```bash
curl http://localhost:8080
```

Output: `<h1>Hello from Local Host (V1)</h1>`

### Step 4: Edit the file locally on your host machine (no container restart!)

```bash
echo "<h1>Live update reflected instantly! (V2)</h1>" > ~/docker_lab/html/index.html
```

### Step 5: Verify immediate change

```bash
curl http://localhost:8080
```

Output: `<h1>Live update reflected instantly! (V2)</h1>`

### Cleanup Part 2

```bash
docker rm -f web_server
rm -rf ~/docker_lab
```

## 💡 Summary & Takeaways / Resumen

- Use **Docker Volumes** when you need secure, isolated, and high-performance storage for databases (e.g., PostgreSQL, MySQL, MongoDB) or production services.
- Use **Bind Mounts** when developing code locally so your IDE edits immediately reflect inside the container without rebuilding images.





## Other thoughts


A volume keeps important data outside the container's temporary filesystem.

```
Docker volume
└── database data

MongoDB container
└── /data/db → uses that Docker volume
```

Example:

```bash
docker run -v mongo-data:/data/db mongo
```

Meaning:

> "Mount the persistent Docker volume named `mongo-data` on the host machine into `/data/db` inside the MongoDB container."

Now you can remove and recreate the MongoDB container, but the data remains in `mongo-data`.

## Why real applications use volumes

- Databases must keep users, orders, payments, etc.
- Uploaded files may need to survive container replacement.
- Containers are commonly recreated during deployment, updates, crashes, or scaling.
- You should treat containers as replaceable; important data should live separately.

## A simple rule

- **Container** = application process and temporary environment.
- **Volume** = persistent data that must survive container removal.

For a Node app, `node_modules` can also be mounted as a development volume to avoid being overwritten by your local files. But in production, the most important use case is persistent data for databases and user uploads.

## Some examples

**1.**

```bash
docker run -d --name web_server -v ~/docker_lab/html:/usr/share/nginx/html -p 8080:80 nginx
```

In this command, 2 things are important:

a. `~/docker_lab/html` — it is the folder that stores container data in host machine.

b. `/usr/share/nginx/html` — it is the default folder Nginx reads inside container

So, who decides which default folder a container will use?

The answer is: For every image, the important paths are decided by the application/image, not by Docker. Check the image's official Docker Hub documentation or its configuration.

So the above path (`/usr/share/nginx/html`) can be found in docker hub image site.

### Common examples

| Container | Important persistent path inside container |
| --- | --- |
| Nginx | `/usr/share/nginx/html` — website files it serves |
| Redis | `/data` — persisted Redis data |
| PostgreSQL | `/var/lib/postgresql/data` — database files |
| MongoDB | `/data/db` — database files |

### Simple rule

First find where the application reads or writes its important files inside the container. Then mount a host folder or Docker volume to that exact path.
