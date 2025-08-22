# Start with a standard Python image based on Debian to ensure compatibility
FROM python:3.9

# Install system dependencies required for the MS ODBC Driver
RUN apt-get update && apt-get install -y curl apt-transport-https gnupg

# Add the Microsoft package repository for the ODBC driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Update package lists again and install the driver
# The "ACCEPT_EULA=Y" is required to automate the installation
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

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