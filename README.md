# EmergenVis

Emergency dispatch call visualization tool.

<img src="https://i.imgur.com/iOYXj7T.png" width="50%" alt="Map view" title="Map view">
<img src="https://i.imgur.com/Decd6c9.png" width="50%" alt="Graph view" title="Graph view">

## System requirements
 * `python3`
 * `virtualenv`
 * `make`
 * `yarn`
 * `wget`

## Instructions to run
The instructions for running were successfully tested on Linux and macOS. Running the project locally requires that both the **Flask** based backend and the **Vue.js** based
frontentd are spun up. Steps to run:

 1. `cd` to project root
 2. Run `make api`  
    This will pull in the database if it is not available, set up the `virtualenv`,
    install requirements and launch the **Flask** app
 3. Run (in a separate shell) `make serve`  
    This will build and run the **Vue.js** based frontend server

## Usage
* Use the from/to date pickers to choose the interval for which to view emergency calls data. 
  Initially, the interval is the entire span of the data.
* The "Number of incidents" controls how many incidents are being displayed at the same time.
* Use the "Dispatch calls" checkboxes to adjust which calls are displayed.
  Perhaps slightly counterintuitively, when everything is unchecked, all calls are displayed. 
* The "Display points only" toggles between heat map and individual incident
  locations.
* Click the "Graphs" icon to navigate to the bar chart of incident counts.
  Contintuously clicking on the bar graph will narrow down the time interval
  and eventually navigate back to the map screen.

**NOTE:** Map uses only calls with coordinates, while graphs use all calls in
the database.

## API usage
To use the api, make sure to put the latest version of the database into the **db** 
folder at the root of the project. Records are returned sorted by datetime in
decreasing order. Available api endpoints:

* `/api/calls/latest`:
  This endpoint doesn't take any parameters and returns the 100 latest available calls.
* `/api/calls/count`:
  This endpoint doesn't take any parameters and returns the 100 latest available calls.
  This endpoint takes the following parameters:
  * `from`: inclusive date from which records start, format: `YYYY-MM-DD`
  * `to`: inclusive date to which records span, format: `YYYY-MM-DD`
  * `interval`: interval, in which to count calls (year, month, day)
* `/api/calls`:
  This endpoint takes the following parameters:
  * `service`: type of call service, options are: police, ambulance, helicopter
      and fire-brigade. Currently only ambulance and helicopter data is
      available with coordinates.
  * `from`: inclusive date from which records start, format: `YYYY-MM-DD`
  * `to`: inclusive date to which records span, format: `YYYY-MM-DD`
  * `limit`: limit response to latest **n** records.
* `/api/cbs`:
  This endpoint takes the following parameters:
  * `region`: comma separated list of regions to return
  * `columns`: comma separated list of columns returned in response, `region`
      is always included as a column.
* `/api/events`:
  This endpoint takes the following parameters:
  * `city`: comma separated list of cities to return
  * `from`: inclusive date from which records start, format: `YYYY-MM-DD`
  * `to`: inclusive date to which records span, format: `YYYY-MM-DD`
      is always included as a column.
  * `limit`: limit response to latest **n** records.

## Response schema
**calls**
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
