FROM alpine:3.17.3

# Init
RUN apk update && \
    apk add --no-cache openrc php apache2-utils php-apache2 && \
# Create user
    adduser -D -u 1000 mario && \
    echo "mario:$(head -c 32 /dev/urandom | base64)" | chpasswd;

# Allow php errors
# RUN sed -i 's/^display_errors = Off$/display_errors = On/g' /etc/php81/php.ini;

# Copy home user data
COPY --chown=1000:1000 config/ /home/mario/

# Setup service
RUN mkdir -p /run/apache2 && \
    chown mario:mario /run/apache2 && \
    sed -i 's,User apache,User mario,g' /etc/apache2/httpd.conf && \
    sed -i 's,Group apache,Group mario,g' /etc/apache2/httpd.conf && \
    sed -i 's,var/www/localhost/htdocs,var/www/html,g' /etc/apache2/httpd.conf && \
    sed -i 's/^Listen 80$/Listen 8000/' /etc/apache2/httpd.conf

# Change ownership of log directory
RUN chown mario:mario /var/log/apache2

COPY src/ /var/www/html/
RUN chown -R mario:mario /var/www/html && \
    chmod -R 755 /var/www/html

# Switch user
USER 1000:1000

# Start
CMD ["httpd", "-D", "FOREGROUND"]