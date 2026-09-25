# Lab2-weather
please install dependency with:
(python -m pip install --user requests)
(python -m pip install requests pandas)

simply clone this repo:   (clone lab2weather\Lab2-weather> python .\lab2weather.py)
and at app root folder run:
(python lab2weather.py)


Lab2 capstone prep Art Lobrin

weather data aggregation app that gives data on average 
temperature and total precipitation for a given date, useful for 
collecting data and determining patterns and as historical reference.

data source https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto
each record represents average temperature, total precipitation and record count 168.

json excerpt ex.   overall_statistics": {
    "minimum_temperature": 7.3,
    "maximum_temperature": 22.6,
    "mean_temperature": 14.654166666666667,
    "minimum_precipitation": 0.0,
    "maximum_precipitation": 0.0,
    "mean_precipitation": 0.0,
    "total_precipitation": 0.0
  },
  "daily_statistics": {
    "2026-09-18": {
      "average_temperature": 17.429166666666667,
      "total_precipitation": 0.0,
      "record_count": 24
    },

problems averted:
Invalid timestamps	Uses pd.to_datetime() to validate dates and rejects invalid timestamps.
Unequal array lengths	Checks that timestamps, temperatures and precipitation arrays have equal lengths. Raises a ValueError if they differ.
Invalid numerical values	Uses math.isfinite() to reject NaN and infinite values.
Negative precipitation	Rejects records with precipitation below zero.
Insufficient data	Stops processing if fewer than 50 records are downloaded or fewer than 50 valid records remain.
simply clone this repo
and at app root folder run:
python lab2weather.py

collection types:
List []	Stored weather records and collected valid records.	Lists preserve order and allow new records to be added using append().
Tuple ()	Grouped each record's timestamp, temperature and precipitation.	Tuples keep related values together and are immutable.
Dictionary {}	Stored overall statistics, daily summaries and JSON output.	Dictionaries organize information using descriptive keys, making values easy to access.
Set {}	Identified unique dates in the weather records.	Sets automatically eliminate duplicate dates.


enjoy
and give Art good grades!
