# Use the official lightweight Alpine Linux Redis image
FROM redis:7.2-alpine

# Set the working directory inside the container
WORKDIR /data

# Copy a custom redis.conf file from your host machine into the container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose the default Redis port
EXPOSE 6381
# Start Redis using the custom configuration file
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
