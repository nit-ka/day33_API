import requests
from datetime import datetime
import smtplib
import time

my_email = "nit.kinga2@gmail.com"
password = "lejadsojcwweobxa"

MY_LAT = 50.060420
MY_LNG = 19.561750


def is_iss_up():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if abs(iss_latitude - MY_LAT) < 5 and abs(iss_longitude - MY_LNG) < 5:
        return True
    else:
        return False


def is_dark():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if time_now.hour < sunrise or time_now.hour > sunset:
        return True
    else:
        return False


def iss_notification():
    if is_iss_up() and is_dark():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject: ISS notification\n\nHey! Look UP. ISS should be visible on your sky."
            )


while True:
    time.sleep(60)
    iss_notification()
