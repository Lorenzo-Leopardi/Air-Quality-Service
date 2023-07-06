# Air-Quality-Service
Mock sensor and Data Analysis

# Docker Compose Guide

This guide explains how to run the Docker Compose YAML file to set up the project environment automatically. By following these instructions, you will have the project up and running in no time!

## Prerequisites

Before proceeding, please make sure you have the following prerequisites installed on your system:

- Docker: [Installation Guide](https://docs.docker.com/get-docker/)

## Getting Started

To run the project using Docker Compose, follow these steps:

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/Lorenzo-Leopardi/Air-Quality-Service.git
   ```

2. Navigate to the project directory:

    ```shell
    cd Air-Quality-Service
    ```

3. Run the following command to start the project:

    ```shell
    docker-compose up --build
    ```
    This command will build and start the necessary containers.

4. Wait for the containers to start. 
    Once everything is up and running, you can access the application by opening the following URL in your web browser:

    http://localhost:8000/airqualityAPI/docs/

    This will take you to the project documentation, where you can learn more about the API endpoints and their usage.

## Enjoy exploring the application and its features!
