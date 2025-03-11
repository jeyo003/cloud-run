# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set environment variables for logs
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the necessary files
COPY requirements.txt .
COPY main.py .
COPY phishing.h5 .
COPY scaler.pkl .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
