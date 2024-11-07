# Use Python 3.9 as base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and data
COPY Nnhopfield.py .
COPY melodias.csv .
COPY melodias_dos.csv .

# Use ENTRYPOINT to set the main command and allow parameters
ENTRYPOINT ["python", "Nnhopfield.py"]

# Set default values for CMD which can be overridden
CMD ["melodias.csv", "--noise_level_1", "0.4", "--noise_level_2", "0.3"]