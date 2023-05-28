FROM alpine:3.17.2

# Init
RUN apk update; \
    apk add --no-cache python3 py3-pip gcc libc-dev && \
# Create user
    adduser -D -u 1000 challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd

# Copy chall data
WORKDIR /usr/app
ADD ./src .

# Switch user
USER 1000:1000

# Start
CMD ["/usr/bin/python3", "/usr/app/chall.py"]