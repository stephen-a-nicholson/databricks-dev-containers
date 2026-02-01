# Advanced Setup

Production-ready Dev Container setup with custom Dockerfile and CI/CD.

## Features

- Custom Debian-based image
- Oh My Zsh with Spaceship theme
- UV for fast Python package management
- Proper user permission handling (UID/GID mapping)
- SSH key mounting for Git operations
- Databricks CLI pre-installed
- Full CI/CD pipeline with Azure Pipelines

## Files in This Directory

- `Dockerfile` - Custom container image with all tools
- `devcontainer.json` - Advanced Dev Container configuration
- `ci-pipeline.yml` - Azure Pipelines CI/CD workflow

## Setup Instructions

### 1. Check and Update UIDs

Your container user needs to match your local UID/GID for proper file permissions.

Check your local UID/GID:
```bash
id -u  # Your UID (probably 501 on Mac, 1000 on Linux)
id -g  # Your GID
```

If different from 501, update in `devcontainer.json`:
```json
"args": {
  "USER_UID": "YOUR_UID",
  "USER_GID": "YOUR_GID"
}
```

Also update in `runArgs`:
```json
"runArgs": [
  "--userns=keep-id:uid=YOUR_UID,gid=YOUR_GID"
]
```

### 2. Create `.databrickscfg`

In your home directory (`~/.databrickscfg`):
```ini
[DEFAULT]
host = https://your-workspace.cloud.databricks.com
token = dapi123...your-token-here
```

Get your token from: Databricks Workspace → Settings → User Settings → Access Tokens

### 3. Open in Container

1. Copy this `advanced/` directory to your project root as `.devcontainer/`
2. Open project in VS Code
3. Command Palette (Cmd/Ctrl+Shift+P): "Dev Containers: Reopen in Container"
4. Wait for build (first time ~5-7 minutes)
5. Container starts with your zsh environment ready

### 4. Verify Setup

In the container terminal:
```bash
# Check Databricks CLI
databricks --version

# Check UV
uv --version

# Check Python
python3 --version
```

## What You Get

### Development Environment
- Full VS Code with extensions pre-installed
- Databricks extension connected to your workspace
- Oh My Zsh with autosuggestions and syntax highlighting
- UV for ultra-fast Python package management

### File Access
- Your SSH keys are mounted (for Git push/pull)
- Your `.databrickscfg` is mounted (for Databricks auth)
- All files have correct permissions (no permission denied errors)

### CI/CD Pipeline
The `ci-pipeline.yml` runs on every push:
1. **Pre-commit checks** - Runs ruff linting and formatting
2. **Build** - Builds your Docker image
3. **Test** - Runs pytest suite with coverage
4. **Publish** - Test results and coverage reports

## Azure DevOps Pipeline Setup

1. Go to your Azure DevOps project
2. Pipelines → New Pipeline
3. Select "Existing Azure Pipelines YAML file"
4. Choose `advanced/ci-pipeline.yml`
5. Save and run

The pipeline will:
- Run on every commit to any branch
- Skip if only Databricks bundle files changed
- Build your custom image
- Run all tests in the container
- Publish results

## Customization

### Add Python Packages

Use UV for fast installs. In container terminal:
```bash
uv pip install pandas polars duckdb
```

Or add to a requirements file:
```bash
uv pip install -r requirements.txt
```

### Add VS Code Extensions

Edit `devcontainer.json`:
```json
"extensions": [
  "databricks.databricks",
  "your.extension.id"
]
```

Find extension IDs: VS Code → Extensions → Right-click extension → Copy Extension ID

### Customize Zsh

After container starts:
```bash
code ~/.zshrc
```

Add aliases, PATH modifications, etc.

### Change Python Version

Edit `Dockerfile`, change base image:
```dockerfile
FROM python:3.12-slim  # Instead of debian:latest
```

## Troubleshooting

### Container won't start
**Problem**: Dev Container fails to build or start

**Solutions**:
- Check Docker Desktop is running
- Verify UID/GID settings match your system (`id -u` and `id -g`)
- Try: Docker → Preferences → Resources → Reset to factory defaults
- Check Docker logs: View → Output → Docker

### SSH keys not working
**Problem**: Can't push to Git

**Solutions**:
- Ensure `~/.ssh` directory exists locally
- Check mount in `devcontainer.json` is correct
- Verify permissions: `ls -la ~/.ssh` should show `700` for directory
- Test in container: `ssh -T git@github.com`

### Databricks extension not connecting
**Problem**: "Databricks extension failed to connect"

**Solutions**:
- Verify `.databrickscfg` exists in your home directory
- Check token is still valid (they can expire)
- Test CLI: `databricks workspace ls /`
- Restart VS Code and reopen in container

### Permission denied errors
**Problem**: Can't write files or `permission denied` errors

**Solutions**:
- This is usually UID/GID mismatch
- Check `id -u` locally vs `USER_UID` in devcontainer.json
- Update both `args` and `runArgs` to match your local IDs
- Rebuild container: Cmd+Shift+P → "Dev Containers: Rebuild Container"

### Tests fail in CI but pass locally
**Problem**: CI pipeline shows test failures

**Solutions**:
- Check `PYTHONPATH` is set correctly in ci-pipeline.yml
- Verify test requirements are in `tests/requirements-test.txt`
- Ensure JAVA_HOME is set for PySpark tests
- Run tests locally first: `pytest -v`

## Performance Tips

### Faster Builds
```bash
# Use BuildKit for faster Docker builds
export DOCKER_BUILDKIT=1
```

### Faster Package Installs
UV is already configured, but you can cache builds:

Add to `devcontainer.json`:
```json
"mounts": [
  "type=volume,source=uv-cache,target=/home/developer/.cache/uv"
]
```

### Exclude Unnecessary Files
Create `.dockerignore`:
```
.git
.venv
__pycache__
*.pyc
node_modules
.pytest_cache
```

## Advanced: Multiple Dev Containers

Want different setups for different projects?

1. Keep this advanced setup in `advanced/`
2. Use simple setup in `.devcontainer/` for quick work
3. Switch between them:
   - Cmd+Shift+P → "Dev Containers: Open Container Configuration File"
   - Choose which devcontainer.json to use

## Next Steps

- Add your PySpark code to `source/`
- Add tests to `tests/`
- Connect to Databricks clusters and start developing
- Set up Asset Bundles for deployment
- Configure pre-commit hooks

## Resources

- [Databricks Dev Containers](https://docs.databricks.com/dev-tools/vscode-ext.html)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [UV Documentation](https://github.com/astral-sh/uv)
- [Oh My Zsh](https://ohmyz.sh/)
