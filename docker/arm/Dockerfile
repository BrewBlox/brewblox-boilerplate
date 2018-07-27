FROM brewblox/brewblox-service:rpi-latest

WORKDIR /app

COPY ./dist /app/dist
COPY ./config /app/config

EXPOSE 5000

RUN pip3 install /app/dist/* \
    && pip3 show YOUR-PACKAGE

ENTRYPOINT ["python3", "-m", "YOUR_PACKAGE"]
