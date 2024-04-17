# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Optionally declare environment variables
ENV OPENAI_API_KEY=""
ENV OPENAI_URL=""
ENV OPSGENIE_API_KEY=""
ENV OPSGENIE-URL=""
ENV WEBHOOK_API_KEY=""
# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
