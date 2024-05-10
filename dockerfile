# Dockerfile
FROM python:3.9

# Install ping and curl utilities
RUN apt-get update && apt-get install -y iputils-ping curl

# Set work directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Expose the port that the app will run on
EXPOSE 5000

# Command to run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
