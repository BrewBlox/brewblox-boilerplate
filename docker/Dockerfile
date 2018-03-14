FROM python:3.6

# Bit of a trick: copy Dockerfile, and the "pkg" directory if it exists
# This allows a conditional copy of ./pkg/*
RUN mkdir -p /pkg
COPY ./Dockerfile ./pkg*/* /pkg/

EXPOSE 5000

RUN pip3 install -U YOUR-PACKAGE -f /pkg/

ENTRYPOINT ["python3", "-m", "YOUR_PACKAGE"]
