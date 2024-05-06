# Use the official Python image from Docker Hub
FROM python:3.9

# Install Ollama AI using the provided installation script
RUN curl https://ollama.ai/install.sh | sh

# Install required Python packages
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install Ollama Python client
RUN pip install --no-cache-dir ollama

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that Streamlit will run on
EXPOSE 5000

# Command to start Ollama AI service and run the Python script
CMD nohup ollama serve && ollama pull nomic-embed-text && python chat.py
