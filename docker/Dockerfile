# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt from the src folder to the container
COPY ../src/requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code from the src folder to the container
COPY ../src /app/src

# Expose the port your app will run on
EXPOSE 5000

# Command to run your app
CMD ["python", "src/dashboard/app.py"]
