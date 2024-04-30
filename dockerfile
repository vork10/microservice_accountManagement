# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Make port 5000 available to the world outside this container
EXPOSE 5000


# Define environment variable
ENV NAME World

# Run gunicorn when the container launches, adjust the command to your application's entry point
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:5000", "app:app"]