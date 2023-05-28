FROM ubuntu:22.04
# Init
RUN apt update -y && \
# Add user
    useradd -u 1000 -ms /bin/bash challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd;

# Copy chall data
RUN mkdir -p /chall/websrc
WORKDIR /chall

COPY src/server /chall/server

COPY src/flag.txt .
COPY src/websrc/ ./websrc/
COPY src/entrypoint.sh .

# Set libc
COPY src/libc.so.6 /lib/x86_64-linux-gnu/

# fix permissions
RUN chown -R root:challenge /chall/ && \
    chown -R root:challenge /home/ && \
    chmod -R g=rx,o= /chall/ && \
    chmod -R g=rx,o= /home/ && \
    mv /chall/flag.txt "/chall/flag-$(head -c 32 /dev/urandom | sha256sum | sed s/\ \ -/\/g ).txt"

# Switch user
USER 1000:1000

# Start
CMD ["/bin/sh","/chall/entrypoint.sh"]