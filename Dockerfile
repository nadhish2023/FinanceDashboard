# Start from a lightweight, official Python 3.11 image
FROM python:3.11-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Install the Tkinter library, which is a system dependency, not a Python one.
# We update the package list, install, and then clean up to keep the image small.
RUN apt-get update && apt-get install -y python3-tk && rm -rf /var/lib/apt/lists/*

# Install Poetry system-wide inside the container
RUN pip install poetry

# Copy only the dependency definition files first. This is a key caching optimization.
# Docker will only re-run the next step if these files change.
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies using Poetry.
# THE FIX: --no-dev is replaced with --without dev
# --no-interaction is for CI environments.
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Copy the rest of your application source code into the container's /app directory
COPY . .

# No CMD is needed, as this image's primary purpose is to be a package for testing
# in CI/CD and for deployment in Kubernetes.
