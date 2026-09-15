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
