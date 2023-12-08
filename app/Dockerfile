# app/Dockerfile
FROM python:3.8-slim-buster

# set work directory
WORKDIR /app

# Install git so that can clone the code
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the code from the host to the container
COPY . .

# Install dependencies
RUN pip3 install -r requirements.txt

# Network port the container listens on at runtime
EXPOSE 8501

# Healthcheck to monitor the container
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Entrypoint to run the container
ENTRYPOINT ["streamlit", "run", "trig_plot_app.py", "--server.port=8501", "--server.address=0.0.0.0"]