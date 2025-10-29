# Start with a Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire 'blog' folder AS a 'blog' sub-directory
COPY ./blog ./blog

# Command to run your app
# This now works because /app/blog/main.py exists!
CMD ["uvicorn", "blog.main:app", "--host", "0.0.0.0", "--port", "80"]