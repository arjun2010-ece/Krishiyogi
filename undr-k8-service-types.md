A Kubernetes **Service** gives a stable address to a group of Pods.

Why? Pods can be recreated and their IP addresses change. Instead of your frontend calling a changing Pod IP, it calls a stable Service name such as:

```txt
http://users-api
```

Kubernetes then sends the request to one healthy Pod behind that Service.

## The basic building block: `ClusterIP`

`ClusterIP` is the default Service type.

```txt
Frontend Pod → users-api Service → one of the Users API Pods
```

- Accessible **only inside the Kubernetes cluster**
- Gives the Service an internal IP and DNS name
- Distributes traffic among matching Pods
- Usually used for backend APIs, databases, Redis, internal microservices

```yaml
type: ClusterIP
```

Think: “My internal receptionist knows which current Pod should receive the call.”

---

## Level ahead: `NodePort`

`NodePort` builds on top of `ClusterIP`.

```txt
Outside user
    ↓
Any Node IP : fixed NodePort
    ↓
ClusterIP Service
    ↓
One healthy Pod
```

For example:

```txt
http://<node-ip>:30080
```

- Kubernetes opens the **same port on every worker node**
- External traffic reaching any node at that port is forwarded to the Service
- It still has the internal `ClusterIP` functionality too

```yaml
type: NodePort
```

So yes: `NodePort` provides both:

1. Internal cluster access via `ClusterIP`
2. External access via `NodeIP:NodePort`

Please note that normally in a vpc scenarios, if a ec2 instance outside the k8 cluster but inside the vpc, normally uses nodePort.

It is useful for local learning clusters or when you provide your own external load balancer. But exposing real production applications as `IP:30080` is usually not convenient.

Kubernetes normally allocates NodePorts from `30000–32767`. [Kubernetes](https://kubernetes.io/docs/concepts/services-networking/service/?utm_source=chatgpt.com)

---

## Next level: `LoadBalancer`

`LoadBalancer` is generally the next layer above `NodePort`.

```txt
Internet user
    ↓
Cloud Load Balancer / public IP
    ↓
NodePort
    ↓
ClusterIP Service
    ↓
One healthy Pod
```

```yaml
type: LoadBalancer
```

In a cloud environment such as AWS EKS, Azure AKS, or Google GKE, Kubernetes asks the cloud provider to create an actual external load balancer and give it a public IP or DNS name.

Traditionally, it provides all three layers:

| Capability | `ClusterIP` | `NodePort` | `LoadBalancer` |
|---|---:|---:|---:|
| Internal Service IP/DNS | Yes | Yes | Yes |
| Node IP + fixed port | No | Yes | Usually yes |
| Public cloud load balancer/IP | No | No | Yes |

So the normal mental model is:

```txt
ClusterIP → NodePort → LoadBalancer
```

However, one modern exception exists: some load balancer implementations can route directly to Pods, so Kubernetes can be configured **not** to allocate NodePorts for a `LoadBalancer` Service. In that case, it still gives you the external load balancer, but not the NodePort layer. [Kubernetes](https://kubernetes.io/docs/concepts/services-networking/service/?utm_source=chatgpt.com)

---

## Separate type: `ExternalName`

`ExternalName` is **not a higher level** of `ClusterIP`, `NodePort`, or `LoadBalancer`.

It is a DNS alias.

```txt
Pod calls: payments-db
          ↓
Kubernetes DNS says:
payments-db = external-db.example.com
          ↓
Pod connects to external-db.example.com
```

```yaml
type: ExternalName
externalName: external-db.example.com
```

It does **not** create:

- a ClusterIP
- a NodePort
- a load balancer
- a proxy to Pods

It only tells Kubernetes DNS: “When someone asks for this internal Service name, return this external hostname.” [Kubernetes](https://kubernetes.io/docs/concepts/services-networking/service/?utm_source=chatgpt.com)

---

## A simple real-world example

Suppose you have a React frontend and NestJS API in EKS:

```txt
Internet
  ↓
LoadBalancer / Ingress
  ↓
frontend Service
  ↓
frontend Pods

frontend Pods
  ↓
api Service (ClusterIP)
  ↓
NestJS API Pods

API Pods
  ↓
postgres Service (ClusterIP)
  ↓
Postgres Pod(s)
```

Typical choice:

- `frontend`: exposed externally using `LoadBalancer` or, more commonly, an **Ingress**
- `api`: `ClusterIP`, because only frontend and other cluster services need it
- `postgres`: `ClusterIP`, because it must remain private

One final connection: **Ingress is not a Service type.** It sits in front of Services and routes HTTP/HTTPS requests by hostname or path, for example:

```txt
app.example.com        → frontend Service
app.example.com/api    → API Service
```

For production web apps, you commonly use one external load balancer/Ingress and keep most app Services as internal `ClusterIP`s. Official Kubernetes documentation describes the normal nesting as `ClusterIP → NodePort → LoadBalancer`, while `ExternalName` is a separate DNS-only case. [Kubernetes](https://kubernetes.io/docs/concepts/services-networking/service/?utm_source=chatgpt.com)
