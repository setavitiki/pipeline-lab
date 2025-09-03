FROM python:3.9-slim AS builder

WORKDIR /app
COPY ../src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Create logs directory with proper permissions
RUN mkdir -p logs && chmod 755 logs

# Copy installed packages from builder (system-wide installation)
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source code
COPY ../src/ .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

ENV PATH=/usr/local/bin:$PATH

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]