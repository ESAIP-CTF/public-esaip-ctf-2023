FROM debian:11.6-slim

# Init
RUN apt update -y && \
    apt install -y python3 python3-pip wget chromium && \
    mkdir /usr/app/ && \
    wget https://nodejs.org/dist/v18.16.0/node-v18.16.0-linux-x64.tar.xz -O /usr/app/node.tar.xz;

# Copy chall data
WORKDIR /usr/app/
RUN tar -xvf node.tar.xz && \
    mv node-v18.16.0-linux-x64 node && \
    ln -s /usr/app/node/bin/npm /usr/bin/npm && \
    ln -s /usr/app/node/bin/node /usr/bin/node
ADD ./src .

# Setup app
WORKDIR /usr/app/app/
RUN chmod -R 755 /usr/app/app/ && \
    /usr/bin/python3 -m pip install -r requirements.txt

# Setup bot
WORKDIR /usr/app/bot
RUN npm i

# Start
CMD ["/usr/bin/python3", "/usr/app/app/app.py"]
