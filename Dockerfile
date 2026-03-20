FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (nodejs/npm needed to build the web UI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy Python project files
COPY pyproject.toml README.md ./
COPY pulsebot/ ./pulsebot/

# Build the web UI — vite outputs to ../pulsebot/web relative to pulsebot_ui/,
# which resolves to /app/pulsebot/web/ so pip install picks it up automatically.
COPY pulsebot_ui/ ./pulsebot_ui/
RUN cd pulsebot_ui && npm ci && npm run build

# Set fallback version for hatch-vcs in case .git is not copied
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${SETUPTOOLS_SCM_PRETEND_VERSION}

# Install Python package — pulsebot/web/ is now present so it is included
RUN pip install --no-cache-dir --extra-index-url https://d.timeplus.com/simple/ .

# Copy config template
COPY config.yaml ./

# Create non-root user
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Default command
CMD ["pulsebot", "run"]
