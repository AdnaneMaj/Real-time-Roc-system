# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Set the Python path to include /app/src
ENV PYTHONPATH=/app/src

# Copy requirements.txt from the src folder to the container
COPY src/requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code from the src folder to the container
COPY src /app/src

# Expose the port your app will run on
EXPOSE 5000
EXPOSE 9092
EXPOSE 8501

# Copy the shell script into the container
COPY src/start.sh /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Run the script
CMD ["/app/start.sh"]