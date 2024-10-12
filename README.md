
# ReBAC Policy Visualization Project

This project implements a Relationship-Based Access Control (ReBAC) policy visualization tool using D3.js for the frontend and FastAPI for the backend, along with PostgreSQL for data storage and Permit.io for access control.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Services](#services)
- [Environment Variables](#environment-variables)
- [Docker Commands](#docker-commands)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Make sure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/aishmn/permit-io-assignment.git
   cd rebac-visualization
   ```

2. **Create a `.env` File**

   Create a `.env` file in the root directory of the project with the following environment variables:

   ```env
   DB_USER=your_db_username
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   PERMIT_API_KEY=your_permit_api_key
   JWT_SECRET=your_jwt_secret
   PERMIT_PDP_URL=http://permit-pdp:7000
   ```

## Usage

To start the application, run the following command:

```bash
docker-compose up
```

This command will build the services and start them in the background. You can access the frontend at `http://localhost:3000` and the backend at `http://localhost:8000`.

## Services

### 1. Frontend

- **Description**: React application for visualizing ReBAC policies.
- **Dockerfile**: `./webapp/Dockerfile.dev`
- **Ports**: `3000:3000`
- **Environment Variables**: 
  - `CHOKIDAR_USEPOLLING=true` (required for hot reloading)

### 2. Backend

- **Description**: FastAPI application providing an API for managing ReBAC policies.
- **Dockerfile**: `./backend/Dockerfile.dev`
- **Ports**: `8000:8000`
- **Environment Variables**:
  - `PERMIT_API_KEY` - API key for Permit.io
  - `DATABASE_URL` - Database connection string
  - `JWT_SECRET` - Secret key for JWT token signing
  - `PERMIT_PDP_URL` - URL of the Permit PDP service

### 3. Database (PostgreSQL)

- **Description**: PostgreSQL database for storing application data.
- **Image**: `postgres`
- **Environment Variables**:
  - `POSTGRES_USER` - Database user
  - `POSTGRES_PASSWORD` - Database password
  - `POSTGRES_DB` - Database name
- **Volumes**: Persist data using Docker volumes.

### 4. Permit PDP

- **Description**: Permit.io Policy Decision Point for managing access control.
- **Image**: `permitio/pdp-v2:latest`
- **Ports**: `7766:7000`
- **Environment Variables**:
  - `PDP_API_KEY` - API key for Permit.io
  - `PDP_DEBUG` - Enable debugging for Permit PDP service
- **Healthcheck**: Checks the health of the service every 30 seconds.

## Environment Variables

Make sure to configure the following environment variables in your `.env` file:

- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Name of the database to create
- `PERMIT_API_KEY`: API key for Permit.io
- `JWT_SECRET`: Secret key for JWT
- `PERMIT_PDP_URL`: URL for the Permit PDP
- `PERMIT_PDP_DEBUG`: Debug mode for Permit PDP

## Docker Commands

- **Build and Start Services**: 
  ```bash
  docker-compose up --build
  ```

- **Stop Services**: 
  ```bash
  docker-compose down
  ```

- **View Logs**: 
  ```bash
  docker-compose logs
  ```

- **Run Database Migrations** (if applicable):
  ```bash
  docker-compose exec backend alembic upgrade head
  ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue if you have suggestions or improvements.

## License
