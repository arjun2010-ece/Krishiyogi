Let’s build the files gradually using one example: **run two copies of an Nginx web server, then give them a shared address.**

These three things work together:

- **Pod:** holds your running container. In our example, each Pod contains one Nginx container.
- **Deployment:** tells Kubernetes how to create and maintain the Pods.
- **Service:** gives other applications a stable address for reaching those Pods. [Kubernetes](https://kubernetes.io/docs/concepts/workloads/pods/?utm_source=chatgpt.com)

**1. Start with the shared skeleton.** Both Deployment and Service manifests have these four main fields:

```yaml
apiVersion: # Which Kubernetes API version to use
kind:       # What kind of resource to create
metadata:   # Its identifying information
spec:       # How you want it configured
```

Read them as four questions:

| Field | Question it answers | Example |
|---|---|---|
| `apiVersion` | Which API understands this resource? | `apps/v1` |
| `kind` | What am I creating? | `Deployment` |
| `metadata` | What is its name? | `web-deployment` |
| `spec` | What should it do? | Run two copies of an application |

The fields inside `spec` depend on the `kind`: a Deployment needs Pod configuration; a Service needs networking configuration. [Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/?utm_source=chatgpt.com)

A few YAML basics before we continue:

- Indentation shows what belongs inside what. Use spaces, not tabs.
- A dash `-` starts an item in a list.
- Text after `#` is a comment.
- The incomplete skeletons below are for learning. Apply only the completed files.

**2. Give the Deployment its identity, then expand `spec`.**

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: web-deployment

spec:
  replicas: 2
  selector: {}
  template: {}
```

`apps/v1` is the API version for a Deployment. It is separate from your application’s version.

Inside `spec`, we now have three pieces:

| Field | Meaning |
|---|---|
| `replicas: 2` | “I want two Pods running.” |
| `selector` | “These labels identify the Pods this Deployment manages.” |
| `template` | “Use this blueprint when creating each Pod.” |

The empty `{}` values are placeholders that we will fill next. A Deployment uses a ReplicaSet behind the scenes to maintain the requested Pods; you do not need a separate ReplicaSet file here. [Kubernetes](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/?utm_source=chatgpt.com)

**3. Fill in the selector and Pod blueprint.** This gives us the complete `deployment.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: web-deployment

spec:
  replicas: 2

  selector:
    matchLabels:
      app: web

  template:
    metadata:
      labels:
        app: web

    spec:
      containers:
        - name: nginx
          image: nginx:stable
          ports:
            - containerPort: 80
```

Let’s read the newly added parts.

First, we put a label on every Pod created from this template:

```yaml
labels:
  app: web
```

Think of a label as a sticker: **“This Pod belongs to the web application.”**

Then the Deployment’s selector looks for that sticker:

```yaml
selector:
  matchLabels:
    app: web
```

The selector must match the labels in the Pod template. The key `app` and value `web` are choices we made; Kubernetes does not require those particular words. [Kubernetes](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/?utm_source=chatgpt.com)

Next, the template describes what runs inside each Pod:

```yaml
containers:
  - name: nginx
    image: nginx:stable
    ports:
      - containerPort: 80
```

This means:

- `containers`: the list of containers in **each Pod**.
- `name: nginx`: the name we give this container.
- `image: nginx:stable`: the container image to run.
- `containerPort: 80`: documents the port the application uses.

The application itself must actually listen on that port. Writing `containerPort: 80` does not configure the application or publish it to the internet.

Because the template contains one container and `replicas` is `2`, we get **two Pods, each with one Nginx container**. [Kubernetes](https://kubernetes.io/docs/concepts/workloads/pods/?utm_source=chatgpt.com)

You may notice that **`metadata` and `spec` appear twice**. Their location explains their meaning:

| Location | What it describes |
|---|---|
| `metadata` | The Deployment’s identity |
| `spec` | The Deployment’s configuration |
| `spec.template.metadata` | Labels attached to the Pods |
| `spec.template.spec` | What runs inside each Pod |

So `template` is a small Pod blueprint nested inside the Deployment. Kubernetes uses it repeatedly when creating Pods. [Kubernetes](https://kubernetes.io/docs/concepts/workloads/pods/?utm_source=chatgpt.com)

**4. Now build the Service skeleton.** Our Pods can be replaced, and replacement Pods can have different IP addresses. A Service gives clients a stable way to reach them. [Kubernetes](https://kubernetes.io/docs/tutorials/services/connect-applications-service/?source=post_page---------------------------\&utm_source=chatgpt.com)

Start with this:

```yaml
apiVersion: v1
kind: Service

metadata:
  name: web-service

spec:
  type: ClusterIP
  selector: {}
  ports: []
```

Notice that Service uses `apiVersion: v1`.

Its `spec` answers three questions:

| Field | Question |
|---|---|
| `type` | How should this Service be exposed? |
| `selector` | Which Pods should receive traffic? |
| `ports` | Which Service port maps to which application port? |

We use `ClusterIP` for access within the cluster. It is also the default Service type.

Now fill the placeholders to make the complete `service.yml`:

```yaml
apiVersion: v1
kind: Service

metadata:
  name: web-service

spec:
  type: ClusterIP

  selector:
    app: web

  ports:
    - port: 8080
      targetPort: 80
```

Read this as:

> “Create a Service named `web-service`. Accept traffic on port `8080` and send it to port `80` on Pods labelled `app: web`.”

| Setting | Meaning |
|---|---|
| `port: 8080` | The port clients use on the Service |
| `targetPort: 80` | The destination port where Nginx listens |

These numbers can differ. Also notice that the Service selector contains `app: web` directly—there is no `matchLabels` field here. [Kubernetes](https://kubernetes.io/docs/concepts/services-networking/service/?utm_source=chatgpt.com)

**5. Connect the two files through the Pod labels.** These are the three related places:

| Location | Value | Purpose |
|---|---|---|
| Deployment → `spec.selector.matchLabels` | `app: web` | Identifies Pods to manage |
| Deployment → `spec.template.metadata.labels` | `app: web` | Puts the label on each Pod |
| Service → `spec.selector` | `app: web` | Selects Pods to receive traffic |

**The Service finds Pods through their labels.** It does not look for the filename or the Deployment name. That is why `web-deployment` and `web-service` can have different names. [Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/?utm_source=chatgpt.com)

Another application running in the same namespace can now use:

```text
http://web-service:8080
```

The Service directs the connection to an eligible Pod on port `80`. [Kubernetes](https://kubernetes.io/docs/tutorials/services/connect-applications-service/?source=post_page---------------------------\&utm_source=chatgpt.com)

**6. Apply the completed files.** With a running Kubernetes cluster and `kubectl` connected to it:

```bash
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

`apply` asks Kubernetes to create or update the resources according to your files. [Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/?utm_source=chatgpt.com)

Check what was created:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

Once the Pods are running, you can try the application from your computer using:

```bash
kubectl port-forward service/web-service 9000:8080
```

Keep that command running and open [http://localhost:9000](http://localhost:9000).

Here, `9000` is your computer’s port. `kubectl` uses the Service’s `8080` mapping to forward to port `80` on a selected Pod. This provides temporary local access for testing. [Kubernetes](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/?utm_source=chatgpt.com)

For a first experiment, change `replicas: 2` to `replicas: 3` in `deployment.yml`, then apply that file again. Kubernetes will work toward running three Pods. The Service will automatically include the new Pod when it is ready because it has the same `app: web` label. [Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/?utm_source=chatgpt.com)
