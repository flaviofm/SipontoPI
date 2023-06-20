import simpleaudio as sa
import requests
from astral.sun import sun
from astral import LocationInfo
from datetime import datetime, timedelta
import threading
import subprocess
import pytz
import os
from time import sleep
import logging

logging.basicConfig(filename='script.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def infolog(str):
    print(str)
    logging.info(str)

infolog("---------------------------------------------")
infolog("INITIALISING SipontoSunset v1.2 - prod 20:30")
infolog("RUNTIME " + str(datetime.now()))
def download(url, save_path):
    counter = 0
    while True:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            infolog("File Downloaded")
        except Exception as e:
            infolog("INTERNET ERROR", e)
            counter += 1
            if(counter > 5):
                infolog("NO WAY TO DOWNLOAD, PLAYING LAST DOWNLOADED TRACK")
                return
            sleep(1)

# Global variables
URL = 'https://likeyousrl.com/siponto/inarena.wav'
# URL = 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID'

DIR_PATH = "./.tracks/"
FILE_PATH = './.tracks/inarena.wav'  # Replace with the desired file path to save the .wav file
LATITUDE = 41.6083133549754  # Basilica
LONGITUDE = 15.889447794802745  # Basilica

ADJUSTMENT_H = 0
ADJUSTMENT_M = 9
ADJUSTMENT_S = 87
# LATITUDE = 47.250000   # Replace with the actual latitude of your location
# LONGITUDE = 129.733333  # Replace with the actual longitude of your location

def initTrack():
    infolog("Checking track")
    
    isExist = os.path.exists(DIR_PATH)
    if not isExist:
        os.makedirs(DIR_PATH)
    # download(URL, FILE_PATH)

    # # Download the track from the URL and save it locally
    # counter = 0
    # while True:
    #     try:
    #         response = requests.get(URL, timeout=30)
    #         infolog("RESPONSE LOADED")
    #         break
    #     except Exception as e:
    #         infolog("INTERNET ERROR", e)
    #         counter += 1
    #         if(counter > 5):
    #             infolog("NO WAY TO DOWNLOAD, PLAYING LAST DOWNLOADED TRACK")
    #             return
    #         sleep(1)

    # # response = requests.get(URL)
    # with open(FILE_PATH, 'wb') as file:
    #     # infolog(response.content)
    #     infolog("Writing...")
    #     file.write(response.content)
    # file.close()
    # infolog("Track downloaded successfully.")

def playTrack():
    infolog("PLAYING")
    # Play the previously downloaded track using a media player
    # subprocess.run(['mpg123', FILE_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # subprocess.run(['aplay', FILE_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wave_obj = sa.WaveObject.from_wave_file(FILE_PATH)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    infolog("ENDED")


def run_at_sunset():
    # Run the playTrack function when the sunset time is reached
    playTrack()
    # Restart the whole process
    initTrack()
    calculate_and_schedule()

def calculate_and_schedule():
    # Calculate the sunset time
    time_difference = -1
    checkDate = datetime.now()
    while(time_difference < 0):
        location = LocationInfo(latitude=LATITUDE, longitude=LONGITUDE)
        s = sun(location.observer, date=checkDate)
        sunset_time = s['sunset']
        checkDate += timedelta(days=1)
        # Calculate the time difference between the current time and the sunset time
        current_time = datetime.now(pytz.timezone(location.timezone))
        # current_time.replace(
        #     hour=current_time.hour+ADJUSTMENT_H,
        #     minute=current_time.minute+ADJUSTMENT_M,
        #     second=current_time.second+ADJUSTMENT_S)
        datetime_difference = (sunset_time - current_time)

        # ADJUSTMENT
        delta = timedelta(hours=ADJUSTMENT_H, minutes=ADJUSTMENT_M, seconds=ADJUSTMENT_S)
        datetime_difference -= delta
        infolog("TIME ADJUSTED" + str(datetime_difference))

        time_difference = datetime_difference.total_seconds()

        sec = time_difference % 60
        min_time = (time_difference - sec) / 60
        min = min_time % 60
        h_time = (min_time - min) / 60
        h = h_time

        infolog(
            "Will play at " + str(sunset_time.astimezone(pytz.timezone('Europe/Rome'))) +
            "\Current time " + str(current_time.astimezone(pytz.timezone('Europe/Rome'))) +
            "\nSunset in " + str(h) + "hours - " + str(min) + " min - " + str(sec) + " secs"
        )

    
    # Schedule the event to run at the sunset time
    t = threading.Timer(time_difference, run_at_sunset)
    t.start()
    # while True:
    #     current_time = datetime.now(pytz.timezone(location.timezone))
    #     datetime_difference = (sunset_time - current_time)

    #     delta = timedelta(hours=ADJUSTMENT_H, minutes=ADJUSTMENT_M, seconds=ADJUSTMENT_S)
    #     datetime_difference -= delta
    #     infolog("TIME ADJUSTED" + str(datetime_difference))

    #     time_difference = datetime_difference.total_seconds()
    #     if(time_difference < 0):
    #         break
    #     infolog(str(time_difference) + " till sunset")
    #     sleep(3)

# Initial setup
initTrack()
infolog("SipontoSunset IS READY")
calculate_and_schedule()