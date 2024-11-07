# Specify the base image
FROM python:3-slim-buster

# Create a folder to store the app
RUN mkdir /code

# Define the working directory
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /code/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]