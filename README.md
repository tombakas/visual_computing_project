# Instructions to run
 - Create a virtual environment using Python3. The argument after `-p` should be the path to your Python3 executable - it differers between systems. This is an example from Fedora Linux: `virtualenv -p /usr/bin/python3 venv`
 - Source the environment: `source venv/bin/activate`
 - Install the dependencies: `pip install -r requirements.txt`
 - Set the FLASK_ENV variable to `development`:
   Windows users: `set FLASK_ENV=development`
   Unix users: `export FLASK_ENV=development`
 - Run the app with `flask run`
 - It's available at `localhost:5000` by default and should reload on code update
