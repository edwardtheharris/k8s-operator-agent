---
abstract: >-
   This folder contains the Helm Chart used to deploy the Kubernetes Operator
   Agent.
authors:
   - name: Xander Harris
     email: xandertheharris@gmail.com
date: 2024-08-04
title: Helm Chart
---

Documentation to be provided.

## Chart

```{autoyaml} ./deployment/helm/k8s-agent/Chart.yaml
```

## Values

The value for `image.repository` must be set for the chart to deploy.

```{autoyaml} deployment/helm/k8s-agent/values.yaml
```
