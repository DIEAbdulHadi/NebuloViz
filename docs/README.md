# **⚠️Project Disclaimer**

NebuloViz is a production-level application, built entirely by me as a **solo developer** within the span of just **one week**. The goal was to test my skills and create a powerful, scalable, and maintainable system using the best tools and technologies available.

This project reflects not just my technical expertise but also my passion for coding and solving real-world challenges. By leveraging frameworks like **FastAPI, React, Kafka, and Redis,** and integrating advanced AI capabilities such as **predictive analytics** and **anomaly detection**, I aimed to deliver a functional, efficient, and cutting-edge solution that businesses can utilize effectively.

While it’s fully operational, NebuloViz was also a personal challenge—to design, build, and complete a project of this scale independently in record time, demonstrating what focused determination can achieve.

### Why This Project Matters
This project isn’t just a testament to skill but also an example of how modern libraries, strong architecture, and a drive for quality can create scalable systems in a short period. Every line of code was crafted with care, focusing on maintainability, simplicity, and power.

While my ambitions extend far beyond this, NebuloViz serves as a representation of what I can achieve—delivering quality software quickly and efficiently, ready for production.

# NebuloViz

**NebuloViz** is an advanced sales dashboard designed to provide businesses with actionable insights into their sales data. It integrates real-time analytics, AI-powered predictions, and anomaly detection to help businesses make data-driven decisions effectively. Built with cutting-edge technologies, NebuloViz is scalable, efficient, and user-friendly.

---

## Table of Contents

- [NebuloViz](#nebuloviz)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Application](#running-the-application)
  - [Technical Details](#technical-details)
    - [Tech Stack](#tech-stack)
    - [Project Structure](#project-structure)
  - [Key Features Breakdown](#key-features-breakdown)
  - [Setup and Deployment](#setup-and-deployment)
  - [How to Contribute](#how-to-contribute)
  - [License](#license)

---

## Features

- **Asynchronous Backend**: Built with FastAPI and async SQLAlchemy for high performance.
- **Real-Time Anomaly Detection**: Stream data via Kafka to identify unusual patterns in sales.
- **AI-Powered Insights**: Predictive analytics and customer segmentation using explainable AI models (SHAP).
- **Advanced Frontend**: Responsive React-based UI with lazy loading, error boundaries, and caching (React Query).
- **Granular Permissions**: Role-based and permission-based access controls for secure functionality.
- **Caching and Optimization**: Redis caching for rapid data access and API rate limiting.
- **Observability**: Metrics collection via Prometheus and Grafana for real-time monitoring.
- **Multi-Language Support**: Internationalization for global accessibility.

---

## Getting Started

### Prerequisites

- **Docker** and **Docker Compose**
- **Node.js** and **npm** (for frontend development)
- **Python 3.10+**
- **PostgreSQL** for database storage
- **Redis** for caching

---

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nebuloviz/nebuloviz.git
   cd nebuloviz
   ```

2. Copy the environment configuration:

   ```bash
   cp .env
   ```

3. Install backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install frontend dependencies:

   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. Apply database migrations:

   ```bash
   alembic upgrade head
   ```

---

### Running the Application

**Using Docker Compose**:

```bash
docker-compose up --build
```

- Access the backend at: [http://localhost:8000](http://localhost:8000)
- Access the frontend at: [http://localhost:3000](http://localhost:3000)

**Without Docker**:

1. Run the backend:

   ```bash
   uvicorn main:app --reload
   ```

2. Run the frontend:

   ```bash
   cd frontend
   npm start
   ```

---

## Technical Details

### Tech Stack

- **Backend**: Python (FastAPI), Async SQLAlchemy, Alembic
- **Frontend**: React with React Query, Material-UI
- **Database**: PostgreSQL
- **Caching**: Redis
- **Real-Time Streaming**: Kafka and Zookeeper
- **AI Models**: Scikit-learn, SHAP, and Dask
- **Monitoring**: Prometheus and Grafana

---

### Project Structure

```
NebuloViz/
├── config/                # Environment configurations
├── services/              # Core backend services (e.g., Auth, Data, AI Insights)
├── models/                # Database models
├── utils/                 # Utility functions (e.g., logging, permissions)
├── tests/                 # Unit and integration tests
├── frontend/              # React-based frontend
│   ├── public/            # Static assets
│   └── src/               # Frontend source code
├── docs/                  # Documentation (API, architecture, user guide)
├── alembic/               # Database migration scripts
├── docker/                # Docker and docker-compose files
├── .github/               # CI/CD workflows
├── main.py                # Application entry point
└── requirements.txt       # Backend dependencies
```

---

## Key Features Breakdown

1. **Real-Time Data Processing**:
   - Kafka streams sales data into the backend for immediate processing.
   - Adaptive anomaly detection tracks unusual trends and flags them.

2. **AI Insights**:
   - Predictive analytics help businesses forecast future sales.
   - Customer segmentation groups users by purchasing behaviors, enhancing targeted marketing.

3. **Advanced UI**:
   - React app with modern patterns like lazy loading, React Query for state management, and reusable Material-UI components.

4. **Caching**:
   - Redis caching improves performance for frequently accessed data.
   - Hierarchical cache invalidation ensures data consistency.

5. **Observability**:
   - Prometheus collects metrics from services, visualized via Grafana dashboards.
   - Alerts for performance or error thresholds ensure proactive issue resolution.

---

## Setup and Deployment

- **Docker**: The project is containerized using Docker. To set up the application, use the provided `docker-compose.yml` file.
- **CI/CD Pipeline**: GitHub Actions automates testing, builds, and deployment.

---

## How to Contribute

We welcome contributions! Here’s how you can get involved:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and open a pull request.
4. Follow our [contribution guidelines](docs/CONTRIBUTING.md) for detailed instructions.

---

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for details.

---
