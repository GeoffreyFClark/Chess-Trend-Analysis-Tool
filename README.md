# CIS4301 Project

![logo](https://github.com/GeoffreyFClark/Chess-Opening-Database-Project/blob/main/react-frontend/public/logo.png)

![current project image](https://github.com/GeoffreyFClark/Chess-Opening-Database-Project/blob/main/react-frontend/public/screenshotMar20.png)

This project uses React for the frontend and Flask for the backend.

## Prerequisites
- Git
- Node.js (which comes with npm)
- Python 3 (which comes with pip, starting with Python 3.4 and newer)

## Project Setup
Optionally, you may choose to fork the repository if you want to work on your own features independently before merging them into the main project.

Clone the repository:
`git clone https://github.com/GeoffreyFClark/Chess-Opening-Database-Project` </br>
or if forked: `git clone https://github.com/YourGitHubUsername/Chess-Opening-Database-Project`

### Backend setup:

`cd Chess-Opening-Database-Project`

`cd python-backend`

`python -m venv venv`

`venv\Scripts\activate` (On Mac: `source venv/bin/activate`)

`pip install -r requirements.txt`

### Frontend setup:

`cd ../react-frontend`

`npm install`

### OracleDB Connection setup:

1. Navigate to backend directory

`cd python-backend`

2. Start virtual environment

`venv\Scripts\activate` (On Mac: `source venv/bin/activate`)

3. Reinstall requirements (oracledb added)

`pip install -r requirements.txt` 

  OR install oracledb directly

`pip install oracledb`

4. Navigate to https://www.oracle.com/database/technologies/instant-client.html and install Oracle client

5. Add Oracle client path as a system variable within environment variables.

  Important: Name this system variable ORACLE_HOME.

  Windows: System->About->Advanced system settings->Environment Variables->Add New in System Variables

NOTE that usage of OracleDB via a UF account requires an active Gatorlink VPN connection.

## Run the Development Server

Navigate to the flask_backend directory and run `python server.py`

In a new terminal, navigate to the react_frontend directory and run `npm run dev`

View at the frontend's localhost:port which will then be linked in the terminal.


