# 1. Start with a lightweight Python base image
FROM python:3.9-slim

# 2. Set the working directory inside the container to /app
WORKDIR /app

# 3. Copy the list of dependencies into the container
COPY requirements.txt .

# 4. Install the Python dependencies listed in the file
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Document that the app will run on port 5000
EXPOSE 5000

# 7. Specify the command to run when the container launches
CMD ["python", "app.py"]