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
ENV DB_HOST=inventory-db
ENV DB_NAME=inventorydb
ENV DB_USER=qtdevops
ENV DB_PASSWORD=qtdevops
# Expose port 80 for the application
EXPOSE 8000
# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]