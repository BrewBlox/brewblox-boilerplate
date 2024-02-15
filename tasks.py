from pathlib import Path

from invoke import Context, task

ROOT = Path(__file__).parent.resolve()
IMAGE = 'ghcr.io/you/your-package'


@task
def dist(ctx: Context):
    with ctx.cd(ROOT):
        ctx.run('rm -rf dist')
        ctx.run('poetry build --format sdist')
        ctx.run('poetry export --without-hashes -f requirements.txt -o dist/requirements.txt')


@task
def prepx(ctx: Context):
    """
    Creates a Docker builder for multiplatform images, if not yet present.

    If a valid builder is already present, it does nothing.
    """
    if 'linux/arm/v7' in ctx.run('docker buildx inspect').stdout:
        return

    ctx.run('docker run --rm --privileged multiarch/qemu-user-static --reset -p yes')
    ctx.run('docker buildx rm --force --all-inactive')
    ctx.run('docker buildx create --bootstrap --use --name bricklayer')


@task(pre=[dist])
def build(ctx: Context, tag='local'):
    """
    Builds a local Docker image.

    This image is only built for the current platform, and is not uploaded.
    """
    with ctx.cd(ROOT):
        ctx.run(' '.join([
            'docker buildx build',
            f'--tag {IMAGE}:{tag}',
            '--load',
            '.'
        ]))


@task(pre=[dist, prepx])
def release(ctx: Context, tag: str):
    """
    Builds and uploads a multiplatform Docker image.
    """
    with ctx.cd(ROOT):
        ctx.run(' '.join([
            'docker buildx build',
            '--platform linux/amd64,linux/arm/v7,linux/arm64/v8',
            f'--tag {IMAGE}:{tag}',
            '--push',
            '.',
        ]))
