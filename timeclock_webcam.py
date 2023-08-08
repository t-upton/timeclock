import csv
from datetime import datetime
import cv2  # Import the opencv-python library

# Define user data file and clock records file
USER_FILE = "users.txt"
CLOCK_FILE = "times.csv"

# Read user data
def read_users():
    with open(USER_FILE, 'r') as f:
        return [line.strip().split() for line in f]

# Write clock record
def write_clock_record(user, pin, action, shift_duration=None):
    with open(CLOCK_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if shift_duration is not None:
            # Convert timedelta to hours in decimal format
            hours_decimal = shift_duration.total_seconds() / 3600
            writer.writerow([user, pin, action, datetime.now(), "{:.2f}".format(hours_decimal)])
        else:
            writer.writerow([user, pin, action, datetime.now()])

# Read last action of user
def read_last_action(pin):
    with open(CLOCK_FILE, 'r') as f:
        reader = csv.reader(f)
        last_action = None
        last_time = None
        for row in reader:
            if row[1] == pin:
                last_action = row[2]
                last_time = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S.%f")
        return last_action, last_time

def show_clocked_in_users():
    """
    Display users who are currently clocked in.
    """
    clocked_in_users = set()
    with open(CLOCK_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            user, _, action, _ = row[:4]
            if action == "clock-in":
                clocked_in_users.add(user)
            elif action == "clock-out" and user in clocked_in_users:
                clocked_in_users.remove(user)

    if clocked_in_users:
        print("Currently clocked in users:")
        for user in clocked_in_users:
            print(user)
    else:
        print("No users are currently clocked in.")

# Capture image using webcam
def capture_image(filename):
    cap = cv2.VideoCapture(0)  # Open the default camera (0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Save the image
    if ret:
        cv2.imwrite(filename, frame)

    # Release the camera
    cap.release()

# Main function
def main():
    users = read_users()

    print("Welcome to the time tracking system!")

    while True:
        pin = input("PIN: ")

        # Show clocked in users
        if pin.lower() == "0":
            show_clocked_in_users()
            continue

        # Check if the PIN matches a user
        for user, user_pin in users:
            if pin == user_pin:
                last_action, last_time = read_last_action(pin)
                if last_action == "clock-in" and last_time is not None:
                    duration = datetime.now() - last_time
                    print(f"Clocked out successfully! Your shift duration was {duration.total_seconds() / 3600:.2f} hours")
                    filename = f"{user}_clock-out_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    capture_image(filename)
                    write_clock_record(user, pin, "clock-out", duration)
                elif last_action == "clock-out" or last_action is None:
                    filename = f"{user}_clock-in_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    capture_image(filename)
                    write_clock_record(user, pin, "clock-in")
                    print("Clocked in successfully!")
                else:
                    print("You need to clock-in first!")
                break
        else:
            print("Invalid PIN!")

if __name__ == "__main__":
    main()
