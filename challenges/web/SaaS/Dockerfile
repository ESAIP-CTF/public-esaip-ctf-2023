FROM alpine:3.17.0

# Init
RUN apk update && \
    apk add --no-cache python3 py3-pip nodejs npm chromium && \
# Create user
    adduser -D -u 1000 challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd

# Copy chall data
WORKDIR /usr/app
ADD ./src .
RUN chmod -R 755 /usr/app/;

# Setup bot
WORKDIR /usr/app/screenshot
RUN npm i

# Install python dependencies
WORKDIR /usr/app/app
RUN /usr/bin/python3 -m pip install -r requirements.txt

# Switch user
USER 1000:1000

# Start
CMD ["/usr/bin/python3", "/usr/app/app/app.py"]
