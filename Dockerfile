# Start with a standard Python image based on Debian
FROM python:3.9

# Install system dependencies required for the MS ODBC Driver
RUN apt-get update && apt-get install -y curl gpg lsb-release

# Add the Microsoft package repository GPG key securely
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg

# Add the repository source for Debian 12
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/mssql-release.list

# Update package lists again and install the newer driver
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

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