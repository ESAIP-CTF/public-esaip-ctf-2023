FROM alpine:3.11.0

# Init
RUN apk update && \
    apk add --no-cache python2 py2-pip musl-dev gcc && \
# Create user
    adduser -D -u 1000 challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd

# Copy chall data
WORKDIR /usr/app
ADD ./src .
RUN python2 -m pip install -r requirements.txt

# Switch user
USER 1000:1000

# Start
CMD ["/usr/bin/python2", "/usr/app/run.py"]