from machine import Pin
from mfrc522 import MFRC522
import time

# PIN SETUP
REED_PIN = 0
PIR_PIN = 5
LED_PIN = 2
BUZZER_PIN = 4

MOTION_LIGHT_SECONDS = 15
DELAY = 0.1
DEBOUNCE_MS = 80

reed = Pin(REED_PIN, Pin.IN, Pin.PULL_UP)
pir = Pin(PIR_PIN, Pin.IN)
led = Pin(LED_PIN, Pin.OUT)
buzzer = Pin(BUZZER_PIN, Pin.OUT)

# RFID setup
rfid = MFRC522(spi_id=0, sck=2, mosi=3, miso=4, rst=1, cs=0)

#Alarm
BUZZER_DURATION_SECONDS = 1

alarm_active = False
alarm_start_time = 0.0

# STATE
bypass_enabled = False
last_motion_time = 0.0
door_open = False
authorized_entry_started = False
last_door_open = False

# RFID
#AUTHORIZED_UID = 1234   # will replace with real authorized card UID
AUTHORIZED_UID = [83, 114, 25, 201]
last_rfid_time = 0
RFID_COOLDOWN = 2   

# For debounce
last_reed = reed.value()
last_change_ms = time.ticks_ms()


def read_reed_debounced():
    global last_reed, last_change_ms

    cur = reed.value()
    now = time.ticks_ms()

    if cur != last_reed:
        last_reed = cur
        last_change_ms = now
        return None

    time_passed = now - last_change_ms
    if time_passed >= DEBOUNCE_MS:
        return cur

    return None


def set_outputs(led_on: bool, buzzer_on: bool):
    if led_on:
        led.value(1)
    else:
        led.value(0)

    if buzzer_on:
        buzzer.value(1)
    else:
        buzzer.value(0)


def update_motion():
    global last_motion_time

    if pir.value() == 1:
        last_motion_time = time.time()

    return (time.time() - last_motion_time) < MOTION_LIGHT_SECONDS


def is_door_open_from_reed(reed_val: int) -> bool:
    return reed_val == 1

def update_alarm(intrusion: bool) -> bool:
    global alarm_active, alarm_start_time

    if intrusion and not alarm_active:
        alarm_active = True
        alarm_start_time = time.time()

    if alarm_active:
        if time.time() - alarm_start_time < BUZZER_DURATION_SECONDS:
            return True
        else:
            alarm_active = False

    return False

def update_led_timer(led_trigger: bool) -> bool:
    global last_motion_time

    if led_trigger:
        last_motion_time = time.time()

    return (time.time() - last_motion_time) < MOTION_LIGHT_SECONDS

def enable_bypass():
    global bypass_enabled
    bypass_enabled = True


def disable_bypass():
    global bypass_enabled
    bypass_enabled = False


def key_card_access(scanned_uid) -> bool:
    '''
    Returns True if scanned UID matches the authorized UID.
    '''
    return scanned_uid == AUTHORIZED_UID


def read_rfid():
    '''
    RFID function.
    will replace this later with real RFID reader code.
    For now it returns None if no card is scanned.
    '''
    result = rfid.SelectTagSN()

    status = result[0]
    uid = result[1]

    if status == rfid.OK:
        return uid

    return None


# MAIN LOOP
print('System starting...')
set_outputs(False, False)

while True:

    current_time = time.time() 

    # Check RFID card
    scanned_uid = read_rfid()

    if scanned_uid is not None:
        #print('Scanned UID:', scanned_uid)

        if key_card_access(scanned_uid):
            if current_time - last_rfid_time > RFID_COOLDOWN:
                enable_bypass()
                authorized_entry_started = False
                last_rfid_time = current_time
                print('Authorized card detected')
        else:
            print('Unauthorized card')

    # 1) Read door state
    stable_reed = read_reed_debounced()
    if stable_reed is not None:
        door_open = is_door_open_from_reed(stable_reed)

    door_open_event = door_open and (not last_door_open)
    last_door_open = door_open

    # If bypass is on and the door opens, authorized entry has started
    if bypass_enabled and door_open:
        authorized_entry_started = True

    # If the door closes again after authorized entry, disable bypass
    if bypass_enabled and authorized_entry_started and (not door_open):
        disable_bypass()
        authorized_entry_started = False
        print('Bypass disabled')

    # 2) Motion detection
    motion_detected = (pir.value() == 1)

    # 3) Intrusion logic
    if bypass_enabled:
        intrusion = False
    else:
        intrusion = door_open_event
    '''
    # Alarm timing 
    buzzer_active = update_alarm(intrusion)

    # 4) Output logic
    if (buzzer_active or motion_active):
        led_on = True
    else:
        led_on = False

    set_outputs(led_on, buzzer_active)
    '''
    # Alarm timing 
    buzzer_active = update_alarm(intrusion)

    # LED trigger: door open OR motion
    led_trigger = door_open_event or motion_detected

    # LED timing (30s)
    led_active = update_led_timer(led_trigger)

    # Output
    set_outputs(led_active, buzzer_active)
    
    # 5) Debugging
    print('door_open:', door_open,'bypass:', bypass_enabled,
          'motion:', motion_detected,'intrusion:', intrusion,
          'authorized_entry_started:', authorized_entry_started)

    time.sleep(DELAY)
