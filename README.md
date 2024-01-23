# Backend Application

This is the backend application for our project. It is built using Flask, and it provides the API for communication with the frontend.

## Setup

### 1. Clone the Repository


git clone https://github.com/AH-bi/tp_cicd.git
cd tp_cicd.git
cd backend


### 2. Create a Virtual Environment
`python3 -m venv venv`


### 3. Activate the Virtual Environment
`source venv/bin/activate`

### 4. Install Dependencies
`pip install -r requirements.txt`


### 5. Configure the Database
`Update the config.py file with your database credentials.`

### 6. Create Database Tables (for Testing)
`python createdb.py`


## Testing

### Run Tests
Try one of the following commands (if one doesn't work):
1. `python -m unittest test_*.py`
2. `python3 -m unittest discover`

Run these commands from the root directory of the backend.


## Run the Server

To start the server, use the following command within the root directory of the backend:

`python main.py`

