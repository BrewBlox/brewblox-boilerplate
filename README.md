# Boilerplate code for Brewblox services

There is some boilerplate code involved when creating a Brewblox service.
This repository can be used as a template to get started.

You're free to use whatever editor or IDE you like, but we preconfigured some useful settings for [Visual Studio Code](https://code.visualstudio.com/).

Everything listed under **Required Changes** must be done before the package works as intended.

## How to use

- Install required dependencies (see below)
- Fork this repository to your own Github account or project.
- Follow all steps outlined under the various **Required Changes**.
- Start coding your service =)
  - To test, run `poetry run pytest`
  - To lint, run `poetry run flake8`

## Install

Install the Python dev environment: <https://brewblox.com/dev/python_env.html>

During development, you need to have your environment activated.
When it is activated, your terminal prompt is prefixed with `(.venv)`.

Visual Studio code with suggested settings does this automatically whenever you open a .py file.
If you prefer using a different editor, you can do it manually by running:

```bash
poetry shell
```

Install [Docker](https://www.docker.com/101-tutorial):

```bash
curl -sL get.docker.com | sh

sudo usermod -aG docker $USER

reboot
```

## Files

---

### [pyproject.toml](./pyproject.toml)

The [pyproject](https://python-poetry.org/docs/pyproject/) file contains all kinds of Python settings.
For those more familiar with Python packaging: it replaces the following files:

- `setup.py`
- `MANIFEST.in`
- `requirements.txt`

**Required Changes:**

- Change the `name` field to your package name. This is generally the same as the repository name, but with any dash (`-`) characters replaced with underscores (`_`).
- Change the `authors` field to your name and email.
- Change the `description` field to a short description of your service.

---

### [.editorconfig](./.editorconfig)

This file contains [EditorConfig](https://editorconfig.org/) configuration for this project. \
Among other things, it describes per file type whether it uses tabs or spaces.

For a basic service, you do not need to change anything in this file.
However, it is recommended to use an editor that recognizes and uses `.editorconfig` files.

---

### [README.md](./README.md)

Your repository readme (this file). It will automatically be displayed in Github.

**Required Changes:**

- Add all important info about your package here. What does your package do? How do you use it? What is your favorite color?

---

### [your_package/](./your_package/)

The source code directory. The directory name is used when importing your code in Python.

Here you can find both code scaffolding, and examples for common features.

**Required Changes:**

- Rename to the desired module name. This name can't include "`-`" characters.

---

### [models.py](./your_package/models.py)

[Pydantic](https://docs.pydantic.dev) data models.
This includes the service configuration, which is set through environment variables.

**Required Changes:**

- Change the default service name value from `your_package` to your service name.
- Change the default env prefix from `your_package_` to your preferred prefix. Typically this is either package name or service name.

---

### [test/](./test/)

The test code shows how to setup tests and call endpoints.
This includes multiple tricks for testing async code with pytest.
You can remove the files if you no longer need them.

**Required Changes:**

- Change `your_package` imports to your package name.

---

### [Dockerfile](./Dockerfile)

A docker file for your service. Building the Dockerfile installs your Python distributable, and creates a Docker image.

**Required Changes:**

- Change `your_package` to your package name.

---

### [entrypoint.sh](./entrypoint.sh)

This script is the entrypoint for the Docker container.
It starts [Uvicorn](https://www.uvicorn.org/), the ASGI web server that runs the service code.

**Required Changes:**

- Change `your_package` to your package name.

---

### [tasks.py](./tasks.py)

[Invoke](https://www.pyinvoke.org/) is a convenient way to add build scripts.

By default, four tasks are available:

- **dist** generates the Python distributable that can then be used to build a Docker image.
- **prepx** creates a Docker builder for multiplatform images.
- **build** creates a local Docker image for testing. This image is not uploaded.
- **release** creates and uploads a multiplatform image.

**Required Changes:**

- Change `IMAGE` from `ghcr.io/you/your-package` to your Docker image name.

---

### [build.yml](./.github/workflows/build.yml)

Github can automatically test, build, and deploy all commits you push.
When enabled, this configuration will run tests, and then build a Docker image.

By default, the image is pushed to the Github Container Registry (ghcr.io).
If you want to use an alternative registry like Docker Hub, you can do this by changing the login step,
and then omitting the `ghcr.io/` prefix to your image.

When first pushed, Github sets the visibility of the image to `Internal`.
To make it publicly available:

- Navigate to the Github page of your repository.
- Click on the image name under "Packages" on the right-hand side of the repository page.
- Click on "Package settings" on the right-hand side of the package page.
- Scroll down to the "Danger Zone", and click "Change package visibility".
- Set visibility to "Public", and type the name of the image to confirm.

**Required Changes:**

- Remove the `if: false` line in the `build` job to enable CI.
- Set the `DOCKER_IMAGE` variable to your Docker image name.

That's it. Happy coding!
