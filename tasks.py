from pathlib import Path

from invoke import Context, task

ROOT = Path(__file__).parent.resolve()
IMAGE = 'ghcr.io/you/your-package'


@task
def build(ctx: Context):
    with ctx.cd(ROOT):
        ctx.run('rm -rf dist')
        ctx.run('poetry build --format sdist')
        ctx.run('poetry export --without-hashes -f requirements.txt -o dist/requirements.txt')


@task(pre=[build])
def local_docker(ctx: Context, tag='local'):
    with ctx.cd(ROOT):
        ctx.run(f'docker build -t {IMAGE}:{tag} .')
