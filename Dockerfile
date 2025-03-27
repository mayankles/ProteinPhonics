# Use the pre-built MUSCLE image from Docker Hub
FROM --platform=linux/amd64 pegi3s/muscle

# Install additional dependencies (Python, pip, curl)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip --break-system-packages && \
    pip3 install --break-system-packages -r requirements.txt

# Copy the rest of your project files
COPY . .

# Expose the port for Streamlit
EXPOSE 8501

# Set Streamlit environment variables for headless operation
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLECORS=false

# Override the ENTRYPOINT from the base image so our CMD runs correctly
ENTRYPOINT []

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
