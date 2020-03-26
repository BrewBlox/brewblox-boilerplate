# Boilerplate code for Brewblox service implementations

There is some boilerplate code involved when creating a Brewblox service. This repository can be forked to avoid having to do the boring configuration.

You're free to use whatever editor or IDE you like, but we preconfigured some useful settings for Visual Studio Code.

Everything listed under **Required Changes** must be done before the package works as intended.

## How to use

* Install required dependencies (see below)
* Fork this repository to your own Github account or project.
* Follow all steps outlined under the various **Required Changes**.
* Start coding your service =)
    * To test, run `poetry run pytest`


## Install

First, make sure Python 3.7 is installed.

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3.7-dev
```

Install [Pyenv](https://github.com/pyenv/pyenv):
```
sudo apt-get update -y && sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

curl https://pyenv.run | bash
```

Install [Poetry](https://python-poetry.org/)
```
pip3 install --user poetry
```

Set Python environment (the python version used for this project).

**Run in the root of your cloned project**
```
pyenv local 3.7.7
```


## Files

---
### [pyproject.toml](./pyproject.toml)
The [pyproject](https://python-poetry.org/docs/pyproject/) file contains all kinds of Python settings. For those more familiar with Python packaging: it replaces the following files:
- `setup.py`
- `MANIFEST.in`
- `requirements.txt`

**Required Changes:**
* Change the `name` field to your project name. This is generally the same as the repository name. This name is used when installing the package through Pip. </br> It is common for this name to equal the package name, but using "`-`" as separator instead of "`_`".
* Change the `authors` field to your name and email.

---
### [tox.ini](./tox.ini)
Developer tools such as [Pytest](https://docs.pytest.org/en/latest/), [Flake8](http://flake8.pycqa.org/en/latest/), and [Autopep8](https://github.com/hhatto/autopep8) use this file to find configuration options.

**Required Changes:**
* Change `--cov=YOUR_PACKAGE` to refer to your module name.
* The `--cov-fail-under=100` makes the build fail if code coverage is less than 100%. It is optional, but recommended. Remove the `#` comment character to enable it.


---
### [.env](./.env)
Project-specific environment variables can be stored here. `Pipenv` will automatically load it when executing a command in `pipenv run`.

By default, the names of the Docker and Github repositories are stored here. They are read during the CI build.

**Required Changes:**
* Change `DOCKER_REPO=you/your-package` to match the name of your docker image.


---
### [.editorconfig](./.editorconfig)
This file contains [EditorConfig](https://editorconfig.org/) configuration for this project. </br>
Among other things, it describes per file type whether it uses tabs or spaces.

For a basic service, you do not need to change anything in this file.
However, it is recommended to use an editor that recognizes and uses `.editorconfig` files.


---
### [README.md](./README.md)
Your module readme (this file). It will automatically be displayed in Github.

**Required Changes:**
* Add all important info about your package here. What does your package do? How do you use it? What is your favorite color?


---
### [YOUR_PACKAGE/](./YOUR_PACKAGE/)
[\_\_main\_\_.py](./YOUR_PACKAGE/__main__.py),
[events_example.py](./YOUR_PACKAGE/events_example.py),
[http_example.py](./YOUR_PACKAGE/http_example.py),
[poll_example.py](./YOUR_PACKAGE/poll_example.py)

Your module. The directory name is used when importing your code in Python.

You can find examples for common service actions here.

**Required Changes:**
* Rename to the desired module name. This name can't include "`-`" characters. </br>
It is common for single-module projects to use "`-`" as a separator for the project name, and "`_`" for the module. </br>
For example: `your-package` and `your_package`.
* Change the import statements in .py files from `YOUR_PACKAGE` to your package name.

---
### [test/conftest.py](./test/conftest.py)
Project-level pytest fixtures. Some useful fixtures for testing any brewblox_service implementation are defined here. See tests in https://github.com/BrewBlox/brewblox-service/tree/develop/test for examples on how to use.


**Required Changes:**
* Change the import from `YOUR_PACKAGE` to your package name.


---
### [test/test_http_example.py](./test/test_http_example.py)
An example on how to test aiohttp endpoints you added. Feel free to remove this once you no longer need it.


---
### [docker/before_build.sh](./docker/before_build.sh)
Docker builds can only access files in the same directory as the `Dockerfile`.

The `before_build.sh` copies the dependencies for the Docker build into the docker/ directory.



---
### [docker/Dockerfile](./docker/Dockerfile)
A docker file for running your package. To build the image for both desktop computers (AMD), and Raspberry Pi (ARM):


Prepare the builder (run once per shell):
``` sh
# Buildx is an experimental feature
export DOCKER_CLI_EXPERIMENTAL=enabled

# Enable the QEMU emulator, required for building ARM images on an AMD computer
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

# Remove previous builder
docker buildx rm bricklayer || true

# Create and use a new builder
docker buildx create --use --name bricklayer

# Bootstrap the newly created builder
docker buildx inspect --bootstrap
```

Build:
``` sh
REPO=you/your-package
TAG=local

# Will build your Python package, and copy the results to the docker/ directory
bash docker/before_build.sh

# Build the image for amd and arm
# Give the image a tag
# Push the image to the docker registry
docker buildx build \
    --push \
    --platform linux/amd64,linux/arm/v7 \
    --tag "$REPO":"$TAG" \
    docker
```

While you are in the same shell, you don't need to repeat the build preparation.

If you want to use the image locally, run the build command like this:

``` sh
docker buildx build \
    --load \
    --platform linux/amd64 \
    --tag $REPO:$TAG \
    docker
```


**Required Changes:**
* Rename instances of `YOUR-PACKAGE` and `YOUR_PACKAGE` in the docker file to desired project and package names.

---
### [azure-pipelines.yml](./azure-pipelines.yml)
[Azure](https://dev.azure.com) can automatically test and deploy all commits you push to GitHub. If you haven't enabled Azure Pipelines for your repository: don't worry, it won't do anything.

To deploy your software, you will also need to create a [Docker Hub](https://hub.docker.com/) account, and register your image as a new repository.


## Deployment

Other Brewblox services are published and used as Docker images.
Setting this up is free and easy, and this repository includes the required configuration.

### Docker Hub

First, we'll need a Docker Hub account and repository to store created images.
Go to https://hub.docker.com/ and create an account.

After this is done, log in, and click `create repository`.
Pick a name, and click `create`. You don't need to connect the repository.

You can now push images to `user`/`repository`.

**Don't forget to set the DOCKER_REPO field in the .env file**.

### Azure Pipelines

To automatically build and push those images, you'll need a Continuous Integration (CI) server.
Here we'll set up Azure Pipelines as CI service, but you can do the same thing using [Travis](https://travis-ci.org/), [CircleCI](https://circleci.com/), [GitHub Actions](https://github.com/features/actions), [GitLab](https://about.gitlab.com/solutions/github/) or any of the others.

Go to https://azure.microsoft.com/en-us/services/devops/ and click "Start free with GitHub". You can then connect your GitHub account to Azure.

After logging in, create a new project. The name does not matter.

In the side bar, go to Pipelines, click on Library, and create a new variable group.
Call this group `brewblox`.

Add two variables:
- `DOCKER_USER` is your Docker Hub user name.
- `DOCKER_PASSWORD` is your Docker Hub password. Make the value secret by clicking the lock icon.

Save to confirm the group. These variables are now used during CI builds.

Again in the side bar, go to Pipelines, and create a new Pipeline. Choose GitHub as source, and select your repository.

Azure will automatically detect the `azure-pipelines.yml` file. Click "Run" to initialize it. It will ask you for permission to link Azure to your GitHub repository.

When this is done, it will start its first build. You can view the build results on https://dev.azure.com/

That's it. Happy coding!
