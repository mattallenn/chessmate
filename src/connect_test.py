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
def move_printer():
    # Example G-code to move to a specific position
    send_gcode('G1 X50 Y50 Z10 F3000')  # Move to X=50, Y=50, Z=10 at speed F=3000

# Main program
if __name__ == '__main__':
    try:
        # Initialize communication with the printer
        initialize_printer()

        # Move the printer as an example
        move_printer()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the serial connection when done
        ser.close()
        print("Serial connection closed.")
