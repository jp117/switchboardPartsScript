# Use the official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install required packages
RUN pip install reportlab

# Copy the application files
COPY . /app

# Run the application
CMD ["python", "app.py"] 