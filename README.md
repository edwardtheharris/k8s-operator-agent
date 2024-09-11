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

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=edwardtheharris_k8s-operator-agent&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=edwardtheharris_k8s-operator-agent)
[![Coverage Status](https://coveralls.io/repos/github/edwardtheharris/k8s-operator-agent/badge.svg)](https://coveralls.io/github/edwardtheharris/k8s-operator-agent)

Kubernetes Operator Agent

## Development

This project uses [Skaffold](https://skaffold.dev/) and [Helm](https://helm.sh/)
for development. Please make sure you have them installed on your machine.

### Python

The main code is written in Python, which may be formatted with either
PyDantic or Black.

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
