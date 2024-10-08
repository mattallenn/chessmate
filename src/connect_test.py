import serial
import time

# Connect to the printer, send G-code home command, and receive response

# Open the serial connection
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
time.sleep(2)  # Give the connection some time to establish
print("Connected to printer.")

# Send G-code command to home the printer
ser.write("G28\n".encode())
time.sleep(0.5)  # Delay between commands
response = ser.readline().decode('utf-8')  # Read response
print(f"Response: {response.strip()}")

# Close the serial connection
ser.close()
print("Disconnected from printer.")

