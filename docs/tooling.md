---
abstract: >
    This document requires the tooling required for the k8s operator agent.
authors:
    - Rudy Attias
    - Steve Moore
    - Xander Harris
title: K8s Operator Agent Tooling
---

## Python

This project uses Python.

## FastAPI

Allows simple, trivial access to custom APIs.

## LangServe

[LangServe](https://www.langchain.com/langserve) is part of the
[LangChain](https://www.langchain.com/) set of services.

LangChain provides context management for LLM interactions. For the
purposes of this project, the relevant portion of the LangChang
documentation is its
[Python](https://python.langchain.com/docs/get_started/introduction)
implementation

## GitHub Actions

Integration and delivery is done using GitHub Actions. The following actions
are used.

### CI

This workflow builds and pushes a container image.

```{autoyaml} .github/workflows/ci.yml
```

### Documentation

This workflow builds and deploys the documentation site to GitHub Pages for
pull requests and pushes to the main branch.

```{autoyaml} .github/workflows/docs.yml
```

### CodeQL

This workflow checks the quality of the code and provides a report.

```{autoyaml} .github/workflows/codeql.yml
```

### DependaBot

Dependabot automatically creates PRs when software is out of date.

```{autoyaml} .github/dependabot.yml
```

```{sectionauthor} Xander Harris <xandertheharris@gmail.com>
```
