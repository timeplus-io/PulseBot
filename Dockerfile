FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files needed for installation
COPY pyproject.toml README.md ./
COPY pulsebot/ ./pulsebot/

# Install Python dependencies (non-editable for Docker)
RUN pip install --no-cache-dir --extra-index-url https://d.timeplus.com/simple/ .

# Copy config template
COPY config.yaml ./

# Create non-root user
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Default command
CMD ["pulsebot", "run"]
