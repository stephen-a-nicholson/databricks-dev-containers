# Databricks Dev Containers Setup

Local PySpark development with VS Code Dev Containers + Databricks Connect + CI/CD.

Write PySpark locally in VS Code. Execute on remote Databricks clusters. Deploy automatically.

## Quick Start (5 Minutes)

### Prerequisites

- Docker Desktop installed and running
- VS Code with [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Databricks workspace access
- Git

### Option 1: Simple Setup (Recommended to Start)

Perfect for getting started quickly. Uses Microsoft's pre-built Python image.

1. Clone this repo:
```bash
git clone https://github.com/stephen-a-nicholson/databricks-dev-containers.git
cd databricks-dev-containers
```

2. Open in VS Code:
```bash
code .
```

3. When prompted, click **"Reopen in Container"**  
   (Or: Cmd/Ctrl+Shift+P → "Dev Containers: Reopen in Container")

4. Wait for container to build (~2 minutes first time)

5. Configure Databricks:
   - Open Databricks extension in sidebar
   - Click "Configure Databricks"
   - Sign in and select your workspace

6. Start coding! Create a new Python file and write PySpark.

That's it. You're now writing PySpark locally with full IDE support.

### Option 2: Production Setup

For teams wanting a robust, customised environment. See [`advanced/README.md`](advanced/README.md).

Includes:
- Custom Debian-based Docker image
- Oh My Zsh with plugins
- UV for ultra-fast package management
- Proper UID/GID handling
- SSH key mounting
- Full CI/CD pipeline

## What You Get

### 🎯 Real IDE Experience
- IntelliSense and autocomplete for PySpark
- Real-time syntax checking with Pylance
- Debugging with breakpoints
- Refactoring tools
- Git integration that actually works

### 📦 Actual Version Control
- Write PySpark in `.py` files (not notebooks)
- Git diffs that make sense
- Proper code review in pull requests
- No more "exported notebook" commits

### ✅ Automated Testing
- Run pytest locally before pushing
- Integrate with CI/CD (GitHub Actions, Azure Pipelines)
- Pre-commit hooks with ruff linting
- Test against real Databricks clusters

### 🚀 Remote Execution
- Execute code on Databricks clusters instantly
- No uploading or syncing needed
- See results in VS Code terminal
- Full Databricks Connect support

## Example Workflow

```python
# my_pipeline.py
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# This runs on your Databricks cluster!
df = spark.read.table("sales")
result = df.groupBy("region").sum("revenue")
result.show()
```

Run it:
```bash
python my_pipeline.py
```

Results appear instantly. No uploads. No waiting.

## Project Structure

```
databricks-dev-containers/
├── README.md                     # This file
├── .devcontainer/
│   └── devcontainer.json         # Simple setup config
├── advanced/
│   ├── README.md                 # Production setup guide
│   ├── Dockerfile                # Custom image
│   ├── devcontainer.json         # Advanced config
│   └── ci-pipeline.yml           # Azure Pipelines CI/CD
├── examples/
│   ├── simple_pipeline.py        # Example PySpark code
│   └── test_simple_pipeline.py   # Example tests
├── source/                       # Your PySpark code goes here
└── tests/                        # Your tests go here
```

## Next Steps

### For Beginners
1. Use the simple setup above
2. Create a Python file in `source/`
3. Write some PySpark code
4. Execute against your Databricks cluster
5. Enjoy the workflow!

### For Teams
1. Check out [`advanced/README.md`](advanced/README.md)
2. Customize the Dockerfile for your needs
3. Set up CI/CD pipeline
4. Configure Asset Bundles for deployment
5. Add pre-commit hooks

## Common Questions

### Do I need Databricks Connect?
It's included! The `postCreateCommand` in devcontainer.json installs it automatically.

### Can I use this with GitHub Actions?
Yes! The CI/CD example uses Azure Pipelines, but you can adapt it for GitHub Actions.

### What about Databricks Asset Bundles?
Absolutely. This setup works great with Asset Bundles for deployment. Add your `databricks.yml` to the project root.

### Can I use notebooks?
You can, but the whole point is to avoid notebook-driven development for production code. Use `.py` files and version control them properly.

### Does this work on Windows/Mac/Linux?
Yes, all three. Dev Containers work the same everywhere.

## Troubleshooting

### Container won't start
- Make sure Docker Desktop is running
- Check you have enough disk space (~2GB for images)
- Try: Docker → Preferences → Reset to factory defaults

### Databricks extension won't connect
- Create `~/.databrickscfg` with your workspace details:
```ini
[DEFAULT]
host = https://your-workspace.cloud.databricks.com
token = dapi123...
```
- Get token from: Databricks → Settings → User Settings → Access Tokens

### "Module not found" errors
The container installs common packages. To add more:
```bash
# Inside the container
pip install your-package-here
```

Or add to `postCreateCommand` in `devcontainer.json`.

## Resources

- [Databricks Dev Tools Docs](https://docs.databricks.com/dev-tools/index.html)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Databricks Connect](https://docs.databricks.com/dev-tools/databricks-connect.html)
- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)

## Contributing

Found a bug? Have a suggestion? Open an issue or PR!

## License

MIT License - use this however you want.

## Questions?

- Open an issue
- Reach out on [LinkedIn](https://www.linkedin.com/in/stephen-nicholson/)
- Check the [Databricks Community](https://community.databricks.com/)

---

**Like this setup?** ⭐ Star the repo and share it with your team!
