FROM ubuntu:latest
LABEL authors="ВИОЛЕТТА"

ENTRYPOINT ["top", "-b"]

FROM python:3.9-slim

# Set build argument for verbosity
ARG VERBOSE=1

# Prohibits writing pyc file
ENV PYTHONDONTWRITEBYTECODE 1

# Ensures that stdout and stderr are sent directly to the terminal without pre-buffering
ENV PYTHONBUFFERED 1

# Set working directory
WORKDIR /app

# Install asyncpg
RUN pip install --no-cache-dir ${VERBOSE:+--verbose} asyncpg
RUN pip install poetry

# Copy the file with the dependencies alone
COPY requirements.txt .

# Install any needed packages specified
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY .. .

# Expose the port 80
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
