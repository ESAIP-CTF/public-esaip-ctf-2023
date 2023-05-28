FROM alpine:3.17.0

# Init
RUN apk update && \
    apk add --no-cache nodejs npm socat chromium && \
# Create user
    adduser -D -u 1000 challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd;

# Copy chall data
WORKDIR /usr/app/
COPY src/ .
RUN npm install;
RUN chmod -R 755 /usr/app/;

# Setup entrypoint
RUN echo '#!/usr/bin/env sh' > /entrypoint.sh; \
    echo 'while true; do socat TCP-LISTEN:55555,fork,reuseaddr EXEC:"node /usr/app/client_bot.js",stderr; done' >> /entrypoint.sh

# Setup DNS
RUN echo "app  app.give-me-a-switch.esaip-cyber.com  >> /etc/hosts"; \
    echo "chat chat.give-me-a-switch.esaip-cyber.com >> /etc/hosts";

# Switch user
USER 1000:1000

# Start
CMD ["/bin/sh", "/entrypoint.sh"]
