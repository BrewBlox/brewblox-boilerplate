FROM brewblox/brewblox-service:latest

RUN mkdir -p /pkg
COPY ./pkg/* /pkg/

EXPOSE 5000

RUN pip3 install /pkg/* || true \
    && pip3 install YOUR-PACKAGE \
    && pip3 show YOUR-PACKAGE

ENTRYPOINT ["python3", "-m", "YOUR_PACKAGE"]
