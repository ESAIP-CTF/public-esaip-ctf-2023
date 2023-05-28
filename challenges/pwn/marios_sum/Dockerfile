FROM alpine:3.17.3
# Init
RUN apk update && \
    apk add --no-cache socat && \
# Add user
    adduser -D -u 1000 challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd;

# Copy chall data
RUN mkdir -p /chall
WORKDIR /chall

COPY src/chall /chall/chall

COPY src/flag.txt .

RUN echo '#!/usr/bin/env sh' > /chall/entrypoint.sh ;\
    echo 'while true; do socat TCP-LISTEN:55555,fork,reuseaddr EXEC:"/chall/chall",stderr; done' >> /chall/entrypoint.sh

# fix permissions
RUN chown -R root:challenge /chall/ && \
    chown -R root:challenge /home/ && \
    chmod -R g=rx,o= /chall/ && \
    chmod -R g=rx,o= /home/

# Switch user
USER 1000:1000

# Start
CMD ["/bin/sh","/chall/entrypoint.sh"]