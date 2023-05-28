FROM alpine:3.17.0

# Init
RUN apk update && \
    apk add --no-cache python3 py3-pip && \
# Create user
    adduser -D -u 1000 challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd;

# Copy chall data
WORKDIR /usr/app/src
ADD ./src .
RUN chmod -R 777 /usr/app/src/; \
    chown 1000:1000 /usr/app/src/

# Startup script
COPY /config /tmp

ENV TOKEN=MTA1NTQ0MjEyMzE5MDcxMDI3Mg.G5L-K2.OT-4kuX3b2z5QX2pvXkCmuz9a6xAdBTvMqFcWo
ENV FLAG=ECTF{Alw4s_S3cure_YoUr_D1sc0Rd_B0ts}

# Switch user
USER 1000:1000

# Start
CMD ["/bin/sh", "/tmp/start.sh"]