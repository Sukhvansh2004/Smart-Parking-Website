# Smart Parking Management System

A full-stack Smart Parking Management System with a FastAPI backend (with PostgreSQL database) and a React frontend. This app lets users book and release parking slots, while admins can manage slots via an admin panel.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Backend Setup](#backend-setup)
  - [1. Setting Up a Conda Environment](#1-setting-up-a-conda-environment)
  - [2. Installing Dependencies](#2-installing-dependencies)
  - [3. Configuring PostgreSQL](#3-configuring-postgresql)
  - [4. Running the Backend](#4-running-the-backend)
- [Frontend Setup](#frontend-setup)
  - [1. Installing Node and Dependencies](#1-installing-node-and-dependencies)
  - [2. Running the Frontend](#2-running-the-frontend)
- [Usage](#usage)
- [Admin Panel](#admin-panel)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Features

- **User Interface:** Book and release parking slots.
- **Admin Panel:** Manage parking slots by adding or deleting them.
- **REST API:** Built with FastAPI, with endpoints for user and admin functionalities.
- **Database:** PostgreSQL for data persistence.
- **React Frontend:** Modern, responsive UI with real-time updates.
- **Conda Environment:** Manage Python dependencies isolated from the global installation.

## Prerequisites

- **Conda:** [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)
- **Node.js:** LTS version (v16 or later recommended)
- **PostgreSQL:** Installed and running (see [PostgreSQL Setup](#3-configuring-postgresql) below)
- **WSL Ubuntu 20.04/22.04:** (if using WSL on Windows)

## Project Structure

smart-parking/ 
.
├── README.md
├── backend
│   ├── auth.py
│   ├── create_admin.py
│   ├── database.py
│   ├── main.py
│   ├── requirements.txt
│   └── secret.py
├── frontend
│   ├── package.json
│   ├── public
│   │   └── index.html
│   └── src
│       ├── App.css
│       ├── App.js
│       ├── components
│       │   ├── AdminLogin.js
│       │   ├── AdminPanel.js
│       │   ├── GoogleLoginComponent.js
│       │   ├── ParkingLot.js
│       │   └── Slot.js
│       └── index.js
└── set_env.sh


# Backend Setup

## 1. Setting Up a Conda Environment

Open your terminal and navigate to the `backend` directory. Create a new conda environment (e.g., named `smart_parking_env`):

```bash
conda create -n smart_parking_env python=3.9
conda activate smart_parking_env
```

## 2. Installing Dependencies
Inside the backend folder, install the required Python packages. Make sure you have a requirements.txt file that includes:

```txt
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-jose[cryptography]
bcrypt
passlib
```
Then install them with:

```bash
pip install -r requirements.txt
```

## 3. Configuring PostgreSQL
Installing PostgreSQL (WSL Ubuntu)
Update packages:
```bash
sudo apt update
```

Install PostgreSQL:

```bash
sudo apt install postgresql postgresql-contrib
```

Start PostgreSQL service:
```bash
sudo service postgresql start
```

Creating Database and User
Switch to the PostgreSQL shell as the postgres user:

```bash
sudo -u postgres psql
```

Then run:

```sql
CREATE DATABASE smart_parking;
CREATE USER your_username WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE smart_parking TO your_username;
\q
```

## 4. Running the Backend
Now export all the secrets and tokens into the terminal where you will be running the backend. It is advisable to make a bash script exporting all the necessary variables and then source it.

```sh
#!/bin/bash
# set_env.sh
# This script sets environment variables for the Smart Parking Management System.
# Run it using: source set_env.sh

export DATABASE_URL="postgresql://your_username:your_password@localhost/smart_parking"
export SECRET_KEY="YOUR_SECRET_KEY_FOR_ADMIN_ACCESS"
export GOOGLE_CLIENT_ID="GOOGLE_AUTH_CLIENT_TOKEN"
export GOOGLE_CLIENT_SECRET="GOOGLE_AUTH_CLIENT_TOKEN_SECRET"


echo "Environment variables have been set."
```
After configuring the variables and installing dependencies, run the FastAPI backend:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```


The API should now be accessible at http://localhost:8000.

# Frontend Setup

## 1. Installing Node and Dependencies
Navigate to the frontend directory. If you haven't created the React app yet, run:

```bash
npx create-react-app .
```

Then, install required packages:

```bash
npm install axios react-router-dom
```

Make sure your package.json is similar to:

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "axios": "^0.27.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.3.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

Also, ensure you have a valid index.html in frontend/public/ as described in the Project Structure.

## 2. Running the Frontend

Before running the frontend, create a .env file in the frontend folder containing the google auth token required for signing in.

```env
REACT_APP_GOOGLE_CLIENT_ID=YOUR_GOOGLE_AUTH_CLIENT_TOKEN
```

In the frontend folder, run:

```bash
npm start
```

Your React app will be available at http://localhost:3000.

Usage
User Interface:

Browse to http://localhost:3000 to view available parking slots.
Use the buttons to book or release a slot.
Admin Panel:

Navigate to http://localhost:3000/admin to log in as an admin.
After login, you'll be redirected to the admin dashboard where you can add or delete parking slots.
Admin Panel
Admin Login: Use the endpoint /admin/login with your admin credentials (create an admin using the create_admin.py script in the backend).

Example to create an admin:

```bash
python create_admin.py admin mypassword
```

Managing Slots: After logging in, use the admin panel to add new parking slots, delete existing ones or release the booked ones.

Troubleshooting
Network Issues: Ensure that your backend (FastAPI) is running and accessible from your React app. Adjust the API URL in your Axios requests if needed (try http://127.0.0.1:8000 or use the proxy option in package.json).

CORS Issues: Verify that CORS is correctly configured in main.py:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
Conda Environment: Make sure you have activated your conda environment before running the backend commands:

```bash
conda activate smart_parking_env
```
