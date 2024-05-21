import RPi.GPIO as GPIO
from lib.pn532_nfc_hat.pn532 import PN532_SPI

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
                print('Found card with UID:', [hex(i) for i in uid])
                card_scanned = True

    except PN532.PN532Exception as e:
        print(e)
    finally:
        GPIO.cleanup()