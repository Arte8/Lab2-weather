#libraries#
import requests
import pandas as pd
import json
import math

from pathlib import Path
from collections import defaultdict

#url var#
URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=43.65&longitude=-79.38"
    "&hourly=temperature_2m,precipitation"
    "&past_days=7&forecast_days=0"
    "&timezone=America/Toronto"
)


def download_weather(url):
    #Download weather data, requested from url and times out after 15 seconds
    response = requests.get(url, timeout=15)
    #raise error#
    response.raise_for_status()
    #returns to json()#
    return response.json()


def process_weather(data):
    #Validate records from data#
    #declares hourly var from data "hourly" from url table#
    hourly = data["hourly"]
    #declares times variable from hourly from "time" from table#
    times = hourly["time"]
    #further var declarations from [xxxxtable#]
    temperatures = hourly["temperature_2m"]
    precipitation = hourly["precipitation"]
    #check for error based on data length check check#
    if not (
        len(times) == len(temperatures) == len(precipitation)
    ):
        raise ValueError("Weather data arrays have different lengths.")

    # List comprehension creates the original records.#
    records = [
        (time, temp, rain)
        for time, temp, rain
        #checks that all three lists forequal lengths before using zip(). 
        # keeps weather records from being discarded"
        in zip(times, temperatures, precipitation)
    ]
    #Creates an empty list that will store weather records that pass validation.#
    valid_records = []
    #counts rejected records#
    rejected = 0

    for time, temp, rain in records:
        try:
            #timestamp var called by pd to datetime tuple time with error exception#
            timestamp = pd.to_datetime(time, errors="raise")
        #checks whether timestamp is missing#
            if pd.isna(timestamp):
                raise ValueError("Missing timestamp")
        #temperature and precipitation values from the weather API into floating-point numbers (float).
            temperature = float(temp)
            rainfall = float(rain)
            #therwise#
            if not (
                math.isfinite(temperature)
                and math.isfinite(rainfall)
            ):
                raise ValueError("Missing or non-finite value")

            if rainfall < 0:
                raise ValueError("Negative precipitation")
            #adds a validated weather record#
            valid_records.append(
                (timestamp, temperature, rainfall)
            )
        #counts how many invalid weather records are encountered.#
        except (ValueError, TypeError, OverflowError):
            rejected += 1
        #converts your list of valid weather records into a Pandas DataFrame#
    df = pd.DataFrame(
        valid_records,
        columns=["time", "temperature", "precipitation"]
    )
#returns three values from your process_weather() function to call#
    return df, len(records), rejected


def calculate_statistics(df):
    #Calculate overall temperature and precipitation statistics.#

    return {
        "minimum_temperature": float(df["temperature"].min()),
        "maximum_temperature": float(df["temperature"].max()),
        "mean_temperature": float(df["temperature"].mean()),
        "minimum_precipitation": float(df["precipitation"].min()),
        "maximum_precipitation": float(df["precipitation"].max()),
        "mean_precipitation": float(df["precipitation"].mean()),
        "total_precipitation": float(df["precipitation"].sum())
    }


def calculate_daily_statistics(df):
    #Group using a dictionary.defaultdict(list) creates an empty list when accessing#
    # a nonexistent dictionary key#

    daily_records = defaultdict(list)

    for row in df.itertuples(index=False):
        date = row.time.date().isoformat()

        daily_records[date].append(
            (row.temperature, row.precipitation)
        )

    # Dictionary comprehension calculates daily statistics.
    daily_summary = {
        date: {
            "average_temperature": sum(
                record[0] for record in records
            ) / len(records),

            "total_precipitation": sum(
                record[1] for record in records
            ),

            "record_count": len(records)
        }
        for date, records in daily_records.items()
    }

    return daily_summary


def get_unique_dates(df):
    """Use a set to identify unique dates in the dataset."""

    unique_dates = {
        timestamp.date().isoformat()
        for timestamp in df["time"]
    }

    return sorted(unique_dates)


def create_summary(url, df, downloaded, rejected):
    """Combine the statistics and record counts into a summary."""

    return {
        "source_url": url,
        "records_downloaded": downloaded,
        "records_processed": len(df),
        "records_rejected": rejected,
        "unique_dates": get_unique_dates(df),
        "overall_statistics": calculate_statistics(df),
        "daily_statistics": calculate_daily_statistics(df)
    }


def save_summary(summary):
    """Save the weather summary to a UTF-8 JSON file."""

    output_file = Path("weather_summary.json")

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, allow_nan=False)

    return output_file


def main():
    """Run the weather download, analysis and export workflow."""

    try:
        data = download_weather(URL)

        df, downloaded, rejected = process_weather(data)

        if downloaded < 50:
            print("Error: Fewer than 50 records downloaded.")
            return

        if len(df) < 50:
            print("Error: Fewer than 50 valid records available.")
            print("Rejected records:", rejected)
            return

        summary = create_summary(
            URL, df, downloaded, rejected
        )

        stats = summary["overall_statistics"]

        print("Minimum temperature:",
              stats["minimum_temperature"], "°C")
        print("Maximum temperature:",
              stats["maximum_temperature"], "°C")
        print("Mean temperature:",
              stats["mean_temperature"], "°C")

        print("Minimum precipitation:",
              stats["minimum_precipitation"], "mm")
        print("Maximum precipitation:",
              stats["maximum_precipitation"], "mm")
        print("Mean precipitation:",
              stats["mean_precipitation"], "mm")

        print("\nDaily statistics:")

        for date, values in summary["daily_statistics"].items():
            print(date, values)

        output_file = save_summary(summary)

        print("\nRecords downloaded:", downloaded)
        print("Records processed:", len(df))
        print("Records rejected:", rejected)
        print("Summary saved to:", output_file)

    except requests.RequestException as error:
        print("Weather download failed:", error)

    except (ValueError, KeyError, TypeError) as error:
        print("Weather data error:", error)

    except OSError as error:
        print("Unable to save the JSON file:", error)


if __name__ == "__main__":
    main()
