# better-stories/Dockerfile
# Dockerfile used to create an image to deploy on Azure Container Registry
FROM python:3.12.2

# Set working directory
WORKDIR /app

# Upgrade pip and install Rust compiler
RUN apt-get update && apt-get install -y curl build-essential \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --upgrade pip

# Copy requirements.txt to working directory and install python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files to working directory
COPY . .

# Expose port 
EXPOSE 8501

# Run streamlit command and pass PORT so Azure can correctly render app
CMD streamlit run better-stories.py --server.enableCORS true

