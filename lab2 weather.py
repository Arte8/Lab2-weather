lab2 weather

import requests
import pandas as pd

url = "https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto"
