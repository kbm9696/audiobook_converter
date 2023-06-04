# audiobook_converter

To deploy the API server using Docker, follow these steps:

1. Download the `build.sh` script.

2. Make the script executable by running the following command:
    **chmod +x build.sh**
    
3. Run the script to build and deploy the API server:
    **./build.sh**

4. This will build the API server and create two containers: one for the database and another for the API server.

5. The API server will be accessible at:
    **https://<<*host-ip*>>:9075/api/user**
  
Replace `<host-ip>` with the IP address or hostname of the machine where Docker is running.

Please make sure to provide any additional instructions or configuration steps specific to your project or environment.

