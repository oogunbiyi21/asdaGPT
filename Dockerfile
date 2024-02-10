# Use an official Python 3.12.1 image as a parent image
FROM python:3.12.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update package lists and install wget
RUN apt-get update && apt-get install -y wget

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 81

# Set environment variable REMOTE_SERVER to 1
ENV REMOTE_SERVER=1

# Run app.py when the container launches
CMD ["python", "main.py"]
