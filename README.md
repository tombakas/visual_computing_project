# Instructions to run
 - Create a virtual environment using Python3. The argument after `-p` should be the path to your Python3 executable - it differers between systems. This is an example from Fedora Linux: `virtualenv -p /usr/bin/python3 venv`
 - Source the environment: `source venv/bin/activate`
 - Install the dependencies: `pip install -r requirements.txt`
 - Set the FLASK_ENV variable to `development`:
   Windows users: `set FLASK_ENV=development`
   Unix users: `export FLASK_ENV=development`
 - Run the app with `flask run`
 - It's available at `localhost:5000` by default and should reload on code update


# API usage
To use the api, make sure to put the latest version of the database into the **db** 
folder at the root of the project. Records are returned sorted by datetime in
decreasing order. Available api endpoints:

* `/api/calls/latest`:
  This endpoint doesn't take any parameters and returns the 100 latest available calls.
* `/api/calls`:
  This endpoint takes the following parameters:
  * `service`: type of call service, options are: police, ambulance, helicopter
      and fire-brigade. Currently only ambulance and helicopter data is
      available with coordinates.
  * `from`: inclusive date from which records start, format: `YYYY-MM-DD`
  * `to`: inclusive date to which records span, format: `YYYY-MM-DD`
  * `limit`: limit response to latest **n** records.

## Response schema
```yaml
schema:
  type: array
  items:
    type: object
    properties:
      datetime:
        type: string
        format: datetime
      service:
        type: string
      lat:
        type: number
        format: float
      lon:
        type: number
        format: float
      urgency:
        type: string
```
