# Points Tracking API

This project implements a simple REST API for tracking point transactions with payers. The API allows for adding points, spending points based on the oldest first, and checking balances.

## Endpoints

1. **Add Points**
   - **Route**: `/add`
   - **Method**: POST
   - **Description**: Adds points for a payer. 
   - **Request Body**:
     ```json
     {
       "payer": "DANNON",
       "points": 500,
       "timestamp": "2022-11-01T14:00:00Z"
     }
     ```

2. **Spend Points**
   - **Route**: `/spend`
   - **Method**: POST
   - **Description**: Spends points in a FIFO manner across payers. 
   - **Request Body**:
     ```json
     {
       "points": 5000
     }
     ```
   - **Response**: A list of payers and points deducted.

3. **Get Balance**
   - **Route**: `/balance`
   - **Method**: GET
   - **Description**: Returns the current balance of points per payer.
