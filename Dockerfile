FROM python:3.9-bullseye as base

COPY ./dist /app/dist

ENV PIP_EXTRA_INDEX_URL=https://www.piwheels.org/simple
ENV PIP_FIND_LINKS=/wheeley

RUN set -ex \
    && mkdir /wheeley \
    && pip3 install --upgrade pip wheel setuptools \
    && pip3 wheel --wheel-dir=/wheeley -r /app/dist/requirements.txt \
    && pip3 wheel --wheel-dir=/wheeley /app/dist/*.tar.gz

FROM python:3.9-slim-bullseye
EXPOSE 5000
WORKDIR /app

COPY --from=base /wheeley /wheeley

RUN set -ex \
    && pip3 install --no-index --find-links=/wheeley YOUR-PACKAGE \
    && rm -rf /wheeley \
    && pip3 freeze

ENTRYPOINT ["python3", "-m", "your_package"]
