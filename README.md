# Application Documentation

## Table of Contents
1. [Application Overview](#application-overview)
2. [Prerequisites](#prerequisites)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
   - [Development Mode](#development-mode)
   - [Production Mode](#production-mode)
5. [Docker Operations](#docker-operations)
6. [Key Components](#key-components)
7. [Troubleshooting](#troubleshooting)

## Application Overview

This application consists of a frontend service and a backend service, both containerized using Docker. The backend is built with FastAPI and integrates with Permit.io for permission management. The frontend is a React application that interacts with the backend API.

## Prerequisites

- Docker and Docker Compose installed on your system
- Node.js and npm (for local development of the frontend)
- Python 3.7+ (for local development of the backend)
- A Permit.io account and API key
- RBAC policy set up in Permit Cloud (see [Permit.io Setup](#permitio-setup))

### Permit.io Setup

Before running the application, you need to set up your account and RBAC policy in Permit Cloud:

1. Sign up for a Permit.io account at [https://app.permit.io/signup](https://app.permit.io/signup)
2. Create a new project in Permit Cloud
3. Set up your RBAC policy, defining roles, resources, and permissions
4. Obtain your API key from the Permit.io dashboard

## Configuration

### Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```
PERMIT_API_KEY=your_permit_api_key_here
```

Replace `your_permit_api_key_here` with your actual Permit.io API key.

### Docker Compose Configuration

The project should have two Docker Compose files:

- `dev.yml` for development mode
- `docker-compose.yml` for production mode

Both files should include frontend and backend services with appropriate configurations.

## Running the Application

### Development Mode

To run the application in development mode:

1. Navigate to the project root directory in your terminal.
2. Run the following command:

   ```
   docker-compose -f dev.yml up --build
   ```

3. The frontend will be accessible at `http://localhost:3000`
4. The backend API will be available at `http://localhost:8000`

In development mode, the application will use hot-reloading for both frontend and backend, allowing for real-time updates as you modify the code.

### Production Mode

To run the application in production mode:

1. Navigate to the project root directory in your terminal.
2. Run the following command:

   ```
   docker-compose up --build
   ```

3. The application will be accessible at `http://localhost` (or the configured production domain)

In production mode, the application will use optimized builds and configurations suitable for a live environment.

## Accessing the Application

Before accessing the application:

1. Ensure you have set up your account and RBAC policy in Permit Cloud
2. Make sure the `PERMIT_API_KEY` in your `.env` file is correct
3. Verify that the Docker containers are running

Then, you can access the frontend at `http://localhost:3000` (in development) or `http://localhost` (in production).

## Docker Operations

### Executing Commands in a Docker Container

To execute commands in a running Docker container:

1. List running containers:
   ```
   docker ps
   ```

2. Execute a command (e.g., opening a shell):
   ```
   docker compose -f dev.yml exec -it <service_name> /bin/sh
   ```

   Replace `<service_name>` with either `frontend` or `backend`.

### Stopping Docker Containers

To stop the running Docker containers:

1. If you started the containers with `docker-compose up`, press `Ctrl+C` in the terminal where it's running.

2. Alternatively, run one of the following commands in the project directory:

   For development:
   ```
   docker-compose -f dev.yml down
   ```

   For production:
   ```
   docker-compose down
   ```

This will stop and remove the containers, networks, and volumes defined in the respective Docker Compose file.

## Key Components

### Backend (FastAPI)

The backend service is built with FastAPI and includes the following key endpoints:

- `GET /`: Checks if the user has permission to read a document.
- `GET /rbac-data/roles`: Fetches role-based access control data.
- `GET /rbac-data/resources`: Fetches resource data related to permissions.

### Frontend (React)

The frontend is a React application with the following main components:

- `App.js`: The main component that fetches and displays roles and resources data.
- `Navbar.js`: Navigation component.
- `ResourceTree.js`: Displays the resource hierarchy.
- `RoleCard.js`: Displays information about user roles.

## Troubleshooting

1. **Permission Issues**: Ensure that the `PERMIT_API_KEY` in the `.env` file is correct and that the user has the necessary permissions in your Permit.io configuration.

2. **Network Issues**: If services can't communicate, check that they are on the same Docker network (typically `app-network` in this configuration).

3. **Port Conflicts**: If ports 3000 or 8000 are already in use on your host machine, modify the port mappings in the appropriate Docker Compose file.

4. **Container Logs**: To view logs for a specific container:
   ```
   docker logs <container_id_or_name>
   ```

5. **Permit.io Integration**: If you're experiencing issues with permissions, verify that your RBAC policy is correctly set up in Permit Cloud and that the API key has the necessary permissions.
