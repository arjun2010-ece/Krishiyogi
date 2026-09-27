# VPC Explanation

Source link: [https://www.youtube.com/watch?v=P8g7Z4NYk3Q&list=PLdpzxOOAlwvLNOxX0RfndiYSt1Le9azze&index=6](https://www.youtube.com/watch?v=P8g7Z4NYk3Q&list=PLdpzxOOAlwvLNOxX0RfndiYSt1Le9azze&index=6)

## VPC (Isolated Cloud Resources)

Let's learn:
- What is a Virtual Private Cloud?
- Why do you need a Virtual Private Cloud?
- What are the different components of a Virtual Private Cloud?
- How do they interact with each other?

## Let's Understand with a Real Example Scenario

Imagine there is a large village. Some people there do not want to build or maintain their own houses. They want someone else to handle the construction and maintenance for them.

Now there is a smart person in the village called ABC. He sees an opportunity. He buys a large piece of land and tells people: "Send me your requirements—how big a house you need and what facilities you want. I will build and maintain it for you, and you pay me for the service."

It is similar to houses built one after another nearby, like my home in Mughalsarai and my neighbour's home there.

This works well at first. ABC builds houses for different people, takes care of the maintenance, and everyone is happy.

## Now the Problem in the Above

But then some people notice a problem. The houses are too close together, with little separation or security. If someone gets into one house, they may be able to access another one as well. So they tell ABC: "We also want houses, but we want privacy and better security."

## New Idea

ABC comes up with a new idea: a secure community inside his land. It has a gate at the entrance, so only approved people can enter. There can be a security guard at the gate to check who is allowed in.

Inside the community, visitors also need directions to reach the correct house. And when they arrive, there can be another check: "Are you allowed to meet this person?"

Similar to a housing society like Rohit's house in Gaurs or Juhi's friend's house.

So now the community has three important things:

- an entry point (Gateway),
- a way to direct visitors to the right house, and
- security checks at each house.

This gives people privacy and isolation. Seeing this, more groups ask ABC to build similar secure communities.

You may be wondering what this has to do with AWS. Let's connect it.

Think of a large AWS Region, such as Mumbai, Ohio, or Frankfurt. Inside a Region, AWS operates data centers. Earlier, many companies had to build and maintain their own data centers, which was expensive and difficult—especially for startups.

AWS saw this opportunity. It built data centers and told companies: "Tell us how many virtual machines you need. You pay us, and we will provide them."

---

Yes, a single physical server can run multiple virtual machines (VMs) at the same time using software called a hypervisor.

Running multiple virtual "machines" on a single physical server is known as virtualization, and it is the foundational technology that Amazon Web Services (AWS) used to build its entire cloud business.

---

For example, a company might request ten EC2 instances. AWS creates those virtual machines inside its data centers, which contain many physical servers. Multiple customers' virtual machines can run on the underlying infrastructure.

But this creates an important concern: security and isolation.

Let's say a single physical server has a total of 30 VMs (virtual machines). Company A has taken 5 VMs on the same server, Company B took 10 VMs, Company C took 8 VMs, and a startup took 4 VMs.

Let's say a hacker hacks one VM assigned to the startup, and since all the other VMs are on the same physical server in the AWS data center, he can easily go to other VMs and hack the entire thing.

So just because of the startup, what happened is all of the servers are hacked, because AWS was creating entire instances on the same physical server. And until 2013–2014 it was happening.

## AWS Solution

So to solve this problem, like I told you even in the previous example to solve the security breach, what AWS said is: "Okay, we will come up with a new concept." In that case it was a secure community; in AWS terms it is called a VPC.

So what AWS said is: we will build a VPC for you, or in the other way around—like in the previous case the builder will build the entire secure community and give it to you—but in AWS terms, AWS will give you documentation, AWS will give you examples.

Who is the one who builds this entire VPC and maintains the VPC? It is a DevOps or AWS DevOps engineer.

So the AWS DevOps engineer, looking at the documentation of AWS, will go to the AWS portal and they will request the VPC and they will configure everything inside the VPC.

Now let's see what is inside the VPC using the same example itself. I'll try to convert that into an AWS example.

So let's talk about in the context of an AWS data center again.

Let's take the example of a company called TCS. Inside TCS, there is a project, and a DevOps engineer is responsible for setting up its infrastructure.

The engineer goes to AWS, chooses a Region such as Mumbai, and says, "I need a VPC."

So whenever a DevOps engineer creates a VPC, what AWS asks is: what is the IP address range?

## How Do We Define the Size of a VPC?

So for defining the size of a VPC, there is something called an IP address range.

In the real-world example, we used land area such as acres or hectares. In AWS, we define the size of a VPC using an "IP address range", also called a CIDR block.

For example, if the engineer chooses `172.16.0.0/16`, AWS gives the VPC a range containing 65,536 IP addresses, so technically you can assign these IP addresses to 65,536 application instances (or VMs).

Don't worry about the calculation for now. Just understand that this range defines the size of the VPC and how many private IP addresses can be used inside it.

But one project may contain multiple smaller applications or teams—for example, payments, transactions, and another internal service. So the DevOps engineer splits the VPC's IP range into smaller ranges, such as:

```
172.16.1.0/24
172.16.2.0/24
172.16.3.0/24
```

Each of these is called a subnet, which simply means a smaller network inside the VPC. A `/24` subnet contains 256 IP addresses. AWS reserves a few of them, but the rest can be assigned to resources such as EC2 instances.

What you are doing here is that the VPC is created with a particular IP address range, so as a DevOps engineer, you are splitting the IP address range for your sub-projects, calling it a subnet, and inside this sub-project—let's say we have only one application—so you deploy an EC2 instance and the application on it.

On another sub-project, you can have 2 applications (or microservices), so you will deploy 2 EC2 instances. And similarly we deploy in other sub-projects too.

So, the VPC is one large network, and subnets help us organize it into smaller sections. One subnet may host one application (one EC2 instance), while another may host multiple EC2 instances. The exact setup depends on the project's requirements.

So, after creating the VPC and subnets inside it, what will the DevOps engineer do?

They will create a gateway.

## Why Is This Gateway Required?

If there is no gateway, nobody can access this particular VPC.

So without a gate nobody can enter the gated community or the secure community; similarly, without this gate, nobody can access or enter this entire property itself, which is called a VPC.

So this is the way for users on the internet to access the application. Just like a gated community needs an entrance, a VPC needs an Internet Gateway.

Let's say there is a relative, as in the previous case—here let's say there is a customer who wants to access an application on this EC2 instance in a particular subnet within this VPC.

There is a customer who wants to access the application on this EC2 instance, so he has to definitely come through this gateway itself to the VPC. So firstly there will be a gateway, and what this gateway will do is: the gateway is just like a pass for someone to enter this VPC.

Once they enter the VPC through the gateway, what will happen?

Inside the VPC, we have one subnet here, another there, and another there, all within the VPC itself.

Like in a gated community, we imagine we have free space inside the VPC before reaching the houses or a particular subnet. And this we call public subnets.

Please note that inside VPCs, the sub-projects owning their own subnets is called private subnets.

So as soon as the customer enters the VPC gateway, then it accesses the public subnet first.

---

So how does the public subnet connect to the user on the internet?

It is through the VPC gateway.

---

Once the user enters through the public subnet, it encounters a load balancer, and it forwards the traffic to the correct application instance (EC2 instances). It uses a target group to know which instances should receive traffic.

Now there has to be a path which leads from the public subnet / load balancer to the target EC2 instance.

But how does the public subnet / load balancer know the path to reach the private subnet? For that, we will be creating something called a route table.

And this route table defines how a request should go to the application (a specific EC2 instance).

Finally, even if the request reaches the EC2 instance, there will be something called a Security Group, which can say which port you want to connect to or which IP address you are coming from.

A Security Group acts like a security guard for the instance, which allows or blocks traffic based on rules such as port or internet IP, as mentioned above.

So, a Security Group can say: "Okay, only if it is coming from this particular IP address on the internet," or "only if you are trying to access me on a particular IP address, then I will allow the access," and that way you will finally reach your application.

## So What Is Happening on the Whole VPC Communication Flow?

Let's summarise it here.

If someone from the internet is trying to access an application in the private subnet—first of all he has to make a request, and his request has to go through the Internet Gateway. Once it reaches the Internet Gateway, it will go to the public subnet in the VPC.

So what is a public subnet?

Public subnet—it's a common subnet across the VPC. Once it goes to the public subnet, there is a load balancer.

So, what is the load balancer doing?

The load balancer is attached to the public subnet, and the load balancer has a target group. So when a request goes to the load balancer, the load balancer is the one that takes the request to the private subnet and to the application.

So for the load balancer to understand how to reach this application—although the private subnet exists here—for the load balancer to understand the path to the private subnet, there is something called a route table.

So the route table is something which defines the path from the public subnet to the private subnet.

Even when the request goes to the EC2 instance (the application hosted on EC2 is hidden behind a private subnet IP address), there is something called a Security Group, which can block access.

Once the Security Group allows you, you reach the application (hosted on EC2).

### VPC Components We Discussed Here

- Internet Gateway
- Public subnet
- Load balancer (e.g. Elastic Load Balancer / ELB in AWS)
- Route table
- Private subnet
- Security Group

## A Few More Important Concepts

There are a few more important concepts apart from the above:

- One is NACL (Network Access Control Lists), and
- the other is NAT Gateway.

Now, as we have studied previously about multiple subnets (private ones), within a subnet we can have multiple Security Groups also on multiple EC2 instances.

Now, imagine if within the same subnet, there can be multiple EC2 instances (applications too). So if we want to repeat the same Security Group configuration on multiple EC2 instances, then we have something called NACL.

Instead of defining the same thing again and again, we can define that as part of NACLs, and it is defined at the subnet level.

### More Technically

Now imagine you want to control traffic rules for every resource inside a particular subnet. Instead of attaching and managing Security Group rules on each individual EC2 instance, AWS also provides NACLs.

A NACL works at the subnet level. Any resource inside that subnet is affected by the NACL rules. For example, you can allow or deny traffic from a particular IP range for the whole subnet.

However, NACLs and Security Groups are not replacements for each other:

- Security Groups work at the EC2 instance or network-interface level and are stateful.
- NACLs work at the subnet level and are stateless, so you must explicitly allow both incoming and outgoing traffic.

In practice, Security Groups are used for most application-level access control, while NACLs provide an additional security layer for the entire subnet.

## NAT Gateway

There is another very important concept called NAT Gateway.

Imagine we have EC2 instances where our real applications are hosted, and we want to download something from the internet on this EC2 instance. So we make a request from this EC2 instance to the internet site.

In that case, the IP address of our server (EC2 instance) will be exposed to the external site, and a hacker or a malicious script can hack our server.

This is a bad practice—to expose our server's IP address to the internet. And the external site should not know the IP address of our server or private subnet application.

So how do we avoid it?

We avoid it by masking our IP address, and this is called a NAT Gateway—essentially it is a Network Address Translation (NAT) service.

So what does a NAT Gateway do?

It helps us make a request to the internet to access some resource from an external site, like downloading a resource, by masking or translating our actual IP address (private subnet) with the public subnet IP address, either of the load balancer or of the router (or route table).

If it is at the load balancer level we call it SNAT (Source Network Address Translation), and if it is going through the route table we call it NAT Gateway.

### More Technically

Imagine we have EC2 instances where our actual applications are hosted, and these instances are inside a private subnet. Sometimes, the application may need to access the internet—for example, to download system updates, install packages, call a third-party API, or access an external service.

But because this EC2 instance is in a private subnet, it should not accept direct requests from the internet, and it normally does not have a public IP address.

So how can it access the internet?

This is where a NAT Gateway comes in. NAT means Network Address Translation. A NAT Gateway is placed in a public subnet and has a public Elastic IP address.

When an EC2 instance in a private subnet sends a request to the internet, the request first goes through the NAT Gateway. The NAT Gateway translates the private IP address of the EC2 instance into its own public IP address before sending the request outside.

So, the external website sees the public IP address of the NAT Gateway, not the private IP address of the EC2 instance.

The response then comes back to the NAT Gateway, which forwards it to the correct private EC2 instance.

The important point is: the NAT Gateway allows resources in a private subnet to make outbound internet requests, but it does not allow the internet to initiate a new direct connection to those private resources.

To make this work, the private subnet's route table sends internet-bound traffic (`0.0.0.0/0`) to the NAT Gateway. The NAT Gateway itself is in a public subnet, whose route table sends internet-bound traffic to the Internet Gateway.

---

To go into more detail on Security Group and NACL: [https://www.youtube.com/watch?v=TtlKFgfN3PU&list=PLdpzxOOAlwvLNOxX0RfndiYSt1Le9azze&index=7](https://www.youtube.com/watch?v=TtlKFgfN3PU&list=PLdpzxOOAlwvLNOxX0RfndiYSt1Le9azze&index=7)

---
