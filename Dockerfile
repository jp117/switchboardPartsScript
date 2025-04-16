# Use the official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install required packages
RUN pip install reportlab

# Keep container running and provide interactive shell
CMD ["/bin/bash"] 