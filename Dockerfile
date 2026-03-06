FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy project files needed for installation
COPY pyproject.toml README.md ./
COPY pulsebot/ ./pulsebot/

# Set fallback version for hatch-vcs in case .git is not copied
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${SETUPTOOLS_SCM_PRETEND_VERSION}

# Install Python dependencies (non-editable for Docker)
RUN pip install --no-cache-dir --extra-index-url https://d.timeplus.com/simple/ .

# Copy config template
COPY config.yaml ./

# Create non-root user
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Default command
CMD ["pulsebot", "run"]
