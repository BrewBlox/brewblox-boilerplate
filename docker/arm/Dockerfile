FROM brewblox/brewblox-service:rpi-newest-tag as base

COPY ./dist /app/dist
COPY ./requirements.txt /app/requirements.txt

RUN pip3 install wheel \
    && ls /wheeley-base \
    && pip3 wheel --wheel-dir=/wheeley --find-links=/wheeley-base -r /app/requirements.txt \
    && pip3 wheel --wheel-dir=/wheeley --find-links=/wheeley --no-index /app/dist/*

FROM brewblox/rpi-python:3.7-slim
EXPOSE 5000
WORKDIR /app

ARG service_info=UNKNOWN
ENV SERVICE_INFO=${service_info}

COPY --from=base /wheeley /wheeley
COPY ./config /app/config

RUN pip3 install --no-index --find-links=/wheeley YOUR-PACKAGE \
    && rm -rf /wheeley \
    && pip3 freeze

ENTRYPOINT ["python3", "-m", "YOUR_PACKAGE"]
