FROM brewblox/brewblox-service:rpi-latest

EXPOSE 5000
WORKDIR /app

COPY ./dist /app/dist
RUN pip3 install /app/dist/*
RUN pip3 show YOUR-PACKAGE

ENTRYPOINT ["python3", "-m", "YOUR_PACKAGE"]
