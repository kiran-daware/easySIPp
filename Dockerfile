# official Python base image with debian 12 bookworm
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    SIPP_VERSION=3.7.3 \
    SIPP_BIN_URL=https://github.com/SIPp/sipp/releases/download/v3.7.3/sipp

# Install system dependencies & clean-up (libcap2-bin for granting permissions using setcap)
RUN apt-get update && \
    apt-get install -y libcap2-bin nginx curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR $APP_HOME

# Copy just requirements.txt first to leverage build cache
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# Ensure you have a .dockerignore file to exclude unnecessary files!
COPY . .

# Download and install SIPp binary
RUN curl -L -o easySIPp/sipp ${SIPP_BIN_URL} && \
    chmod +x easySIPp/sipp

# Create /app/easySIPp/xml/tmp dir for tmp xml modification internally
RUN mkdir -p easySIPp/xml/tmp easySIPp/xml/backup && \
    cp easySIPp/xml/*.xml easySIPp/xml/backup

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN addgroup --gid 1234 kuser && \
    adduser --system --uid 5678 --gid 1234 --disabled-password --gecos "" kuser

# Set ownership and permissions
RUN chown -R kuser:kuser $APP_HOME && \
    chown -R kuser:kuser /var/lib/nginx /var/log/nginx /run

# separate RUN for setcap as it sometimes did not work when combined with above RUN.    
RUN setcap cap_net_raw+eip $APP_HOME/easySIPp/sipp

# Nginx configuration
COPY easysipp-nginx.conf /etc/nginx/sites-available/
RUN rm /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/easysipp-nginx.conf /etc/nginx/sites-enabled/

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose ports
EXPOSE 8080
EXPOSE 5060/udp 5060
EXPOSE 5061/udp 5061

# Switch to the non-root user before running the container
USER kuser

# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint.sh"]
