# Columbia University Lion Dance App

[![codecov](https://codecov.io/gh/ew2664/culd-app/branch/main/graph/badge.svg?token=XU966851SF)](https://codecov.io/gh/ew2664/culd-app)

## Quick Start

This project uses a Django backend with a React.js frontend.
Make sure that you have both Python 3 and Node.js installed on your machine.

Install the required Python dependencies for the backend by running
`pip install -r requirements.txt` in the `backend` directory.

To set up the SQLite database, run Django migrations, and load in the dummy data, you can run the shell script ```backend/loaddb.sh```.
Alternatively, once the backend server is started (see below), you can log into the Django admin site to enter dummy data yourself.

To start the backend server, in the `backend` directory run `python manage.py runserver`.

To start the frontend server, in the `frontend` directory run `npm start`.
