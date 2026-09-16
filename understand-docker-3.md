# Development Best Practices: Code Hot-Reloading

- Dev environment can be used without Docker, but then it brings the typical problem of "it works on my computer but not yours."

  So we can simply use Docker for the dev environment too.

- For production, there is no problem as we are using Docker there itself.

For hot reloading, combine bind mounts with proper working directory settings:

```yaml
services:
	nodeapp:
		build: .
		volumes:
			- .:/usr/src/app
			- /usr/src/app/node_modules # anonymous volume to prevent host override

		command: npm run dev -- --watch
```

So in the volumes section, we have 2 mounts (mapping):

1. First, our current local host project folder (.) is mounted to the Docker container's (/usr/src/app) folder, meaning when Docker looks for the project's source code inside the /usr/src/app folder, it is referencing the current local project folder itself (.).

2. Second, we are creating an anonymous volume whose node_modules will be referenced.

Basically, we need to understand 2 things:

- During image build → Docker installs dependencies.
- When the development container starts with a bind mount → the bind mount can HIDE (not remove) those installed dependencies.

So when we are running our dev setup from inside Docker, meaning we are running Docker to start our dev server. And when we need to use a bind mount, we need to keep in mind that although our Docker containers are Linux containers, our host machine can be Windows/Linux/Mac.

And when we are installing dependencies locally, some packages contain operating-system-specific code. For example, a package installed on macOS may not run on Linux.

So, how will we have a dev setup which works via Docker on all machines?

So, we try to do 2 things:

- Our source code comes live from our host machine.
- And node_modules comes from the Docker container's project working directory.

This node_modules exists from the image build step but gets hidden because of the usage of the bind mount, so we simply unhide this node_modules path in the container's project working directory by providing an anonymous volume path.

```
Essentially, if we want to run server inside docker containers to serve our project then that server 
must see that project source code and node_modules inside that container project.

When we use bind mount then we start referencing from outside the container everything and thus node_modules 
present inside containers project gets hidden so once we point it in the volume section , 
everything starts working again.


Also, Hot reloading is a feature of your dev tool—such as Vite, Next.js, or nodemon.

It means:

“When I change code, automatically refresh/restart the app.”

It works in both cases:

Without Docker:
Your computer runs `npm run dev`

With Docker:
The container runs `npm run dev`

Docker does not create hot reloading. It only changes where the dev server 
runs either inside docker container or not.
```
