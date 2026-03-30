# ============================================================================
# matcha-target — vulnerable target container for attack simulation demos
# ============================================================================
# Exposes lightweight HTTP (nginx:80), SSH (openssh:22), and FTP (vsftpd:21)
# services so that the matcha attacker container can target them on a shared
# Docker network.
#
# Build:  docker build -t matcha-target docker/target/
# Run:    docker run --rm -p 80:80 -p 22:22 -p 21:21 matcha-target
# ============================================================================

FROM ubuntu:22.04

LABEL org.opencontainers.image.title="matcha-target" \
      org.opencontainers.image.description="Vulnerable target container for matcha attack simulation demos" \
      org.opencontainers.image.source="https://github.com/Montimage/mmt-attacker"

ENV DEBIAN_FRONTEND=noninteractive

# ---------------------------------------------------------------------------
# Install lightweight target services
# ---------------------------------------------------------------------------
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        nginx \
        openssh-server \
        vsftpd \
        net-tools \
        iputils-ping \
        curl && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# SSH — create demo user with a weak password (intentionally for lab use)
# ---------------------------------------------------------------------------
RUN useradd -m -s /bin/bash demo && \
    echo "demo:password123" | chpasswd && \
    mkdir -p /var/run/sshd && \
    # Allow password authentication (intentionally weak for demo)
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    # Allow root login with password (intentionally for demo)
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    echo "root:root123" | chpasswd

# ---------------------------------------------------------------------------
# HTTP — nginx serving a simple target page
# ---------------------------------------------------------------------------
COPY nginx/index.html /var/www/html/index.html
RUN chown -R www-data:www-data /var/www/html

# ---------------------------------------------------------------------------
# FTP — vsftpd with anonymous read access enabled
# ---------------------------------------------------------------------------
RUN echo "anonymous_enable=YES" > /etc/vsftpd.conf && \
    echo "local_enable=YES" >> /etc/vsftpd.conf && \
    echo "write_enable=NO" >> /etc/vsftpd.conf && \
    echo "listen=YES" >> /etc/vsftpd.conf && \
    echo "listen_ipv6=NO" >> /etc/vsftpd.conf && \
    echo "dirmessage_enable=YES" >> /etc/vsftpd.conf && \
    echo "use_localtime=YES" >> /etc/vsftpd.conf && \
    echo "pasv_enable=YES" >> /etc/vsftpd.conf && \
    echo "pasv_min_port=30000" >> /etc/vsftpd.conf && \
    echo "pasv_max_port=31000" >> /etc/vsftpd.conf && \
    mkdir -p /var/ftp/pub && \
    echo "Welcome to the matcha demo FTP server" > /var/ftp/pub/README.txt && \
    chown -R ftp:ftp /var/ftp

# ---------------------------------------------------------------------------
# Entrypoint starts all services and keeps the container alive
# ---------------------------------------------------------------------------
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose service ports
EXPOSE 21 22 80 30000-31000

ENTRYPOINT ["/entrypoint.sh"]
