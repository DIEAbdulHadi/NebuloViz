# Design Decisions

This document outlines the key design decisions made during the development of **NebuloViz** and the rationale behind them.

## Table of Contents

- [Design Decisions](#design-decisions)
  - [Table of Contents](#table-of-contents)
  - [Technology Stack](#technology-stack)
  - [Asynchronous Programming](#asynchronous-programming)
  - [Microservices vs Monolith](#microservices-vs-monolith)
  - [Authentication and Authorization](#authentication-and-authorization)
  - [Caching Strategy](#caching-strategy)
  - [Real-Time Data Processing](#real-time-data-processing)
  - [Frontend Enhancements](#frontend-enhancements)
  - [Observability](#observability)
  - [Internationalization](#internationalization)
  - [Security Considerations](#security-considerations)

## Technology Stack

- **Python & FastAPI**: Chosen for its high performance, support for asynchronous operations, and ease of development.
- **React**: Selected for building a responsive and dynamic user interface.
- **PostgreSQL**: Used as the primary relational database for its reliability and feature set.
- **Redis**: Employed for caching and rate limiting due to its speed and simplicity.
- **Kafka**: Implemented for real-time data streaming and processing.

## Asynchronous Programming

- **Reasoning**: To improve scalability and performance by allowing the application to handle more concurrent requests.
- **Implementation**: Used `asyncio` and `sqlalchemy.ext.asyncio` for non-blocking I/O operations.

## Microservices vs Monolith

- **Decision**: Opted for a modular monolith rather than microservices.
- **Rationale**:
  - **Complexity**: Microservices introduce operational complexity that may not be necessary at the current scale.
  - **Development Speed**: A monolith allows for faster development and easier debugging.

## Authentication and Authorization

- **JWT Tokens**: Used for stateless authentication, simplifying scaling and session management.
- **Permission-Based Access Control**: Provides granular control over user actions, enhancing security.

## Caching Strategy

- **Hierarchical Caching with Redis**:
  - **Reasoning**: Improves data retrieval performance and reduces database load.
  - **Implementation**: Uses hierarchical key patterns for finer-grained cache invalidation.

## Real-Time Data Processing

- **Kafka Integration**:
  - **Reasoning**: Enables the application to process streaming data efficiently and detect anomalies in real-time.
  - **Scalability**: Kafka's partitioning allows for horizontal scaling as data volume grows.

## Frontend Enhancements

- **React Query**:
  - **Reasoning**: Simplifies data fetching and state management, providing caching and synchronization.
- **Error Boundaries**:
  - **Reasoning**: Improves user experience by gracefully handling UI errors.
- **Lazy Loading**:
  - **Reasoning**: Enhances performance by splitting code and loading components only when needed.

## Observability

- **Prometheus and Grafana**:
  - **Reasoning**: Provides real-time monitoring and alerting, essential for maintaining application health.
- **Structured Logging**:
  - **Reasoning**: Facilitates easier log analysis and debugging.

## Internationalization

- **Implementation**: Used `react-i18next` for frontend translations.
- **Reasoning**: Supports a global user base by providing multi-language support.

## Security Considerations

- **Password Hashing with Bcrypt**: Ensures secure storage of user passwords.
- **Input Validation**: Prevents injection attacks and ensures data integrity.
- **Permission Sanitization**: Validates and sanitizes user permissions to prevent privilege escalation.

---

**Conclusion**: The design choices made aim to balance performance, scalability, security, and ease of development. By carefully selecting technologies and patterns, **NebuloViz** is positioned to provide a robust and scalable solution for advanced sales analytics.
