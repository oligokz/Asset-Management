# Start with a specific Debian 11 (Bullseye) based Python image
FROM python:3.9-bullseye

# Install system dependencies required for the MS ODBC Driver
RUN apt-get update && apt-get install -y curl gpg apt-transport-https

# Add the Microsoft package repository GPG key securely
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg

# Add the repository source for Debian 11
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list

# Update package lists again and install the driver
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Set the working directory inside the container
WORKDIR /app

# Copy the file that lists the dependencies
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application when the container starts
CMD ["python", "app.py"]