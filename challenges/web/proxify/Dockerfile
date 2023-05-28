FROM nginx:1.23.3-alpine

RUN apk update && \
    apk add --no-cache nodejs npm;

# Copy chall data
WORKDIR /usr/app/
COPY src/app/ .
RUN npm install;
RUN chmod -R 755 /usr/app/;

# Copy startup script
COPY src/config/start.sh /start.sh
RUN chmod +x /start.sh

COPY src/config/nginx.conf /etc/nginx/nginx.conf

CMD ["sh", "/start.sh"]