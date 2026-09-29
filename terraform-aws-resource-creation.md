# Difference Between Docker and Kubernetes

- Docker solves the problem of "it works on my machine." It replicates the same environment everywhere, be it in dev, QA, staging, or production.

Now, containers are ephemeral (short-lived) in nature. They can go down because of issues like memory issues, CPU throttling, etc. And the next time a container comes up (because of Docker's restart policy), the IP address of the container changes.

So the biggest problem is that if 2 containers are talking via IP address, then after a restart, the communication will break. This problem, in technical terms, is called **service discovery**. Because of the ephemeral nature of containers, the major problem is service discovery.

And Kubernetes aims to solve this problem.

When we want to run our containers in production, we need a lot of capabilities such as:

- High availability
- Load balancer
- Integration with API gateway
- Strong disaster recovery mechanism

Or a better explanation of what happens when we deploy containers in production:

- Containers can crash (K8s restarts it)
- Servers die (K8s reschedules the containers onto a healthy server)
- When traffic increases or decreases (K8s spins up new servers to increase capacity, or shuts down additional servers to save cost)
- Deploying a new version of a container (K8s rolls it out gradually, killing old ones only once new ones are healthy — zero downtime)
- New version has a bug (K8s rolls back automatically)

Example: one of those servers crashes at 3 AM → someone needs to notice and restart the containers elsewhere.

All of the above tasks might need a human checking manually, so Kubernetes solves these problems without a human babysitting them 24/7.

- New application instance (Pods)

## Difference Between Docker Compose and Kubernetes

- They solve completely different problems.
- Docker Compose runs multiple containers with a configuration file, so instead of running multiple services with multiple commands, we can run all of it with a single command.
- Kubernetes is a container orchestration platform, and it helps solve the different problems suggested above.

---

# How to Work With Kubernetes?

There are multiple ways to get started with Kubernetes.

**a.** You can use a local Kubernetes platform (Minikube, k3s, k3d, kind), which we can install locally on our machine and definitely run for a development use case.

**b.** Another approach is spinning up multiple VMs and installing Kubernetes on these machines using `kubeadm` or other tools — this is a self-managed Kubernetes cluster, for a production use case.

**c.** Another approach is a managed Kubernetes cluster, like AWS EKS (Amazon Elastic Kubernetes Service), Azure Kubernetes Service (AKS), or Google Kubernetes Engine (GKE), for a production use case.

This third approach is very popular, as management of Kubernetes is a huge undertaking. Lots of optimizations come out of the box, like cost optimization and scaling/descaling.

We will go for EKS.

## How We Set Up Kubernetes

- We will set up an EKS cluster using Terraform (Infrastructure as Code / IaC).
- We will not set it up manually, because even in real-time company work, we use tools like Terraform for exactly this purpose.
- This section is super important, even in an interview context.

---

# Infrastructure as Code Using Terraform

- Our goal is to create an EKS cluster using an infrastructure-as-code tool (Terraform) in AWS, within a VPC (Virtual Private Cloud).

## What Exactly Is the Meaning of Infrastructure as Code?

It means we set up our infrastructure — such as servers (EC2 instances) and resources (CPU, memory, etc.) — by writing it in a configuration file, in a language called HashiCorp Configuration Language (HCL).

Even setting up multiple environments is easy with a single command, and we can even share our setup with other teams so they have a similar infrastructure.

IaC is very popular in recent times. Previously it was handled using a UI and/or command-line interface (CLI), but mostly UI. So we can create an AWS instance through the user interface easily — just click 4–5 buttons and we can have the EC2 instance.

But imagine when you're working in an organization and you get hundreds of requests to create EC2 instances. Probably throughout the year, you might get thousands of requests as well.

Now, if you're doing this through the user interface, you will execute the same thing — that is, you will log in to the AWS account, click on the same five buttons, and do the same thing 1,000 times. Maybe every time you try to do it, it will take some 2 to 3 minutes, which is still fair enough.

Another scenario: now imagine, instead of an EC2 instance, someone asks you to spin up/create a full VPC with all the best-practice components — subnets, route tables, internet gateway — and on top of that, an EKS cluster.

Doing this manually through the AWS console, following best practices, could easily take an hour. EKS setup alone takes time. Now say you get 100 similar requests over three months — that's 100 hours, and every time you're reinventing the wheel, or following a document step by step instead of automating it.

This is exactly where Infrastructure as Code became popular — it lets you define your infrastructure as code, the same way you write code or scripts for your applications.

Almost every cloud provider has their own thing, like:

- AWS has CFT (CloudFormation Template), also called CFN (CloudFormation).
- Azure has ARM templates (Azure Resource Manager templates).
- Other clouds also have their own things.

Terraform is popular because it is vendor-neutral. Meaning, you write it in Terraform and it will automate infrastructure on AWS, on Azure, and on Google Cloud Platform. And the best thing is we do not need to learn Terraform for each individual cloud provider — instead, learn Terraform once and it can work for all of the other platforms.

Tomorrow, if there is a new cloud, we can also use the same Terraform to write infrastructure; the only things that will change are the placeholders.

**VS Code extensions needed to write Terraform locally:**

- Terraform (HashiCorp Terraform, for autocomplete)
- YAML (from Red Hat)

## Understanding the Terraform Lifecycle

Like Docker, Terraform also has a lifecycle, and it is categorized into 3 stages:

- `terraform init`
- `terraform plan`
- `terraform apply`

All of this kicks in when we write the Terraform code in HCL (HashiCorp Configuration Language).

Suppose we make a Terraform project folder locally called `eks`, and then create Terraform files (`.tf`) such as `main.tf`.

- First, we run the `terraform init` command to initialize the project. This includes, if we are connecting to AWS, provider-related info or connection-related info; there is also something called a backend, so backend-related info is initialized too. Once `terraform init` is successful, then we fire:

- `terraform plan` → this is similar to a dry run. Once we run this, it will tell us that whatever config we defined in the HCL config file is going to do certain things, like create components of the VPC, create the EKS cluster, etc., if we actually fire the execution command: `terraform apply`.

- `terraform apply` will actually go and create those resources on the specific cloud providers that you got an idea of during the `terraform plan` stage.

When we run `terraform apply`, Terraform will make API calls to AWS and it will create the resources. But for Terraform to make API calls, you should authenticate with AWS. That is, Terraform should be authenticated with AWS, and it will need your AWS user or credentials to work.

So we need to have AWS IAM credentials.

## How We Will Do It

- We will log in with IAM user credentials in AWS.
- On the local machine, we install the AWS CLI tool and run a few commands to configure it by providing user credentials. This creates configuration files somewhere.
- Terraform reads this AWS-CLI-created config file and understands that it needs to use these credentials to make API calls to AWS.

**After logging in to AWS:**

Console sign-in URL:
- `https://078145931846.signin.aws.amazon.com/console`

User name:
- `devops-user`

Console password:
- `devops-learning1#`

And then we click on the top-right Profile menu link, then we see a link "Security credentials", so click on it. And when you scroll down you find "Access Keys", so click on the "Create access key" button and select the "CLI" use case, then click Next.

We plan to use AWS access keys to enable AWS CLI access to our AWS account.

For the next screen, for the Description tag value, just type "Terraform". And it will generate an access key and secret access key.

Do not share these publicly with anyone else — people will be able to access your AWS account with the AWS CLI.

## Download AWS CLI

- Next, install the AWS CLI by searching for it on Google and going to its documentation's install section.

`https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html`

Select: install script (recommended).

And then check on the local machine:

```bash
aws --version   # shows CLI version
```

Also create a directory:

```bash
mkdir eks
```

Next, run:

```bash
aws configure
```

and provide both the access key and secret access key in the terminal.

Now it will create a `.aws` folder in the root, like:

```
/Users/juhigupta/.aws
```

and it has a `credentials` file where all of it is saved, which is read by Terraform when making connection requests.

The above location is read when we fire the `terraform plan` or `terraform apply` commands.

---

# Terraform State File (Brain of Terraform)

Before writing any Terraform files, we need to understand the concept of state-file management in Terraform. First we need to understand what a state file is and how to manage it in Terraform.

It's a very simple concept in Terraform, right?

Let's say you write some Terraform code in `main.tf` to create an S3 bucket in AWS. Then you run `terraform apply`, and Terraform creates that bucket.

Now, Terraform keeps track of what it created in a file called the **state file**. You can think of it as Terraform's memory.

So after creating the bucket, it updates the state file and says: "I created this S3 bucket with this name in this AWS account."

Why is this important?

Because the next time someone runs the same Terraform code, Terraform checks the state file first. It sees that the bucket already exists, so it does not try to create it again.

After two days, a developer updates `main.tf` and adds versioning or a lifecycle rule to the S3 bucket.

Now, when you run `terraform apply`, Terraform does not try to create the bucket again. It checks the state file, sees that the bucket already exists, and finds only the difference.

It understands: "The bucket is already created, but its lifecycle or versioning configuration has changed." So it makes an API call only to update that part.

After the update, Terraform also updates the state file.

So, the state file is basically Terraform's memory. It keeps complete information about resources created on AWS, Azure, or any other provider — such as EC2 instances, S3 buckets, their names, regions, and configurations.

Similarly, if you remove a resource from `main.tf` and run Terraform, it deletes that resource from the cloud and removes its entry from the state file as well.

That is how Terraform keeps track of everything it creates.

## Why Terraform State-File Management Is Necessary

Now let's understand why state-file management is important.

Suppose Abhi creates an EC2 instance and an S3 bucket using `main.tf`. Terraform creates them and stores their details in a local state file on Abhi's machine.

After two days, Dev downloads the same `main.tf` from Git and makes a few changes. But Dev does not have Abhi's local state file.

So when Dev runs `terraform plan` or `terraform apply`, Terraform thinks: "I do not know about any existing EC2 instance or S3 bucket. I need to create them." Even though those resources already exist in AWS.

You may think: why not push the state file to Git along with `main.tf`?

Because the state file can contain sensitive details, such as IP addresses, subnet configuration, load-balancer details, and sometimes secrets. It should not be stored openly in a Git repository.

So there are two problems:

- The local state file is not shared with the team.
- The state file may contain sensitive information.

That is why state-file management is important.

Terraform solves this using a **remote backend** to store state safely in a shared location, and **state locking** to prevent multiple people from changing it at the same time.

```
Solution ── remote backend
         └── state locking
```

---

# Terraform Remote Backend Using an S3 Bucket

In the last lecture, we learned that Terraform's state file is stored locally by default. This becomes a problem when multiple DevOps engineers work on the same infrastructure.

So now let's understand the **remote backend**.

Suppose Abhi creates EC2 and RDS resources using `main.tf`. Before running `terraform apply`, Abhi also configures a remote backend — usually in a file like `backend.tf`.

This tells Terraform: "Create the resources on AWS, but store the state file in an S3 bucket instead of my local machine."

Now the Terraform state is stored centrally in S3. After two days, Dev can clone the same Git repository, including `main.tf` and `backend.tf`.

When Dev runs `terraform plan` or `terraform apply`, Terraform reads the backend configuration, gets the state file from S3, and understands that the EC2 and RDS resources already exist. It only applies Dev's new changes.

So S3 becomes Terraform's shared memory for the whole team. You can also control who can access it using AWS permissions, and use S3 features like versioning.

This solves the shared-state problem. Next, we need to understand **state locking**, which prevents two people from updating the same state at the same time.

---

# Terraform State Locking Using DynamoDB

The remote backend solves the shared-state problem. Everyone can use the same Terraform code and read the same state file from S3.

But why do we still need **state locking**?

Imagine Abhi and Dev both clone the Terraform repository. Both update the EC2 configuration and run `terraform apply` at nearly the same time.

For example, Abhi changes the EC2 volume from 8 GB to 16 GB, while Dev changes it from 8 GB to 30 GB. Both Terraform processes try to update the same resource. So which change should AWS keep?

This is a race condition.

State locking solves it. When Abhi runs `terraform apply` first, Terraform locks the state file. If Dev runs `terraform apply` while Abhi's execution is still running, Terraform tells Dev that the state is locked and asks them to wait.

Once Abhi's changes are complete, Terraform releases the lock. Then Dev can run their changes safely.

On AWS, S3 is commonly used as the remote backend, while DynamoDB has traditionally been used for state locking. Terraform can now also use S3 locking, but DynamoDB is still widely seen in existing setups.

This is important because Terraform changes can take several minutes, especially for resources like VPCs or EKS clusters. During that time, someone else may try to apply changes.

So, in simple terms:

- **S3 remote backend**: shared Terraform memory for the team.
- **State locking**: prevents multiple people from changing that memory at the same time.

---

# Create S3 Buckets and DynamoDB Using Terraform

Let's open Visual Studio Code and go to the `eks` folder we created in the previous lecture.

Now we can start writing the code. Like I told you, you can also create this manually. You don't need Terraform to do this, because this is not part of VPC and EKS creation. But we are doing it just to get more hands-on practice using Terraform.

1. In `/Users/juhigupta/projects/eks`, create an `eks` folder.

   Create a folder `backend` inside `eks`, and a file named `main.tf`.

   Normally, Terraform projects have four common parts:

   - **provider block**: tells Terraform which cloud provider (AWS, Azure, etc.) and region to use.
   - **resource blocks**: define resources such as S3, EC2, or DynamoDB.
   - **variables.tf / terraform.tfvars**: used to pass reusable values to your resource blocks or your actual Terraform file.
   - **outputs.tf**: shows useful output after Terraform runs, such as an IP address.

2. Now search Google for "terraform aws provider" — it will open this link: `https://registry.terraform.io/providers/hashicorp/aws/latest/docs`.

   Check "Terraform 0.12 and earlier" and copy it into `main.tf` as:

   ```hcl
   # 1. Provider block
   # Configure the AWS Provider
   provider "aws" {
     region = "eu-north-1"
   }

   # 2. Resource block
   # Create a VPC
   resource "aws_vpc" "example" {
     cidr_block = "10.0.0.0/16"
   }
   ```

3. Since I need to create an "S3" resource, I will type "S3" in the search box on the top left, and it will display all S3-related results, but we need to look for "S3 (Simple Storage)" and, under this, in the resource subsection, click "aws_s3_bucket".

   On this page, under the "Private Bucket With Tags" heading in the example usage, copy the code and replace the previous resource block in the `main.tf` file, as we are refining our resource block to be more specific — to use S3 itself:

   ```hcl
   resource "aws_s3_bucket" "example" {
     bucket = "my-tf-test-bucket"

     tags = {
       Name        = "My bucket"
       Environment = "Dev"
     }
   }
   ```

## Learn More

Please note that Terraform resource syntax is:

```hcl
resource "<RESOURCE_TYPE>" "<LOCAL_NAME>" {
  ...
}

resource "aws_s3_bucket" "terraform_state" {}
```

- `aws_s3_bucket` is the resource type. It tells Terraform what AWS object or feature to manage.
- `terraform_state` is the local name used inside the Terraform configuration.
- `bucket = "my-tf-test-bucket"` is the actual AWS S3 bucket name.

`<RESOURCE_TYPE>` — these are different Terraform resource addresses, even though they share the local name.

Each resource manages a different aspect of the same physical bucket. So in this example:

```hcl
provider "aws" {
  region = "eu-north-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-123456789012-eu-north-1"

  tags = {
    Name        = "Terraform State"
    Environment = "Shared"
    Purpose     = "Terraform backend state storage"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}
```

Each resource manages a different aspect of the same physical bucket:

- `aws_s3_bucket` — creates the bucket and its basic settings
- `aws_s3_bucket_versioning` — enables object versioning
- `aws_s3_bucket_server_side_encryption_configuration` — enables default encryption
- `aws_s3_bucket_public_access_block` — prevents public access
- `aws_s3_bucket_ownership_controls` — configures object ownership

This reference connects them to the bucket created by the first resource:

```hcl
bucket = aws_s3_bucket.terraform_state.id
```

So the resulting AWS structure is conceptually:

```
One S3 bucket
├── Versioning enabled
├── Encryption enabled
├── Public access blocked
└── Ownership controls configured
```

---

4. Please note that writing these Terraform files by simply copy-pasting from documentation is one way. Another is to make use of GitHub Copilot — enable it as a VS Code extension, and when you start typing "resource" it will show you suggestions, and thus we can write it ourselves, since no one will remember everything by themselves.

   So I update the bucket name to:

   ```hcl
   resource "aws_s3_bucket" "terraform_state" {
     bucket = "demo-terraform-eks-state-bucket"   # <---- I changed the bucket name here.
   }
   ```

   And I will add a lifecycle block here as:

   ```hcl
   resource "aws_s3_bucket" "terraform_state" {
     bucket = "demo-terraform-eks-state-bucket"

     lifecycle {                # <------- Lifecycle added here
       prevent_destroy = false
     }
   }
   ```

   How do we know that we need to add a lifecycle here? We know because we need to learn the cloud products first — only then will we be able to configure things ourselves, like knowing AWS has something called lifecycle, something called versioning, etc.

5. Next, in the docs, search "dynamodb", and click on "Resource: aws_dynamodb_table". Under example usage for "Basic Example", we copy that code into `main.tf`, since AWS has sample code so we copy it from there.

   We will not keep all of that extensive code — we simply keep the basic parts, along with one attribute to define the "lock ids":

   ```hcl
   # "basic-dynamodb-table" is only the name of the resource, not the DynamoDB table name.
   # Same goes for the S3 bucket above.
   resource "aws_dynamodb_table" "basic-dynamodb-table" {
     name         = "terraform-eks-state-lock"   # <--- This is the name of the DynamoDB table
     billing_mode = "PAY_PER_REQUEST"
     hash_key     = "LockId"                     # <-- use this as we are going to do state lock
     range_key    = "GameTitle"

     attribute {
       name = "UserId"
       type = "S"
     }
   }
   ```

   ---
   If you want to call this resource, or if you want to use something from this resource, you will use the resource name. Otherwise, the resource name is not used, but it is only required if you want to call the resource in future lines. It is also mandatory to put a resource name.
   ---

   Next, go to:

   **a.** `cd eks/backend` — check if `main.tf` is here, and if present, fire the next command.

   **b.** `terraform init` — will initialize and create a lock file too.

   ---
   Before running `terraform init`, we need to install it locally on our machine; only then can we fire this command.
   ---

   **c.** `terraform plan` — check this to see if both resources will get created or not. It is a dry-run test before firing `terraform apply`. It will generate logs on the terminal to show us that the resources defined in `main.tf` will get created, or if not, show errors.

   And it showed errors as:

   ```
   Error: all attributes must be indexed. Unused attributes: ["UserId"]
   │ all indexes must match a defined attribute. Unmatched indexes: ["LockId"]
   │
   │   with aws_dynamodb_table.basic-dynamodb-table,
   │   on main.tf line 20, in resource "aws_dynamodb_table" "basic-dynamodb-table":
   │   20: resource "aws_dynamodb_table" "basic-dynamodb-table" {
   ```

   So, in `resource "aws_dynamodb_table" "basic-dynamodb-table"`, `hash_key` and `attribute.name` should be the same:

   ```hcl
   resource "aws_dynamodb_table" "basic-dynamodb-table" {
     name         = "terraform-eks-state-lock"
     billing_mode = "PAY_PER_REQUEST"
     hash_key     = "LockId"       # <<<--- same as attribute.name

     attribute {
       name = "LockId"             # <<<--- same as hash_key
       type = "S"
     }
   }
   ```

   **d.** Now, let's try one more time: `terraform plan`.

   Now errors are fixed, so now we will create the resources by firing the command below:

   **e.** `terraform apply`

   This gives us logs on the terminal as:

   ```
   aws_dynamodb_table.basic-dynamodb-table: Creating...
   aws_s3_bucket.terraform-state-078145931846-eu-north-1: Creating...
   aws_dynamodb_table.basic-dynamodb-table: Still creating... [00m10s elapsed]
   aws_dynamodb_table.basic-dynamodb-table: Creation complete after 12s [id=terraform-eks-state-lock]
   ╷
   │ Error: creating S3 Bucket (demo-terraform-eks-state-bucket): operation error S3: CreateBucket, https response error StatusCode: 409, RequestID: R3BE3YZF8ST2G72Y, HostID: DvBS6pkyTPbU2FA/tg+dyR31J6UFEl9KxoYe80HJgZfRi0wwXBsCJOod+dkSt1Po61jcRdPeA9ZfHpw0CwTi4LSgQ3ypOWMh, BucketAlreadyExists: The requested bucket name is not available. The bucket namespace is shared by all users of the system. Please select a different name and try again.
   │
   │   with aws_s3_bucket.terraform-state-078145931846-eu-north-1,
   │   on main.tf line 11, in resource "aws_s3_bucket" "terraform-state-078145931846-eu-north-1":
   │   11: resource "aws_s3_bucket" "terraform-state-078145931846-eu-north-1" {
   │
   ╵
   ```

   Meaning: DynamoDB is created, BUT the S3 bucket is not created, because of a naming issue, so we need to update the name — this can happen because we probably did not select a unique bucket name, or it existed previously. In our case, it needs to be unique, since no such bucket existed before.

   So we change the `bucket` name to `demo-terraform-eks-state-s3-bucket`, only adding "s3" like this:

   ```hcl
   resource "aws_s3_bucket" "terraform-state-078145931846-eu-north-1" {
     bucket = "demo-terraform-eks-state-s3-bucket"   # <---- Added only "s3" here

     lifecycle {
       prevent_destroy = false
     }
   }
   ```

   **f.** Now run again: `terraform apply`.

   And I still get the same error as above, this time saying the same thing, because any user of AWS S3 anywhere in the world can create any bucket name, but it has to be unique across the world for it to be able to be created.

   So I changed the bucket name after 3 failures to: `demoo-s3-terraform-eks-state-bucket`, and then it worked.

   Please note that the DynamoDB resource was created previously, so this apply will only create the S3 bucket.

---

# Why Use Terraform Modules Instead of Repeating Code?

## VPC + EKS

So in the previous lecture we used the `backend/main.tf` file to write code to create the S3 bucket and DynamoDB table.

Now can we go ahead and just create a new file called `eks/main.tf` (in the project root) and start writing the Terraform code for EKS cluster creation, as well as VPC creation?

That is, just write the provider block again, and this time in the provider block, we will also define the backend configuration — whatever we created previously in `backend/main.tf` — and we will proceed with resource creation for EKS and VPC.

---

Absolutely. We can definitely do that. However, that is not best practice, because whenever you are dealing with Terraform in your organization, one thing you have to remember is you should always go for a modular approach.

So what is a modular approach?

A modular approach is basically common to all programming and scripting languages, where you write your code in modules. Modules are basically reusable items.

---

So if you take our project as an example: using Terraform, we are trying to create a VPC, and within the VPC we are creating EKS (a Kubernetes cluster).

---

Both VPC and EKS are very commonly used resources.

So, as a DevOps engineer on this project, let's say Abhi writes this code for creating a VPC on AWS. In parallel, there can be another DevOps engineer, or even after ten days, Abhi might be asked to create the same VPC for a different development team.

So now, if Abhi writes the same Terraform code again, this becomes duplicate code.

Imagine the number of DevOps engineers in an organization, and everybody writing the same repetitive code. It is a waste of time. To avoid this, every programming language has this concept of modules, functions, or reusable code.

In Terraform, the reusable code — we call it modules.

---

So what will we do as DevOps engineers? First, we will check if there is any module. Now we want to write VPC and EKS, right?

So first, I will check the organizational Terraform code. As a DevOps engineer, you will have a common place, or you will have sync-ups with other DevOps engineers. So you will try to check with them if they have a module for VPC, and if they have a module for EKS.

If they already have one, all you will do is invoke the module (like a function call). If they already have VPC, all you will do is invoke it, the same as in a shell script or any programming language.

How do people/DevOps engineers work in companies?

Even in Terraform, what we will do is: first, we will not start writing the code, but we will check if someone has the modules for it. The common way is that DevOps engineers maintain a Git repository, and in that Git repository they will have all the modules. So they have modules for EKS and VPC, so that any other DevOps engineer within the organization, or somebody new joining, will first check the Git repository.

If it exists, they will invoke that module — I'll show you how to invoke it as well; it's very simple. If it does not exist, they will write the module and push it to the Git repository, so they help other DevOps engineers. In our case, let's assume the module does not exist.

## Project Configuration (Industry Standard)

Inside the `eks` folder, create a `modules` folder, and inside it make folders for `eks` and `vpc`, to have all the code related to EKS/VPC inside it.

And we will make a `main.tf` file in the project root to invoke the modules from there, so our project looks like this:

```
eks/
├── backend/
│   └── main.tf                 # Remote backend configuration
│
├── modules/
│   ├── eks/
│   │   └── main.tf             # Reusable EKS module
│   │
│   └── vpc/
│       └── main.tf             # Reusable VPC module
│
└── main.tf                     # Root configuration that calls VPC and EKS modules
```

---

# Setting Up the VPC Module Using Terraform

## Mental Model

We will write the VPC module, and we will learn how to invoke those modules so that we can create an EKS cluster in an AWS account.

We will write code for the VPC, and within that VPC we will define the EKS configuration, so that by invoking the VPC module, an EKS cluster is created on AWS.

Also, when we write the VPC resource, we need to define all its components, like private subnet, public subnet, Internet Gateway, NAT Gateway, and route tables.

So we will create Terraform resources for:

- VPC resource
- Private subnet resource
- Public subnet resource
- Internet Gateway resource (since the public subnet should be connected to the IGW)
- NAT Gateway resource (since the private subnet should be connected to the NAT)
- Route tables (to associate public subnets with the IGW and private subnets with the NAT)

**Brief note:** for a request to move from the Internet Gateway to the public subnet, we need a route table. Similarly, for a request to move from a private subnet to the NAT Gateway, we need a route table.

Also, VPC is a very commonly created resource in companies, so interviewers also ask these common questions.

## Project Write-Up for VPC

First, create `main.tf`, `variables.tf`, and `outputs.tf` files inside the `/eks-proj/modules/vpc` folder, for defining the VPC module and all its component resources in `main.tf`.

- `variables.tf` — used for defining variables so the code becomes reusable. The same concept exists in JavaScript, shell scripting, Python, etc.
- `outputs.tf` — used to display what it created, on the terminal — like what VPC ID got created, or what the public subnet CIDR range is.

```
eks/
├── backend/
│   └── main.tf               # Remote backend configuration, not needed, can be removed.
│
├── modules/
│   └── vpc/
│       ├── main.tf           # Reusable VPC module
│       ├── variables.tf      # Module input variables
│       └── outputs.tf        # Module output values
│
└── main.tf                   # Root configuration that calls VPC and EKS modules
```

Link for all the Terraform code below:

`https://github.com/iam-veeramalla/ultimate-devops-project-aws/blob/main/section-8/10-vpc-module-code-explanation.md`

**a.** Let's go to the official Terraform documentation here: `https://registry.terraform.io/providers/hashicorp/aws/latest/docs`

and in the filter search bar on the left side, search for "virtual private cloud", check the "VPC resources" section, and inside it click on the `aws_vpc` resource. Copy the examples section and optimize it like this:

```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr  # In variables.tf, add a "cidr_block" variable
  enable_dns_hostnames = true          # enable this
  enable_dns_support   = true          # enable this

  tags = {
    Name = "${var.cluster_name}-vpc"   # give a name to better organize it
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
}
```

Here:

- `aws_vpc` tells Terraform which AWS resource to create: a Virtual Private Cloud.
- `main` is Terraform's local name for this VPC. You can refer to it elsewhere as `aws_vpc.main.id`.
- `cidr_block`: this defines the private IP address range available inside the VPC.

For example, if your variable contains:

```hcl
vpc_cidr = "10.0.0.0/16"
```

Then the VPC can use IP addresses from approximately `10.0.0.0` to `10.0.255.255`.

A `/16` network provides 65,536 total IP addresses. These addresses are later divided into smaller CIDR ranges for public and private subnets.

For example:

```
VPC: 10.0.0.0/16

Public subnet:  10.0.1.0/24
Private subnet: 10.0.2.0/24
Private subnet: 10.0.3.0/24
```

The VPC CIDR is like the full land area, while subnets are smaller sections created within that land.

- `enable_dns_support = true` — this enables DNS resolution inside the VPC. It means resources in the VPC can resolve domain names into IP addresses. It is especially important when your applications need to communicate using service names instead of hard-coded IP addresses. For Kubernetes, this is important because Pods and services commonly use DNS names to find each other.

- `enable_dns_hostnames = true` — this allows AWS to assign DNS hostnames to instances that receive public IP addresses. For example, an EC2 instance with a public IP may receive a hostname similar to `ec2-18-123-45-67.eu-west-1.compute.amazonaws.com`. This is useful when you need AWS-provided DNS names for public resources such as bastion hosts or public EC2 instances. This setting depends on DNS support being enabled, so usually both are set to `true`.

- `tags = { ... }` — tags are key-value labels attached to AWS resources. They help identify, organize, filter, automate, and manage resources.

  `kubernetes.io/cluster/my-eks-cluster = shared`

  This creates a Kubernetes/EKS-related tag. It tells Kubernetes-related AWS components that this VPC can be used by that cluster. `shared` means the VPC is shared by the Kubernetes cluster and other AWS resources. It does not mean the VPC is public or shared with other AWS accounts.

**b.** Then, from the documentation, search for "Resource: aws_subnet" and copy and adjust it like this:

```hcl
resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name                                         = "${var.cluster_name}-private-${count.index + 1}"
    "kubernetes.io/cluster/${var.cluster_name}"  = "shared"
    "kubernetes.io/role/internal-elb"            = "1"
  }
}
```

- Creates multiple private subnets based on `private_subnet_cidrs`.
- Each subnet is assigned an availability zone from `availability_zones`.
- Tags define Kubernetes cluster association and internal load balancer role.

This block creates multiple private subnets inside the VPC created earlier. A subnet is a smaller IP-address range within a VPC.

We commonly create private subnets in multiple Availability Zones so the application remains available even if one AWS data center has an issue.

`resource "aws_subnet" "private"`:

- `aws_subnet` is the AWS resource Terraform will create.
- `private` is Terraform's local name for this group of subnets.

Because `count` is used, Terraform creates several subnets rather than just one.

For example, if it creates two subnets, you reference them like this:

```hcl
aws_subnet.private[0].id
aws_subnet.private[1].id
```

`count = length(var.private_subnet_cidrs)`

`count` tells Terraform how many copies of this resource to create.

Suppose the variable is:

```hcl
private_subnet_cidrs = [
  "10.0.11.0/24",
  "10.0.12.0/24"
]
```

The `length()` of this list is 2, so Terraform creates two private subnets.

Terraform runs the block twice:

| Terraform index | Subnet created |
|---:|---|
| `0` | First private subnet |
| `1` | Second private subnet |

`vpc_id = aws_vpc.main.id`:

This places every subnet inside the VPC created by this resource: `aws_vpc.main`.

`.id` means the actual AWS VPC ID, something like `vpc-0123456789abcdef0`.

Terraform automatically understands that it must create the VPC first, and only then create these subnets.

`cidr_block = var.private_subnet_cidrs[count.index]`:

This gives each subnet its own IP range.

`count.index` is the current loop index:

- First run: `count.index` is 0
- Second run: `count.index` is 1

With this configuration:

```hcl
private_subnet_cidrs = [
  "10.0.11.0/24",
  "10.0.12.0/24"
]
```

Terraform produces:

```
private[0] → 10.0.11.0/24
private[1] → 10.0.12.0/24
```

A `/24` subnet has 256 IP addresses in total. AWS reserves five IP addresses in every subnet, so normally 251 can be assigned to resources. The subnet CIDRs must be inside the VPC CIDR and must not overlap with each other.

`availability_zone = var.availability_zones[count.index]`:

This places each private subnet in a different Availability Zone.

For example:

```hcl
availability_zones = [
  "eu-west-1a",
  "eu-west-1b"
]
```

Terraform matches the lists using the same index:

| Index | CIDR | Availability Zone |
|---:|---|---|
| `0` | `10.0.11.0/24` | `eu-west-1a` |
| `1` | `10.0.12.0/24` | `eu-west-1b` |

So the final structure is:

```
VPC
├── Private subnet 1: 10.0.11.0/24 in eu-west-1a
└── Private subnet 2: 10.0.12.0/24 in eu-west-1b
```

The order of `private_subnet_cidrs` and `availability_zones` therefore matters. They should contain the same number of items. Otherwise, Terraform will fail when it tries to access an index that does not exist.

### Why Are These Called Private Subnets?

Nothing in this specific Terraform block technically makes the subnet private.

A subnet becomes private when its route table does not send internet traffic directly to an Internet Gateway.

Typically, a private subnet looks like:

```
Private EC2 / EKS node
        ↓
NAT Gateway
        ↓
Internet Gateway
        ↓
Internet
```

This allows outbound access — for package downloads or third-party APIs — but prevents the internet from directly initiating a connection to the EC2 instances or Pods.

The route table configuration, usually defined elsewhere, is what makes these subnets private.

`"kubernetes.io/role/internal-elb" = "1"`

This is especially important for EKS. It tells Kubernetes/AWS Load Balancer Controller that this subnet can be used to create an internal load balancer. An internal load balancer is reachable only from within the VPC, VPN, Direct Connect, or connected networks — not directly from the public internet.

```
Internet
   ✗ cannot access

Internal application / private network
   ✓ can access
        ↓
Internal Load Balancer
        ↓
EKS application pods
```

It does not assign a technical AWS "role" to the subnet by itself. A subnet is still just a subnet.

The tag is metadata that Kubernetes/EKS-aware tooling reads when it needs to create a load balancer. For example, the Kubernetes cloud provider or AWS Load Balancer Controller can discover: "This subnet is intended for internal load balancers."

So it has no effect unless a Kubernetes/AWS integration actually uses it. But when that integration reads it, it can influence where the load balancer is created.

Yes — a public-facing load balancer should be placed in public subnets. But not every load balancer should be public.

| Load balancer type | Subnet placement | Who can access it? | Typical use |
|---|---|---|---|
| Internet-facing | Public subnets | Public internet | Website, public API |
| Internal | Private subnets | VPC and connected private networks | Internal APIs, admin tools, microservices |

An internal load balancer is useful when the service must be reachable only inside your network.

```
Internet
   ↓
Public Load Balancer
   ↓
Frontend / public API
   ↓
Internal Load Balancer
   ↓
Payments, orders, user-profile services
```

So, public subnets are for a load balancer that accepts traffic from the internet. Private subnets are for a load balancer that accepts traffic only from inside the VPC, or from connected networks such as a VPN or another VPC.

**c.** Next, create a public subnet — at least give it a public name for local Terraform purposes.

```hcl
resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  map_public_ip_on_launch = true   # This is needed

  tags = {
    Name                                         = "${var.cluster_name}-public-${count.index + 1}"
    "kubernetes.io/cluster/${var.cluster_name}"  = "shared"
    "kubernetes.io/role/elb"                     = "1"
  }
}
```

`map_public_ip_on_launch = true`: this is needed for assigning public IP addresses to instances on launch.

```hcl
tags = {
  "kubernetes.io/role/elb" = "1"
}
```

Here, we have not given `internal-elb` in the metadata, as in the private subnet case:

- Private subnet: `"kubernetes.io/role/internal-elb" = "1"`
- Public subnet: `"kubernetes.io/role/elb" = "1"`

The rest remains the same.

**d.** Next, create an Internet Gateway like this:

```hcl
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.cluster_name}-igw"
  }
}
```

Creates an Internet Gateway to enable internet access for public subnets.

**e.** Let's create a route table for mapping public subnets with the Internet Gateway:

```hcl
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id   # Route table is created within the VPC

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.cluster_name}-public"
  }
}
```

A route table is like a traffic-direction map. When a resource sends network traffic, AWS checks the route table attached to its subnet and asks: "Where should I send this traffic?"

The route block:

```hcl
route {
  cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.main.id
}
```

This adds a route that says: "For traffic going to any IPv4 address outside this VPC, send it to the Internet Gateway."

`0.0.0.0/0` means all IPv4 addresses. It is called the default route because it matches anything not covered by a more specific route.

Please note: this Terraform block only creates the route table. It does not yet attach it to any subnet — usually another resource, `aws_route_table_association`, does that. Once associated, the subnet becomes a public subnet from a routing point of view.

**Why does this make it a public route table?**

A subnet is considered public when its route table has a route like this:

```
0.0.0.0/0 → Internet Gateway
```

**Important:** a public route does not automatically make an EC2 instance public.

For an EC2 instance to be reachable from the internet, it also needs:

- A public IPv4 address or Elastic IP
- A Security Group allowing the required inbound port, such as 80 or 443
- If applicable, NACL rules that allow the traffic

So this route table allows a path to the internet, but it does not by itself expose every resource in the subnet.

**f.** Let's attach the above public route table to the above public subnet with this resource:

```hcl
resource "aws_route_table_association" "public" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
```

This block attaches the public route table to each public subnet.

Creating a route table alone does nothing until you associate it with a subnet. This association is what tells AWS: "Resources in this subnet must follow the rules in this route table."

`count = length(var.public_subnet_cidrs)`: it gives the maximum number of times the loop should run.

For example:

```hcl
public_subnet_cidrs = [
  "10.0.1.0/24",
  "10.0.2.0/24"
]
```

and `subnet_id` is, for a specific run, the matching public subnet — for the 0th run, `subnet_id` is `10.0.1.0/24`; for the 1st run, `subnet_id` is `10.0.2.0/24`.

Also, keep in mind that `count.index` gives the current run's index.

`route_table_id = aws_route_table.public.id`: this simply refers to the route table created earlier.

Terraform creates two associations:

```
Association 1 → public subnet 1
Association 2 → public subnet 2
```

**g.** Next, we will do the same steps for private subnets too, meaning:

- Creating the private route table
- We already created the private subnet
- We will create the NAT Gateway (similar to the Internet Gateway previously)
- And create the associations between private subnets and the NAT Gateway using the private route table

```hcl
resource "aws_eip" "nat" {
  count  = length(var.public_subnet_cidrs)
  domain = "vpc"

  tags = {
    Name = "${var.cluster_name}-nat-${count.index + 1}"
  }
}

resource "aws_nat_gateway" "main" {
  count         = length(var.public_subnet_cidrs)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "${var.cluster_name}-nat-${count.index + 1}"
  }
}

resource "aws_route_table" "private" {
  count  = length(var.private_subnet_cidrs)
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = {
    Name = "${var.cluster_name}-private-${count.index + 1}"
  }
}

resource "aws_route_table_association" "private" {
  count          = length(var.private_subnet_cidrs)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}
```

Elastic IPs (EIPs) are created for the NAT gateways. NAT gateways allow private subnet instances to access the internet securely. Each NAT Gateway is associated with a public subnet.

Please note that we have created an additional resource, `aws_eip`, for the Elastic IPs used by the NAT gateways.

Populate `variables.tf` from here:
`https://github.com/iam-veeramalla/ultimate-devops-project-aws/blob/eks-install/eks-install/modules/vpc/variables.tf`

## Populate outputs.tf

We want to see the VPC ID, private subnet IDs, and public subnet IDs being generated as logs when our Terraform code runs:
`https://github.com/iam-veeramalla/ultimate-devops-project-aws/blob/eks-install/eks-install/modules/vpc/outputs.tf`

```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}
```

Once it executes the complete `terraform apply` command, it will look at your `outputs.tf` file, where you are asking for the VPC ID, and you are providing the value as `aws_vpc.main.id`.

So it will go to `main.tf`, go to the AWS VPC `main` resource, and its ID. It will also get this information from the state file, and it is going to print that on your terminal.

That's it — we were able to finish writing the VPC module.

---

# Setting Up the EKS Module Inside the VPC Using Terraform

Setting up the EKS module is much simpler than the VPC module, as the VPC module has a lot more components than EKS.

For setting up the EKS cluster, what do we need?

We need 2 IAM roles:

- One for the cluster (control plane) — the master component
- One for the nodes (data plane) — the node component

Simply creating roles means nothing unless we associate a policy with it, and only then does it get permissions.

**Step 1:** We create the IAM roles, then we attach the policy to the IAM role.

```
IAM role → cluster → policy attach
IAM role → node    → policy attach
```

**Step 2:** We will create the EKS cluster, which completes the control plane.

```
IAM role → cluster + EKS cluster → Master component
```

**Step 3:** Create the IAM role for the node + policy attach (which we already did in step 1), and just create the node group and attach it to the EKS cluster.

So we need to write all of this in 6 resource blocks in our Terraform module file for EKS, that's it:

- 2 IAM roles creation
- 2 policy attachments to the IAM roles
- EKS cluster creation + node group creation & attach

## Write the EKS Cluster in the Project

In the project, inside the `modules` folder, create an `eks` folder, and inside it create `main.tf`, `variables.tf`, and `outputs.tf` files, like this:

```
eks/
│
├── modules/
│   └── eks/
│       ├── main.tf           # Reusable EKS module
│       ├── variables.tf      # Module input variables
│       └── outputs.tf        # Module output values
│
│   └── vpc/
│
└── main.tf                   # Root configuration that calls VPC and EKS modules
```

Let's go to the official Terraform documentation and search for "kubernetes". Within the section "EKS (Elastic Kubernetes) resources", click on `aws_eks_cluster`.

Then copy the IAM role resource (`aws_iam_role`) first from there:

```hcl
resource "aws_iam_role" "cluster" {
  name = "${var.cluster_name}-cluster-role"   # <---- EKS cluster name should come from variable

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      },
    ]
  })
}
```

Step 1 is done.

Let's go to step 2, where we need to create a policy and attach it to this IAM role. The resource name is `aws_iam_role_policy_attachment`:

```hcl
resource "aws_iam_role_policy_attachment" "cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster.name
}
```

So `policy_arn` is the permission we are attaching to the cluster role (`aws_iam_role.cluster.name`).

So step 2 is done.

Next, let's go to step 3: create the EKS cluster with the roles above (with attachments). This EKS cluster will be within a VPC and belong to subnets.

So the resource name is `aws_eks_cluster`:

```hcl
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name     # <---- Provide the name of the EKS cluster
  version  = var.cluster_version  # <---- Which version of EKS you want to install
  role_arn = aws_iam_role.cluster.arn  # <-- Assign the cluster role we created above

  vpc_config {
    subnet_ids = var.subnet_ids
  }

  depends_on = [
    aws_iam_role_policy_attachment.cluster_policy
  ]
}
```

Now we are done with the master components — steps 1, 2, and 3 are done.

Let's go for IAM role creation, but this time for the worker node.

```hcl
resource "aws_iam_role" "node" {
  name = "${var.cluster_name}-node-role"   # <---- EKS cluster name should come from variable

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}
```

So we are telling EC2 that it should assume this role for the node worker, and `assume_role_policy` reflects it. We can also have Fargate assume the role of a node worker, which we did not configure above.

Next, we will attach this role with attachments:

```hcl
resource "aws_iam_role_policy_attachment" "node_policy" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodeMinimalPolicy",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
  ])
  policy_arn = each.value
  role       = aws_iam_role.node.name
}
```

Here we are granting more permissions to the worker node (3 permissions):

- EC2 Container Registry
- Container Network Interface (CNI)
- EKS worker node policy

Finally, we create the EKS node group using the resource `aws_eks_node_group`, and we have written a simple loop, since there will be multiple worker nodes.

If it is a single worker node, we do not need a `for_each` loop. And we have provided, in the variables, how many worker nodes we need.

```hcl
resource "aws_eks_node_group" "main" {
  for_each = var.node_groups

  cluster_name    = aws_eks_cluster.main.name
  node_group_name = each.key
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = var.subnet_ids

  instance_types = each.value.instance_types
  capacity_type  = each.value.capacity_type

  scaling_config {
    desired_size = each.value.scaling_config.desired_size
    max_size     = each.value.scaling_config.max_size
    min_size     = each.value.scaling_config.min_size
  }

  depends_on = [
    aws_iam_role_policy_attachment.node_policy
  ]
}
```

We needed here:

- Cluster name, node group name, permission through `node_role_arn`
- Subnet IDs
- Instance types, capacity, and scaling config as variables

A node group is a managed set of EC2 instances that join your EKS cluster and run Kubernetes Pods.

You define the desired configuration; AWS manages the worker machines behind it.

`for_each = var.node_groups`: this creates one node group for every entry in the `node_groups` map you defined earlier. For example:

```hcl
node_groups = {
  general = {
    instance_types = ["t3.medium"]
    capacity_type  = "ON_DEMAND"

    scaling_config = {
      desired_size = 2
      min_size     = 1
      max_size     = 4
    }
  }

  workers = {
    instance_types = ["t3.large"]
    capacity_type  = "SPOT"

    scaling_config = {
      desired_size = 1
      min_size     = 0
      max_size     = 5
    }
  }
}
```

`subnet_ids = var.subnet_ids`: this decides where AWS creates the EC2 worker nodes.

Normally, `var.subnet_ids` contains private subnet IDs from two or more Availability Zones:

```hcl
subnet_ids = [
  "subnet-aaa111",
  "subnet-bbb222"
]
```

AWS can then place worker nodes across these subnets for better availability.

Private subnets are usually preferred, because the worker nodes should not be directly reachable from the internet. They can still make outbound requests through a NAT Gateway when required.

```hcl
scaling_config = {
  desired_size = 2
  min_size     = 1
  max_size     = 4
}
```

The meaning is:

- EKS starts with a target of 2 nodes.
- It must retain at least 1 node.
- It can grow to at most 4 nodes.

One important detail: these values set the limits, but they do not automatically scale nodes just because CPU is high. For dynamic scaling, you also need a Kubernetes-aware component such as Cluster Autoscaler or Karpenter. It watches for Pods that cannot be scheduled and requests more nodes within the `min_size` and `max_size` limits.

## For outputs.tf

In VPC, we wanted the VPC ID, and the public and private subnet IDs. Here, let's say I just want to see the EKS cluster endpoint — that is, the master component (control plane) endpoint — and the cluster name too:

```hcl
output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.main.name
}
```

We populate `modules/eks/variables.tf` from this:
`https://raw.githubusercontent.com/iam-veeramalla/ultimate-devops-project-aws/refs/heads/eks-install/eks-install/modules/eks/variables.tf`

Here, the noteworthy thing is the `node_groups` variable:

```hcl
variable "node_groups" {
  description = "EKS node group configuration"

  type = map(object({
    instance_types = list(string)
    capacity_type  = string
    scaling_config = object({
      desired_size = number
      max_size     = number
      min_size     = number
    })
  }))
}
```

`map()` — a map is a collection of named values:

```hcl
node_groups = {
  general = { ... }
  workers = { ... }
}
```

Here, `general` and `workers` are keys. You choose these names yourself. `object({})` defines many properties.

Please note that `variables.tf` just types the variable's description and type, but not the actual values. The actual values are normally provided in `terraform.tfvars`.

## Execution of the Above EKS Module Code

If you try to execute this EKS module code, it cannot be executed, because this is a module.

A module is just reusable code, like a function in your shell script.

Unless someone invokes the function — whether it's a shell script, Python, or otherwise — if you just write a function and nobody invokes it, it becomes wasted code, or it is just waiting for someone to invoke that function.

At the end of the day, it's like defining a function, which needs to be called.

Now, in the root of the project, we need to create `main.tf`, `variables.tf`, and `outputs.tf`, and this is the main program that we are writing:

```
eks/
├── backend/
│
├── modules/
│   └── eks/
│
│   └── vpc/
│
└── main.tf                   # Root configuration main file that calls VPC and EKS modules
└── variables.tf              # Root configuration variables file
└── outputs.tf                # Root configuration output file
```

## Write Code for Execution in the Root `main.tf` File

Because we have already written the modules, this root configuration (`main.tf`) is now only around 15–20 lines. Most of the actual work is already handled inside the modules.

If your organization allows it, you can also use public Terraform modules from GitHub instead of writing hundreds of lines of code yourself.

However, if public modules are not allowed, then as a DevOps engineer, you should create and maintain your own modules, just like we did in the previous lecture.

Now, let's start writing the actual code to create the VPC and EKS resources on AWS.

**Step 1:**

First, we write the backend configuration, because we want to use a remote backend — that is, the S3 bucket that we created using the backend configuration defined previously in the `backend/` folder. We can do this manually too, but we did it this way to show more Terraform usage. In this project, we can even remove it, since that `backend/` folder is not part of this project itself.

So in the project root `eks/main.tf` file, we define 2 things:

- Required providers, such as `aws`, `google cloud`, or `azure`, etc.
- Backend configuration for the state file (S3) and state lock (DynamoDB)

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "demoo-s3-terraform-eks-state-bucket"  # <- change it with your bucket name
    key            = "terraform.tfstate"
    region         = "eu-north-1"                            # <- change it with your region
    dynamodb_table = "terraform-eks-state-lock"
    encrypt        = true
  }
}
```

Go to AWS → S3, then copy the bucket name and paste it into this `backend "s3"` block.

The `key` (`"terraform.tfstate"`) is the name of the Terraform state file.

The `region` (`"eu-north-1"`) is where I am located, so I will have low latency, so I chose it.

Also, go to AWS → DynamoDB tables and pick the already-created DynamoDB table name, and paste it into the `dynamodb_table` field above.

**Step 2:**

Let's define the provider block for the AWS region:

```hcl
provider "aws" {
  region = var.region   # <- define this value in variables.tf
}
```

Also, we define the modules we want to invoke:

```hcl
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  private_subnet_cidrs = var.private_subnet_cidrs
  public_subnet_cidrs  = var.public_subnet_cidrs
  cluster_name         = var.cluster_name
}
```

`source` (`"./modules/vpc"`) is the location of the module; it can even be a Git repository:

```hcl
source = "git::https://github.com/your-org/terraform-aws-vpc.git?ref=v1.2.0"
```

Here:

- `git::` tells Terraform that the source is a Git repository.
- `https://github.com/your-org/terraform-aws-vpc.git` is the repository containing the module.
- `?ref=v1.2.0` pins the module to a Git tag. This is recommended, so a future change in the repository does not unexpectedly affect your infrastructure.

Also, we defined the variables used in the VPC module's values through other variables, like this:

```hcl
vpc_cidr             = var.vpc_cidr
availability_zones   = var.availability_zones
private_subnet_cidrs = var.private_subnet_cidrs
public_subnet_cidrs  = var.public_subnet_cidrs
cluster_name         = var.cluster_name
```

We could have provided an actual value here, but we intentionally kept a variable to make it reusable, and we define its value in the root `variables.tf` file.

Tomorrow, if we need to invoke another VPC module, the only thing we need to change is `source`, and that's it.

---
Also, I'm stressing this a lot, because module invocation is something your interviewers will be interested in. "Where are your modules stored?" So you can say: as a DevOps engineer, we have a centralized repository within our organization where we store all the modules, like EKS and VPC, and we source them, if project A, B, or C needs that module.
---

So above we have 2 things:

- How we invoke a module
- The variables we need to pass

**Step 3:**

Let's invoke the EKS module, as we have done above:

```hcl
module "eks" {
  source = "./modules/eks"   # <-- Location of module

  # variables needed to invoke the module above
  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  node_groups     = var.node_groups
}
```

Define the root project's `variables.tf` from here:
`https://github.com/iam-veeramalla/ultimate-devops-project-aws/blob/eks-install/eks-install/variables.tf`

Finally, define what we want to see in the terminal for `outputs.tf`, from here:
`https://github.com/iam-veeramalla/ultimate-devops-project-aws/blob/eks-install/eks-install/outputs.tf`

**Step 5:**

Let's go to the project folder root (`/Users/juhigupta/projects/eks`) and run this command from the terminal:

```bash
terraform init
```

Next, run:

```bash
terraform plan
```

And this created an error, because Terraform no longer supports DynamoDB locking. It says:

```
Locking can be enabled via S3 or DynamoDB. However, DynamoDB-based locking is deprecated
and will be removed in a future minor version.
```

For enabling S3 state locking, use `use_lockfile: true`. Put it in step 1, as:

```hcl
backend "s3" {
  bucket         = "demoo-s3-terraform-eks-state-bucket"  # <- change it with your bucket name
  key            = "terraform.tfstate"
  region         = "eu-north-1"                            # <- change it with your region
  # dynamodb_table = "terraform-eks-state-lock"             <--- no longer needed, remove it
  use_lockfile   = true
  encrypt        = true
}
```

Link: `https://developer.hashicorp.com/terraform/language/backend/s3`

So reconfigure the init as:

```bash
terraform init -reconfigure
```

Next, run:

```bash
terraform plan
```

It says 32 resources are going to be created, and there are no errors in the terminal.

Next, run:

```bash
terraform apply
```

I will also say "yes", and it will take close to 20–30 minutes. Once it is done, we will go to the AWS UI and verify it.

It created some resources, and some failed.

The apply partially succeeded:

- VPC, subnets, Internet Gateway, IAM roles, EIPs, and three NAT gateways: created
- EKS cluster `my-eks-cluster`: created
- Node group `general`: failed; no worker EC2 nodes were created

Terraform does not roll back successful resources after a later resource fails.

The specific cause is:

```
InvalidParameterException: Requested AMI for this version 1.30 is not supported
```

In `variables.tf`:

```hcl
variable "cluster_version" {
  default = "1.34"   # <-- previously it was 1.30, which is now obsolete
}
```

And run this to destroy all of the partial resource creation:

```bash
terraform destroy
```

Then run:

```bash
terraform apply
```

to recreate everything, as we want either to create everything or, in case of error, fix the error, destroy the existing resources, and recreate everything.

With a few errors sorted out using ChatGPT, it's finally fixed, and on the terminal it displays:

```
Outputs:

cluster_endpoint = "https://6DA2F3FC5EAD2B0CFF5F6B3C67B3661B.gr7.eu-north-1.eks.amazonaws.com"
cluster_name = "my-eks-cluster"
vpc_id = "vpc-03223fadfd6af4554"
```

## Verifying the VPC and EKS Resources

- Let's go to AWS and search for "EKS" to check if the EKS cluster is created or not. We see that "my-eks-cluster" is the name of the cluster that got created, and its version is 1.34.

- Upon clicking on the above cluster, inside it, if we check the "Networking" section, then I see:

  - VPC (`vpc-03223fadfd6af4554`), to check the created VPC. Until this point, we see the cluster got created, and the VPC got created.

  - If we click on the above VPC link, then we see all the resources — private/public subnets, route tables — that we asked AWS to create.

  We see 3 Availability Zones, and one private/public subnet in each zone, which is best practice. Similarly, we see one Internet Gateway for all public subnets, and one NAT Gateway for each private subnet.

---

# Relationship Between Subnets, Worker EC2 Instances, Node Groups, Etc.

Your current configuration creates:

| Item | Count | How it is decided |
|---|---:|---|
| Availability Zones | 3 | Three entries in `availability_zones` |
| Private subnets | 3 | Three entries in `private_subnet_cidrs` |
| Public subnets | 3 | Three entries in `public_subnet_cidrs` |
| Total subnets | 6 | 3 private + 3 public |
| Node groups | 1 | One entry: `general` in `node_groups` |
| Worker instances (initially) | 2 | `general.scaling_config.desired_size = 2` |

The subnet-to-AZ relationship is based on matching list positions:

| AZ | Private subnet | Public subnet |
|---|---|---|
| `eu-north-1a` | `10.0.1.0/24` | `10.0.4.0/24` |
| `eu-north-1b` | `10.0.2.0/24` | `10.0.5.0/24` |
| `eu-north-1c` | `10.0.3.0/24` | `10.0.6.0/24` |

In simple terms: you chose 3 Availability Zones, then created one private and one public subnet in each zone. This gives your cluster high availability: if one AZ has a problem, workloads can run in the others.

Your EKS worker nodes use all three **private** subnets. Terraform does not say "put exactly X instances in each subnet." Instead, the `general` node group asks AWS for:

- Minimum: 1 instance
- Desired: 2 instances
- Maximum: 4 instances
- Instance type: `t3.micro`
- Purchase option: On-Demand

So initially, AWS creates two worker EC2 instances and places them across the eligible private subnets. You should not assume exactly one instance per subnet — AWS controls the exact placement. With 2 instances and 3 private subnets, one subnet may have no worker node at a given moment.

You currently have one node group, called `general`:

```
EKS cluster
└── Node group: general
    ├── desired instances: 2
    ├── minimum instances: 1
    └── maximum instances: 4
```

You can add more node groups by adding more entries to the `node_groups` map. For example, one group for general workloads and another for compute-heavy workloads:

```hcl
node_groups = {
  general = {
    instance_types = ["t3.micro"]
    capacity_type  = "ON_DEMAND"
    scaling_config = {
      desired_size = 2
      min_size     = 1
      max_size     = 4
    }
  }

  compute = {
    instance_types = ["t3.large"]
    capacity_type  = "ON_DEMAND"
    scaling_config = {
      desired_size = 1
      min_size     = 1
      max_size     = 3
    }
  }
}
```

That would create two node groups, with independent instance types and scaling limits. Terraform itself does not set a fixed maximum number of node groups; the practical limit is AWS's EKS service quota.

---

# Relationship Between Subnets and Route Tables

In your Terraform code, there are **4 custom route tables** for the 6 subnets:

| Subnet type | Number of subnets | Route tables | Relationship |
|---|---:|---:|---|
| Public | 3 | 1 | All public subnets share one public route table |
| Private | 3 | 3 | Each private subnet gets its own private route table |
| **Total** | **6** | **4** | |

The relationship is:

```
Public subnets
├── public subnet 1 (eu-north-1a) ─┐
├── public subnet 2 (eu-north-1b) ─┼── public route table
└── public subnet 3 (eu-north-1c) ─┘       │
                                            └── Internet Gateway
```

All public subnets can use the same route table because they all need the same rule:

```
Internet traffic (0.0.0.0/0) → Internet Gateway
```

For private subnets:

```
private subnet 1 (eu-north-1a) → private route table 1 → NAT Gateway 1
private subnet 2 (eu-north-1b) → private route table 2 → NAT Gateway 2
private subnet 3 (eu-north-1c) → private route table 3 → NAT Gateway 3
```

Each private subnet has its own route table, because your code creates one NAT Gateway per public subnet/AZ, then routes each private subnet through the NAT Gateway in its matching AZ.

1 public subnet will have 1 NAT Gateway.

So the full setup is:

```
3 public subnets  → 1 shared public route table → Internet Gateway
3 private subnets → 3 private route tables       → 3 matching NAT Gateways
```

AWS also automatically creates a default/main route table whenever a VPC is created. But your Terraform configuration explicitly creates and associates the four route tables above, so those are the ones your six subnets actually use.

---

# Few Questions

**1. Does a VPC have multiple public subnets, or is only one public subnet needed?**

A VPC can have many public subnets. It is not limited to one.

For a highly available EKS setup, a common design is one public subnet per Availability Zone:

```
AZ-a: public subnet + private subnet
AZ-b: public subnet + private subnet
AZ-c: public subnet + private subnet
```

Public subnets normally hold internet-facing components, such as public load balancers and NAT gateways. In your configuration, each public subnet also gets its own NAT Gateway.

You could use only one public subnet, but then a NAT Gateway or public load balancer in that AZ becomes a single point of failure. It is cheaper, but less resilient.

**2. If we use 2 node groups, it simply means 2 groups of worker nodes are connected to the EKS cluster, and each node group can have many instances, no?**

Yes, two node groups mean two separate groups of worker-node EC2 instances connected to the same EKS cluster.

Small terminology correction: a worker node is an EC2 instance. A node does not contain many instances.

```
One EKS cluster
├── general node group
│   └── EC2 worker nodes: e.g. 2–4 t3.micro instances
└── compute node group
    └── EC2 worker nodes: e.g. 1–3 c6i.large instances
```

Each node can run multiple Kubernetes Pods (your applications/containers).

**3. Also, as explained above, if we have 2 node groups — one for general and one for compute — does AWS automatically shift heavy computing activity into that node group? Basically, explain why, or in what situation this would be useful.**

AWS/Kubernetes will not automatically understand that a workload is "heavy" and move it to the compute group. You must tell Kubernetes where a workload should run.

Separate node groups are useful when workloads need different kinds of machines:

- `general`: small, lower-cost instances for normal APIs, web apps, background jobs, etc.
- `compute`: faster CPU instances for data processing or CPU-heavy jobs.
- Another group could use memory-optimized instances for databases/caches.
- Another could use GPU instances for AI/ML.
- A Spot node group can run fault-tolerant, cheaper workloads.

You normally direct a Pod to the appropriate node group using node labels, plus `nodeSelector` or node affinity. For example:

```
general workloads → general node group
heavy batch job   → compute node group
```

The Kubernetes scheduler then places the Pod only on nodes matching that rule. Autoscaling can add more nodes to that particular group if it runs out of capacity.

So a Kubernetes manifest file can specify if we want a particular Pod to run on a particular node group.

**4. How will we decide how many private subnets to keep in an EKS cluster, and what is the private-subnet-to-public-subnet ratio or relationship generally?**

Decide the number of private subnets mainly based on the number of Availability Zones you want to use.

A straightforward EKS production pattern is:

```
3 Availability Zones
→ 3 private subnets, one in each AZ
→ 3 public subnets, one in each AZ
```

Private subnets are where your EKS worker nodes and Pods run. They are not directly reachable from the internet. Public subnets are for internet-facing load balancers and NAT gateways.

There is no mandatory universal private-to-public subnet ratio. The common high-availability relationship is 1 private subnet and 1 public subnet per AZ, which is exactly what your code currently creates.

Your current setup is:

```
3 AZs
├── 3 private subnets: worker nodes and Pods
└── 3 public subnets: NAT gateways and public load balancers
```

You also choose private subnet size based on expected node and Pod IP usage. With the AWS VPC CNI, Pods receive VPC IP addresses, so private subnets need enough IP addresses for both worker nodes and Pods. Your `/24` private subnets each have roughly 251 usable IP addresses, which is a reasonable small-to-medium starting point.

---

## Side Note

- Zsh (Z Shell) and Bash (Bourne Again SHell) are both shells, not terminals.
- macOS uses Zsh by default.
- The terminal is just the container, and the shell is the actual program executing the commands.

---

## Next

We will study deployment of the project to Kubernetes and see this in another markdown file.
