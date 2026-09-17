# Container Networking - Connecting Services

- A project can have many high-level components like frontend, backend, database, Redis, Kafka, etc. And all of these are called services in the Docker context, and they each have their own containers, which need to talk with each other, like a backend needs to talk to the DB to do some operations on it. Same with Redis also. Frontend needs to talk with the backend to fetch data also.

- All of this container communication can happen only on a network; otherwise, there is no way they can talk with each other. Without proper networking, even the most perfectly built images remain useless in any multi-service application.

## Default Bridge Network Explained

- When the Docker daemon starts for the first time on a Linux host, it automatically creates a virtual network called the default bridge network.

- This network uses the bridge driver and appears as a software switch named `docker0` on the host.

- Every container launched without an explicit `--network` flag automatically attaches to this default bridge network.

- Docker's default bridge network gives each container a private IP address. Containers can access the internet through the Docker host, but outside traffic cannot reach a container unless you publish a port, for example `-p 3000:3000`.

- Containers have private IP addresses that the internet cannot use directly.

  When a container sends a request to the internet, Docker makes it look as if the request came from the host machine's IP address. (IP masquerading)

  The reply comes back to the host, and Docker sends it to the correct container.

  ```
  Container → Docker host → Internet
  ```

- Docker's default bridge network often uses the range `172.17.0.0/16` for distributing IP addresses. Docker creates a bridge with gateway IP `172.17.0.1`. Each connected container receives its own private IP, such as `172.17.0.2`, `172.17.0.3`, and so on.

  The Docker bridge connects those containers to each other and to the host.

  ```
  Docker bridge / gateway:  172.17.0.1
  Container 1:              172.17.0.2
  Container 2:              172.17.0.3
  Container 3:              172.17.0.4
  ```

- Containers on the default bridge network can reach each other using their assigned IP addresses, but name resolution does not work. Attempting to ping another container by name fails because the default bridge lacks the embedded DNS server present in user-defined networks.

## Commands

1. Check all the networks present in Docker:

   ```bash
   docker network ls
   ```

2. Inspect any network within Docker:

   ```bash
   docker network inspect bridge    # "bridge" is the name of the network.
   ```

   - The inspect output shows connected containers, their IP addresses, the subnet, gateway, and all iptables options managed by Docker.

## How to Check if Container Communication Is Working or Not?

1. Run 2 containers with the same/different images.

   ```bash
   docker run -dit --name alpine1 alpine ash
   docker run -dit --name alpine2 alpine ash
   ```

   - `-dit` means detached mode (`-d`) combined with an interactive terminal (`-it`): `-i` keeps STDIN open and `-t` allocates a pseudo-TTY.
   - alpine1/alpine2 are the names of 2 different containers, and within Alpine, `ash` is the terminal, like `bash`/`shell` in Linux.
   - We put the `-it` flag and `ash` terminal because we want the container to continue running by giving it a process (`ash`) to run. Without it, the container will start up and immediately exit and stop.

2. Inspect the network with the below command, and we can see the connected containers' names, IP addresses, etc.

   ```bash
   docker network inspect bridge
   ```

3. Ping from alpine1 to alpine2 with this command:

   ```bash
   docker exec -it alpine1 ping -c 2 172.17.0.3
   ```

   - The `-c` flag stands for count, and `2` means send exactly 2 ping packets and then stop.
   - Source container name: `alpine1`; destination container IP address: `172.17.0.3`.

## How to Create Custom Bridge Networks?

Custom bridge networks are better than Docker's default bridge network.

Each custom network gets:

- its own isolated network;
- its own IP range (subnet);
- automatic DNS, so containers can communicate using service/container names.

Command to create a custom network:

```bash
docker network create --driver bridge --opt com.docker.network.bridge.name=br-app-net --opt com.docker.network.bridge.enable_icc=true app-net
```

Please note that:

1. This command will simply create a bridge network:

   ```bash
   docker network create app-net
   ```

   but for having specific control we specify `--driver`, the same flag needed to create other network types like overlay, macvlan, etc., so:

   ```bash
   docker network create --driver bridge app-net
   ```

2. Now, simply creating a network is sometimes not enough; we want to have more control, like naming the bridge itself and specifying whether inter-container communication is allowed or not, with these options:

   ```
   --opt com.docker.network.bridge.name=br-app-net
   --opt com.docker.network.bridge.enable_icc=true
   ```

   `enable_icc`: This is true even if not specified, but it will not be visible when inspected if not provided explicitly.

   So:

   ```bash
   docker network create --driver bridge --opt com.docker.network.bridge.name=br-app-net --opt com.docker.network.bridge.enable_icc=true app-net
   ```

3. For finer control, we can provide `subnet` and `gateway` too, like this:

   ```bash
   docker network create \
    --driver bridge \
    --subnet 10.10.0.0/24 \
    --gateway 10.10.0.1 \
    --opt com.docker.network.bridge.name=br-app-net \
    --opt com.docker.network.bridge.enable_icc=true \
    app-net
   ```

## How to Attach/Detach an Existing Container to an Existing Network (Created Above)

- This command will connect an existing network `net0` to an existing container `alpine1`:

  ```bash
  docker network connect net0 alpine1
  ```

  But it does not remove this container from its previous default bridge network connection, meaning it gets connected to 2 networks, which is what we do not want.

  Verify it with:

  ```bash
  docker inspect alpine1
  ```

- This command will disconnect the container (`alpine1`) from the connected network (`bridge`):

  ```bash
  docker network disconnect bridge alpine1
  ```

  ```bash
  docker network connect app-net existing-container
  docker network disconnect app-net existing-container
  ```

## Other Network Drivers or Network Types

Docker has different network types for different situations.

**B-HOM (Bridge-Host-Overlay-Macvlan)**

### 1. Bridge

- Most common network driver. Creates isolated networks.
- Used by Docker's default bridge network and custom bridge networks.
- You usually publish ports with `-p`.

### 2. Host

- Removes all network isolation. The container shares the host's network stack directly, using the host's IP and ports.
- No port mapping needed.

### 3. Overlay

- Used when containers run on multiple machines (multi-host networking).
- Docker creates a virtual network between those machines.
- Common with Docker Swarm.

```
Container on Server A ←→ Container on Server B
```

### 4. Macvlan

- Each container gets its own MAC address and network identity.
- Your router/LAN can see it as a separate device.
- Rarely needed in normal web applications; used mainly for legacy applications.

**Note:**

- Docker has a `none` driver too, to have complete network isolation without any interface.

### Examples

```bash
# Create a macvlan network with its configs.

docker network create -d macvlan \
 --subnet=192.168.1.0/24 \
 --gateway=192.168.1.1 \
 --opt parent=eth0 \
 macvlan-net

# Create/run an "nginx" container inside an existing "macvlan" (macvlan-net) network
docker run --network macvlan-net --ip 192.168.1.100 nginx
```

## Network Isolation and Security

- Custom networks automatically isolate traffic, meaning unless specified, no container is connected to the custom network, and hence no data is shared.

- Containers on `frontend-net` cannot reach containers on `database-net` unless explicitly connected or linked through a proxy.

## Docker Compose Example of Backend Connected with DB

```yaml
version: '3.8'
services:
	db:
		image: postgres:16-alpine
		container_name: postgres-db
		environment:
		 POSTGRES_PASSWORD: SuperSecretPass123
		 POSTGRES_USER: appuser
		 POSTGRES_DB: production
		networks:
			- app-network
		volumes:
			- pgdata:/var/lib/postgresql/data

	web:
		image: my-node-app:latest
		container_name: node-web
		ports:
			- "3000:3000"
		environment:
			DATABASE_URL: postgres://appuser:SuperSecretPass123@db:5432/production
		depends_on:
			- db
		networks:
			- app-network

networks:
	app-network:
		driver: bridge
		driver_opts:
			com.docker.network.bridge.enable_icc: "true"

volumes:
	pgdata:
```

Please note:

1. Custom network `app-network` is provided for both `db` and `web` containers so they can communicate with each other. You see, networks are defined in their own block and then referenced inside each container service.

2. For `web`, port mapping is provided as it needs to talk to the frontend, but not for `db`.

3. The `web` container depends on the `db` container, so the `depends_on` parameter is provided.

4. For the database `db` container, a named volume mapping is provided to point to where Postgres stores its data by default.

5. Also, notice that `volumes` are defined in their own section, and since this is not a "bind mount" — where we define the path on our computer — we keep it empty for a named volume here.

6. Observe here that, for db we are using named volume and for db volume section, we could have provided ```init-scripts``` too.
