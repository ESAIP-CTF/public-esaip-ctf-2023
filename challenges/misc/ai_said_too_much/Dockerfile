FROM alpine:3.17.0

# Init
RUN apk update && \
    apk add --no-cache nodejs npm && \
# Create user
    adduser -D -u 1000 challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd;

# Copy chall data
WORKDIR /usr/app/
COPY src/ .
RUN npm install;
RUN chmod -R 755 /usr/app/;

# Switch user
USER 1000:1000

# Start
CMD ["/bin/sh", "-c", "while true; do node /usr/app/app.js; done"]