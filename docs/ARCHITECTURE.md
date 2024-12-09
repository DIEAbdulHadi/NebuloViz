
# **Location**: `docs/ARCHITECTURE.md`

```markdown
# NebuloViz Architecture Overview

This document provides an overview of the architecture of the **NebuloViz** application, detailing its components, technologies used, and how they interact to provide a seamless user experience.

## Table of Contents

- [High-Level Architecture](#high-level-architecture)
- [Backend Architecture](#backend-architecture)
  - [FastAPI Application](#fastapi-application)
  - [Asynchronous Operations](#asynchronous-operations)
  - [Services Layer](#services-layer)
  - [Database Layer](#database-layer)
- [Frontend Architecture](#frontend-architecture)
  - [React Application](#react-application)
  - [State Management](#state-management)
  - [Internationalization](#internationalization)
- [Data Streaming and Anomaly Detection](#data-streaming-and-anomaly-detection)
- [Caching Layer](#caching-layer)
- [Security and Permissions](#security-and-permissions)
- [Observability and Monitoring](#observability-and-monitoring)
- [Deployment Architecture](#deployment-architecture)
- [Scalability Considerations](#scalability-considerations)

## High-Level Architecture









## Backend Architecture

### FastAPI Application

- **Framework**: FastAPI is used for building the backend RESTful API due to its support for asynchronous operations and automatic documentation generation.
- **API Versioning**: The API is versioned (e.g., `/api/v1`) to maintain backward compatibility.

### Asynchronous Operations

- **Async/Await**: The backend services leverage Python's `asyncio` for non-blocking I/O operations, enhancing scalability.
- **Asynchronous Database Sessions**: Utilizes `sqlalchemy.ext.asyncio` for async database interactions.

### Services Layer

- **Modular Design**: Services are modularized (e.g., `AuthService`, `DataService`, `AIInsights`) to separate concerns.
- **Interfaces**: Abstract base classes define service interfaces for consistency.

### Database Layer

- **ORM**: SQLAlchemy is used for database interactions.
- **Migrations**: Alembic manages database schema migrations.
- **Models**: Defined in the `models` directory, representing database tables.

## Frontend Architecture

### React Application

- **Component-Based**: The UI is broken down into reusable components (e.g., charts, data tables).
- **Routing**: React Router is used for client-side routing.

### State Management

- **React Query**: Manages server state, providing caching, synchronization, and error handling for API calls.
- **Context API**: Used for authentication context (`AuthContext`), managing user sessions.

### Internationalization

- **i18n**: Implements internationalization using `react-i18next`.
- **Supported Languages**: Configurable in `settings.py`.

## Data Streaming and Anomaly Detection

- **Kafka**: Used for real-time data streaming, allowing the application to process incoming sales data.
- **Anomaly Detector**: An asynchronous service consumes data from Kafka, detects anomalies, and triggers alerts.

## Caching Layer

- **Redis**: Serves as an in-memory data store for caching and rate limiting.
- **Hierarchical Caching**: Implements granular cache invalidation using hierarchical key patterns.

## Security and Permissions

- **JWT Authentication**: Uses JSON Web Tokens for stateless authentication.
- **Permission-Based Access Control**: Decorators enforce access control based on user permissions.
- **Password Hashing**: Passwords are securely hashed using bcrypt.

## Observability and Monitoring

- **Prometheus**: Collects metrics from the application and Kafka.
- **Grafana**: Visualizes metrics and sets up alerting rules.
- **Logging**: Structured logging with JSON format for easier parsing and analysis.

## Deployment Architecture

- **Containerization**: Docker is used to containerize the application for consistent deployment.
- **Docker Compose**: Orchestrates multiple services (app, db, redis, kafka) for local development.
- **CI/CD Pipeline**: Configured using GitHub Actions for automated testing and deployment.

## Scalability Considerations

- **Horizontal Scaling**: The stateless nature of the application allows for horizontal scaling of backend instances.
- **Kafka Partitioning**: Proper partitioning ensures scalability for data streaming.
- **Async Tasks**: Asynchronous operations prevent blocking and improve throughput.

---

**Note**: This architecture is designed to be modular and scalable, allowing for future enhancements and the ability to handle increased load as the application grows.

