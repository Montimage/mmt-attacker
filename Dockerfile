# ============================================================================
# matcha CLI — Docker image (CLI-only, no web frontend)
# ============================================================================
# Build:  docker build -t matcha .
# Run:    docker run --rm --cap-add NET_ADMIN --cap-add NET_RAW --network host matcha --help
# ============================================================================

# ---------------------------------------------------------------------------
# Stage 1: builder — install Python deps into a prefix
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build-time system deps (libpcap headers needed to build scapy)
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        libpcap-dev \
        gcc \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy only the files needed to install the package
COPY pyproject.toml ./
COPY matcha/ matcha/
COPY scripts/ scripts/
COPY utils/ utils/

# Install the package and its dependencies into /install
RUN pip install --upgrade pip --quiet && \
    pip install --quiet --prefix=/install .

# ---------------------------------------------------------------------------
# Stage 2: runtime — minimal image with only what is needed to run matcha
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

# Install runtime system deps (libpcap for scapy raw-socket support)
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        libpcap0.8 \
        tcpdump \
        curl && \
    rm -rf /var/lib/apt/lists/* && \
    # Create a non-root user; attacks that need raw sockets are run with
    # --cap-add NET_ADMIN --cap-add NET_RAW at container start time.
    useradd --create-home --shell /bin/bash matcha

# Copy installed Python packages from the builder stage
COPY --from=builder /install /usr/local

# Copy application source (needed because scripts/ and utils/ are not
# installed as packages — they are imported by path at runtime)
COPY --from=builder /build/scripts/ /app/scripts/
COPY --from=builder /build/utils/   /app/utils/

# Ensure the matcha user can read all app files
RUN chown -R matcha:matcha /app

# Set working directory and PATH so matcha is found
WORKDIR /app
ENV PYTHONPATH=/app
ENV PATH="/usr/local/bin:$PATH"

# Switch to non-root user by default
USER matcha

# Expose the matcha CLI as the container entrypoint
ENTRYPOINT ["matcha"]
CMD ["--help"]
