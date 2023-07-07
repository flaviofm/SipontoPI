import simpleaudio as sa
import requests
# from astral.sun import sun
# from astral import LocationInfo
from datetime import datetime, timedelta
import threading
import subprocess
import pytz
import os
from time import sleep
import logging

import librosa
import soundfile as sf

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

def playTrack():
    infolog("PLAYING")
    # Play the previously downloaded track using a media player
    # subprocess.run(['mpg123', FILE_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # subprocess.run(['aplay', FILE_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ##wave
    wave_obj = sa.WaveObject.from_wave_file(FILE_PATH)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    infolog("ENDED")

def run_at_sunset():
    # Run the playTrack function when the sunset time is reached
    playTrack()
    # Restart the whole process
    initTrack()
    run()
    # calculate_and_schedule()

    ############NEW VERSION
def get_diff(h, m):
    now = datetime.now()
    dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
    while(dt < now):
        dt += timedelta(days=1)
    diff = dt - now
    return diff


def schedule_time(t):
    # Schedule the event to run at the sunset time
    diff = t.total_seconds()
    infolog(
        "\nWill play in " + str(diff) + " secs"
    )
    t = threading.Timer(diff, run_at_sunset)
    t.start()


def run():
    d1 = get_diff(15, 25)
    d2 = get_diff(15, 40)
    if(d1 < d2):
        print("Starting time 1")
        schedule_time(d1)
    else:
        print("Starting time 2")
        schedule_time(d2)

# Initial setup
initTrack()
infolog("SipontoSunset IS READY")
# calculate_and_schedule()
run()