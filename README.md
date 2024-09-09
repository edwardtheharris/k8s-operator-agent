---
abstract: >-
   Kubernetes Operator Agent is a LLM agent that is deployed as an operator
   in Kubernetes.
authors:
   - name: Xander Harris
     email: xandertheharris@gmail.com
date: 2024-08-04
title: Readme
---

Kubernetes Operator Agent

## Development

This project uses [Skaffold](https://skaffold.dev/) and [Helm](https://helm.sh/)
for development. Please make sure you have them installed on your machine.

### Prerequisites

1. Access to a running Kubernetes cluster or the ability to create one.
2. Python
3. LangChain
4. Helm

### Bare Metal Deployment

The process for this follows.

1. Build the agent image and push it to a public or local image repository.

   ```sh
   docker build -t dockerhubuser/agent:0.0.1 .
   ```

2. Configure the `redis-stack` application's required storage class settings.

   ```yaml
   # values.yaml
   # This is necessary only if you need to override the default `hostpath` storageClass.
   redis-stack-server:
     redis_stack_server:
       storage_class: csi-lvm-linear
   ```

3. Configure the image repository and tag settings.

   ```yaml
   # values.yaml
   image:
     repository: dockerhubuser/agent
     tag: 0.0.1
   ```

4. Obtain an OpenAPI API key and configure its value for the deployment.

   ```yaml
   # secrets/values.yaml
   envVars:
     OPENAI_API_KEY: base64-encoded-api-key
   ```

5. Create a namespace for the agent.

   ```sh
   kubectl create ns agent
   ```

6. Deploy the agent with Helm using the values shown above.

   ```sh
   helm upgrade --install -n agent agent deployment/helm/k8s-agent -f secrets/values.yaml -f values.yaml
   ```
