FROM python:3.11-slim

# Set up a new user named "user" with user ID 1000 (standard for HF Spaces)
RUN useradd -m -u 1000 user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Install system dependencies for llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user:user . $HOME/app

# Switch to the "user" user
USER user

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Expose the standard HF Spaces port
EXPOSE 7860

# Run the ingestion script and then the main server
CMD python ingest_kb.py && python main.py
