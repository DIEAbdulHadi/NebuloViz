# NebuloViz API Documentation

This document provides detailed information about the API endpoints exposed by the **NebuloViz** backend.

## Table of Contents

- [NebuloViz API Documentation](#nebuloviz-api-documentation)
  - [Table of Contents](#table-of-contents)
  - [Authentication](#authentication)
    - [Login](#login)
- [Sales Orders](#sales-orders)
- [Get Order](#get-order)
- [Get All Orders](#get-all-orders)
- [Delete Order](#delete-order)
- [AI Insights](#ai-insights)
- [Segment Customers](#segment-customers)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Permissions](#permissions)
  - [Examples](#examples)
  - [Predicting Sales](#predicting-sales)

---

## Authentication

### Login

- **Endpoint**: `/api/v1/auth/login/`
- **Method**: `POST`
- **Description**: Authenticates a user and returns a JWT token.
- **Request Body**:

  ```json
  {
    "username": "user1",
    "password": "securepassword"
  }


Response:

{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}


# Sales Orders
Create Order
Endpoint: /api/v1/orders/

Method: POST

Description: Creates a new sales order.

Permissions Required: create_order

Headers:

Authorization: Bearer <token>

Request Body:

{
  "customer_name": "John Doe",
  "items": [
    {
      "product_name": "Widget A",
      "quantity": 10,
      "price": 99.99
    },
    {
      "product_name": "Widget B",
      "quantity": 5,
      "price": 49.99
    }
  ]
}

Response:

{
  "order_id": 123
}

# Get Order
Endpoint: /api/v1/orders/{order_id}/

Method: GET

Description: Retrieves a sales order by ID.

Permissions Required: view_order

Headers:
Authorization: Bearer <token>

Response:
{
  "order_id": 123,
  "customer_name": "John Doe",
  "items": [
    {
      "product_name": "Widget A",
      "quantity": 10,
      "price": 99.99
    },
    {
      "product_name": "Widget B",
      "quantity": 5,
      "price": 49.99
    }
  ],
  "created_at": "2021-11-01T12:34:56"
}

# Get All Orders
Endpoint: /api/v1/orders/

Method: GET

Description: Retrieves all sales orders with pagination.

Permissions Required: view_order

Headers:
Authorization: Bearer <token>

Query Parameters:

limit: Number of records to return (default: 10)
offset: Number of records to skip (default: 0)
Response:

[
  {
    "order_id": 123,
    "customer_name": "John Doe",
    "created_at": "2021-11-01T12:34:56"
  },
  {
    "order_id": 124,
    "customer_name": "Jane Smith",
    "created_at": "2021-11-02T09:21:45"
  }
  // ...
]

# Delete Order
Endpoint: /api/v1/orders/{order_id}/

Method: DELETE

Description: Deletes a sales order by ID.

Permissions Required: delete_order

Headers:
Authorization: Bearer <token>

Response:
{
  "message": "Order deleted successfully."
}

# AI Insights
Predict Sales
Endpoint: /api/v1/ai/predict-sales/

Method: GET

Description: Predicts future sales based on provided dates.

Permissions Required: view_predictions

Headers:
Authorization: Bearer <token>

Query Parameters:

future_dates: List of future dates (e.g., future_dates=2023-12-01&future_dates=2023-12-02)
Response:
{
  "predictions": [1000.0, 1050.0]
}

# Segment Customers
Endpoint: /api/v1/ai/segment-customers/

Method: GET

Description: Segments customers using clustering algorithms.

Permissions Required: view_segments

Headers:

Authorization: Bearer <token>

Response:
[
  {
    "customer_name": "John Doe",
    "total": 5000.0,
    "order_count": 10,
    "segment": 1
  },
  {
    "customer_name": "Jane Smith",
    "total": 15000.0,
    "order_count": 25,
    "segment": 2
  }
  // ...
]

# Error Handling
400 Bad Request: Invalid input data.
401 Unauthorized: Missing or invalid authentication token.
403 Forbidden: Insufficient permissions.
404 Not Found: Resource not found.
429 Too Many Requests: Rate limit exceeded.
500 Internal Server Error: An unexpected error occurred.
Error Response Format:
{
  "detail": "Error message describing what went wrong."
}

# Rate Limiting
Create Order: 10 requests per minute.
Predict Sales: 5 requests per minute.
Segment Customers: 5 requests per minute.

# Permissions
create_order: Allows creating new sales orders.
view_order: Allows viewing sales orders.
delete_order: Allows deleting sales orders.
view_predictions: Allows accessing sales predictions.
view_segments: Allows accessing customer segments.

## Examples
Creating an Order

curl -X POST "http://localhost:8000/api/v1/orders/" \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
        "customer_name": "John Doe",
        "items": [
          {"product_name": "Widget A", "quantity": 10, "price": 99.99}
        ]
      }'

## Predicting Sales
curl -X GET "http://localhost:8000/api/v1/ai/predict-sales/?future_dates=2023-12-01&future_dates=2023-12-02" \
  -H "Authorization: Bearer your_jwt_token"


