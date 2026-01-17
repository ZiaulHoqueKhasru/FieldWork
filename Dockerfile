# 1. Base image
FROM python:3.9

# 2. Set working directory
WORKDIR /app

# 3. Copy all files from current folder to /app in container
COPY . /app

# 4. Install dependencies
# --no-cache-dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose port 8000
EXPOSE 8000

# 6. Command to run the application
# We use uvicorn directly to ensure host is 0.0.0.0 (required for Docker access)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]