---
abstract: >-
   Kubernetes Operator Agent is a LLM agent that is deployed as an operator
   in Kubernetes.
authors:
   - name: Xander Harris
     email: xandertheharris@gmail.com
date: 2024-08-04
title: Kubernetes Operator Agent
---

## Repository Contents

````{sidebar}
```{contents}
```
````

```{toctree}
:caption: contents

deployment/helm/k8s-agent/index
k8s_agent/index
tests/index
```

```{toctree}
:caption: meta

.github/index
docs/index
README
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`

```{glossary}
argo-cd
   A declarative, GitOps continuous delivery tool for {term}`Kubernetes`.
   More information is available [here](https://github.com/argoproj/argo-cd).

ArtifactHub
   A centralized location for Helm charts and artifacts. More information
   is available [here](https://artifacthub.io/packages/helm/argo/argo-cd).

GitHub
   Most likely the site this repository is hosted on. More information is
   available [here](https://github.com).

Helm
   A tool commonly used to deploy applications to {term}`Kubernetes`. More
   information is available [here](https://helm.sh).

LangChain
   LangChain’s flexible abstractions and AI-first toolkit make it the #1
   choice for developers when building with GenAI. More information is available
   [here](https://www.langchain.com/langchain).

Kubernetes
   An ancient Greek word that means 'sailor' or 'navigator', it is the
   most common container orchestration system currently in use. More
   information is available [here](https://kubernetes.io).
```

## Usage for Bare Metal Deployment

The process for this follows.

1. Build the agent image and push it to a public or local image repository.

   ```{code-block} shell
   docker build -t dockerhubuser/agent:0.0.1 .
   ```

2. Configure the `redis-stack` application's required storage class settings.

   ```{code-block} yaml
   :caption: values.yaml

   # This is necessary only if you need to override the
   # default `hostpath` storageClass.
   redis-stack-server:
     redis_stack_server:
       storage_class: csi-lvm-linear
   ```

3. Configure the image repository and tag settings.

   ```{code-block} yaml
   :caption: values.yaml

   image:
     repository: dockerhubuser/agent
     tag: 0.0.1
   ```

4. Obtain an OpenAPI API key and configure its value for the deployment.

   ```{code-block} yaml
   :caption: secrets/values.yaml

   envVars:
     OPENAI_API_KEY: base64-encoded-api-key
   ```

   ```{admonition} .gitignore
   Double check that the git ignore file contains `secrets` or `secrets/` to
   make sure that you don't unintentionally push your API key to GitHub.
   ```

5. Create a namespace for the agent.

   ```{code-block} shell
   kubectl create ns agent
   ```

6. Deploy the agent with Helm using the values shown above.

   ```{code-block} shell
   helm upgrade --install -n agent agent deployment/helm/k8s-agent \
      -f secrets/values.yaml -f values.yaml
   ```

```{sectionauthor} Xander Harris <xandertheharris@gmail.com>
```
