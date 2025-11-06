# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port your Flask app listens on (default is 5000)
EXPOSE 5000

# Define the command to run your Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
