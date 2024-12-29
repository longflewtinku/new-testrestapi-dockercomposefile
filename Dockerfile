# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY . .

# Set environment variables for database connection
ENV DB_HOST=inventory-db
ENV DB_NAME=inventorydb
ENV DB_USER=qtdevops
ENV DB_PASSWORD=qtdevops

# Expose port 800 for the application (note: this should match the port used in CMD)
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
