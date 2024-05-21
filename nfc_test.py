import RPi.GPIO as GPIO
import binascii
import os
from pn532 import *
from dotenv import load_dotenv
from csv_utils import get_value_from_csv_or_remote

load_dotenv()

REMOTE_CSV_LOCATION = os.getenv('REMOTE_CSV_LOCATION')

if __name__ == '__main__':
    try:
        #pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        #pn532 = PN532_I2C(debug=False, reset=20, req=16)
        pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        card_scanned = False

        while not card_scanned:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)

            if uid is not None:
                uid_str = binascii.hexlify(uid).decode()[2:]
                print(uid_str)

                # Call the get_value_from_csv_or_remote function with the UID as the key
                csv_file = "file.csv"
                value = get_value_from_csv_or_remote(uid_str, csv_file, REMOTE_CSV_LOCATION)
                print(value)

                card_scanned = True

    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()