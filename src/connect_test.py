import serial
import time

# Replace '/dev/ttyUSB0' with your actual serial port (e.g., COM3 on Windows)
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=5)

# Function to wait for the printer to respond with 'ok' or 'start'
def wait_for_response():
    while True:
        response = ser.readline().decode('utf-8').strip()
        print(f"Printer response: {response}")
        
        # Continue on certain non-critical responses
        if 'TF init fail' in response:
            print("SD card initialization failed. Continuing with USB commands.")
        elif 'start' in response.lower():
            print("Printer initialized.")
            return True
        elif 'ok' in response.lower():
            return True
        
        # Catch unexpected responses or errors
        elif not response:
            print("No response, retrying...")
            time.sleep(1)  # Retry after a short delay
        else:
            print(f"Unexpected response: {response}")

# Send command and wait for 'ok' response
def send_gcode(command):
    ser.write(f"{command}\n".encode())
    print(f"Sent: {command}")
    if wait_for_response():
        print(f"G-code {command} executed successfully")

# Initialize connection with the printer
def initialize_printer():
    # Wait for the printer to send 'start' after powering up
    print("Waiting for printer to initialize...")
    if wait_for_response():
        # Send M110 to set the line number (handshake)
        send_gcode('M110 N0')

        # Optionally, send M105 to request temperature report (another handshake)
        send_gcode('M105')

# Example function to move the printer
def move_to_corners():
    # Home the printer
    send_gcode('G28')

    # Move to Z-height 10mm for safety
    send_gcode('G1 Z10 F3000')

    # Move to each corner with pauses
    corners = [
        ('G1 X0 Y0 F3000', 'Corner 1: Front-left'),
        ('G1 X220 Y0 F3000', 'Corner 2: Front-right'),
        ('G1 X220 Y220 F3000', 'Corner 3: Back-right'),
        ('G1 X0 Y220 F3000', 'Corner 4: Back-left'),
    ]

    # Repeat moving to corners twice
    for _ in range(2):  # Adjust the range to repeat more/less
        for gcode, description in corners:
            print(description)
            send_gcode(gcode)
            send_gcode('G4 P500')  # Pause for 500 milliseconds

    # Return to center
    send_gcode('G1 X110 Y110 F3000')

# Main program
if __name__ == '__main__':
    try:
        # Initialize communication with the printer
        initialize_printer()

        # Move the printer as an example
        move_to_corners()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the serial connection when done
        ser.close()
        print("Serial connection closed.")
