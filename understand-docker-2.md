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



# Understand Docker Concepts

## 1. Docker Volume

Docker volume is of 2 types:

a. Named volume.
b. Anonymous volume

**Named volume** - It will create a volume with a specific name. We do not need to give any path while creating it.

Default path (in host system) - `/var/lib/docker/volumes`

How to check its path:

```bash
docker volume ls
docker volume inspect my_persistent_data
```

This inspect command will display a JSON with a Mountpoint parameter that shows the path of volumes.

**Anonymous volume** - They are created automatically by Docker when a volume path is specified without a name.

So, we do not fire this command:

```bash
docker volume create my_volume
```

And only this command but not providing the mapping path here:

```bash
docker run -d --name myapp -v /app/data myapp-image
```

You see `/app/data` is different from named volume like `my_volume:/app/data`.

## 2. Bind Mount vs tmpfs Mounts

- tmpfs mounts provide temporary storage entirely in the host's RAM.

- Data written to a tmpfs mount is extremely fast because it never touches the disk, but it is completely discarded when the container stops.

- Use tmpfs for sensitive temporary files, caches, or session data that must not persist beyond the container runtime and should remain off-disk for security.

## Understand Docker Volume with Drivers and Plugins

- Plugins extend Docker's functionality.
- By default when we use volumes, we store data locally, but we can store the same data on remote hosts/storage or cloud providers with drivers and plugins.

Example: Azure file storage plugin, DigitalOcean Block Storage plugin, netshare plugin, AWS EBS.

It keeps the container code completely unaware of the underlying infrastructure.

## Advanced Use Cases

### 1. Sharing Data Between Containers

Multiple containers can safely share the same named volume to exchange data:

```yaml
services:
	web:
		image: nginx
		volumes:
			- shared_data:/usr/share/nginx/html
	processor:
 		image: python-processor
 		volumes:
 			- shared_data:/data/input
volumes:
 shared_data:
```

The web service writes files, and the processor service immediately reads them from the identical volume location.

### 2. Backup and Restore Strategies

Backup a named volume using a temporary container with the following exact command:

```bash
docker run --rm \
-v production_data:/data \
-v $(pwd):/backup \
busybox \
tar cvf /backup/backup.tar /da
```

Restore uses the reverse operation:

```bash
docker run --rm \
-v production_data:/data \
-v $(pwd):/backup \
busybox \
tar xvf /backup/backup.tar -C /data
```

This approach guarantees atomic, consistent backups regardless of the application running inside the containers.


# Postgres Setup in Docker

```yaml
version: "3.8"
services:
	postgres:
	image: postgres:16-alpine
	container_name: prod-postgres
	restart: unless-stopped
	environment:
		POSTGRES_USER: appuser
		POSTGRES_PASSWORD: SuperSecretPass123
		POSTGRES_DB: application
	volumes:
		- postgres_data:/var/lib/postgresql/data
		- ./init-scripts:/docker-entrypoint-initdb.d:ro
	ports:
		- "5432:5432"
volumes:
	postgres_data:
```

## Note

Volumes under services have 2 mounts/mappings or tasks inside it:

- **a.** First is a (Docker managed) named volume (`postgres_data`) mapped to the Postgres image data (`/var/lib/postgresql/data`).
- **b.** Second is the local `init-scripts` folder (`./init-scripts`) mounted/mapped to the special PostgreSQL initialization folder. This is for initial setup scripts, not ongoing data storage.

The official PostgreSQL Docker image has startup logic that says:

> "If I am creating a brand-new, empty database, check `/docker-entrypoint-initdb.d` and run any `.sql`, `.sql.gz`, or `.sh` files there."

When the PostgreSQL container first creates the database, it runs that script and creates the users table automatically.

`:ro` means **read-only**:

> The PostgreSQL container can read the scripts, but cannot edit or delete your local script files.

So the two mounts (solve different needs) together mean:

	1. Store the real database permanently:
	   `postgres_data` → `/var/lib/postgresql/data`

	2. Provide one-time database setup instructions:
	   `./init-scripts` → `/docker-entrypoint-initdb.d`

## Questions

### 1. Why do we need to create an "init-scripts" folder at the root of the project where docker is defined?

Do we even need it?

**Answer:**

Yes. We create init-scripts beside our docker-compose.yml like this:

```
my-project/
├── docker-compose.yml
└── init-scripts/
    ├── 01-schema.sql
    └── 02-seed-data.sql
```

It runs only when Docker initializes an empty PostgreSQL data volume. After that, Docker ignores it.

Next, we use migrations to enhance that table by adding/removing columns or even adding new tables at a later point.

Think of them like this:

```
Init scripts = create a brand-new database once
Migrations   = safely evolve the database over time
```

Example:

```
Day 1: create users table
Day 10: add phone_number column
Day 20: add orders table
```

With migrations:

```
001-create-users.sql
002-add-phone-number.sql
003-create-orders.sql
```

Each migration is tracked. If it has already run, it will not run again.

You can put SQL files in the init-scripts folder:

```sql
-- 01-schema.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL
);
```

Or initial data:

```sql
-- 02-seed-data.sql
INSERT INTO users (email)
VALUES ('admin@example.com');
```

People commonly use this in local development, demos, integration tests, and small projects to:

- create initial tables, indexes, and database extensions;
- add test/demo/initial admin data;
- create extra database users or permissions.

### 2. Does this kind of 2 mounting: named volume mounting and special initial setup run before the container runs, is it common in other databases like MongoDB or MySQL etc. too?

**Answer:**

Yes, this pattern is common, but the special initialization folder and behavior depend on the image.

| Database image | Persistent data path | Initialization support |
| --------------- | --------------------- | ----------------------- |
| PostgreSQL | `/var/lib/postgresql/data` | `/docker-entrypoint-initdb.d` runs `.sql` / `.sh` on first initialization |
| MySQL | `/var/lib/mysql` | `/docker-entrypoint-initdb.d` runs `.sql` / `.sh` on first initialization |
| MongoDB | `/data/db` | `/docker-entrypoint-initdb.d` runs `.js` / `.sh` on first initialization |
| Redis | `/data` | No equivalent standard automatic init-script folder in the official image |

Check the official Docker image documentation, especially:

- "Initialization"
- "Environment variables"
- "Volumes"
- "Data directory"
- docker-entrypoint-initdb.d

Do not assume every Docker image supports this just because PostgreSQL does. The image's startup script decides whether that special folder is recognised.
