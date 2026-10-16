# databricks-dev-containers

Local PySpark development in VS Code with Dev Containers, Databricks Connect and a CI/CD pipeline. Production code lives in `.py` files under version control, runs on a real Databricks cluster from your laptop, and gets tested before it's deployed.

## Why this exists

Most Databricks teams write production pipelines in notebooks because that's what the workspace puts in front of you. It works until the second engineer joins: the diffs are unreadable, there are no tests, the "exported notebook" commits pile up, and nobody can run anything without the browser. This repo is the setup I converged on across client projects to get a normal software engineering workflow (IDE, tests, linting, pull requests, pipeline) while still executing against Databricks compute.

Two variants are included. The simple one gets a new engineer from clone to running PySpark against a cluster in about five minutes. The advanced one is the version you'd standardise a team on.

## Simple setup

Prerequisites: Docker Desktop, VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers), and access to a Databricks workspace.

1. Clone the repo and open it in VS Code:
   ```bash
   git clone https://github.com/stephen-a-nicholson/databricks-dev-containers.git
   cd databricks-dev-containers
   code .
   ```
2. When VS Code offers, choose **Reopen in Container**. First build takes a couple of minutes.
3. Open the Databricks extension in the sidebar, choose **Configure Databricks**, sign in and pick your workspace and cluster.
4. Write PySpark in a `.py` file and run it. It executes on the cluster, with results in the VS Code terminal.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df = spark.read.table("samples.nyctaxi.trips")   # runs on your Databricks cluster
df.groupBy("pickup_zip").count().show()
```

The container uses Microsoft's Python 3.11 image, installs the Azure CLI, the Databricks VS Code extension and Pylance, and runs `pip install databricks-connect uv pytest ruff chispa` on first start. Databricks Connect needs a version that matches your cluster's runtime; if the versions disagree you'll get a clear error on first run, and pinning `databricks-connect==<runtime major.minor>.*` in `postCreateCommand` fixes it.

## What you get

- A real IDE: autocomplete for PySpark, type checking, breakpoints, refactoring, Git that behaves.
- Code in `.py` files, so pull requests show actual diffs and reviewers can review.
- Tests with pytest and [chispa](https://github.com/MrPowers/chispa) for DataFrame assertions, run locally before anything is pushed.
- Linting with ruff.
- Remote execution through Databricks Connect, with no upload step.

## Advanced setup

For teams. See [`advanced/README.md`](advanced/README.md). It adds a custom Debian-based image, UID/GID mapping so file permissions behave on Mac and Linux, SSH key mounting, uv for dependency management, the Databricks CLI pre-installed, and an Azure Pipelines workflow (`ci-pipeline.yml`) that lints, tests and deploys. GitHub Actions users can translate it line for line.

Pair it with [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html) for deployment: add a `databricks.yml` at the project root and the pipeline deploys from the same code it just tested.

## Project layout

```
.devcontainer/devcontainer.json   simple setup
advanced/                         custom image, advanced devcontainer.json, Azure Pipelines CI
examples/simple_pipeline.py       a small PySpark job
examples/test_simple_pipeline.py  its tests
source/                           your code
tests/                            your tests
```

## Common questions

**Can I still use notebooks?** Yes, for exploration. The point of this setup is that production code doesn't live in them.

**Does it work on Windows, Mac and Linux?** Yes. Dev Containers behave the same on all three; the UID/GID notes in the advanced README cover the one place Mac and Linux differ.

**The Databricks extension won't connect.** Create `~/.databrickscfg` in the container with your workspace host and a token, or sign in through the extension with OAuth. Service principals rather than personal tokens for anything shared.

**Module not found.** Add the package to `postCreateCommand` in `devcontainer.json` so the next person gets it too, rather than installing it by hand in the container.

## Contributing

Issues and pull requests welcome. If you've adapted the advanced setup for GitHub Actions or GitLab, a PR with the pipeline file would be useful to others.

## Licence

MIT.
