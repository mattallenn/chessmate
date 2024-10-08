import serial
import time

z_stop = 10 # Height above chess piece to move to when picking up and placing pieces.
z_upper = 75 # Height to move to when moving between squares
velocity = 5000 # Movement velocity

class PrinterController:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        # Initialize serial connection
        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def connect(self):
        try:
            # Open the serial connection
            self.ser = serial.Serial(self.port, self.baudrate, timeout=5)
            time.sleep(2)  # Give the connection some time to establish
            print("Connected to printer.")
        except Exception as e:
            print(f"Failed to connect: {e}")
    
    def send_gcode(self, gcode_commands):
        if self.ser is not None and self.ser.is_open:
            for cmd in gcode_commands:
                self.ser.write((cmd + "\n").encode())  # Send G-code command
                time.sleep(0.1)  # Delay between commands
                response = self.ser.readline().decode('utf-8')  # Read response
                print(f"Response: {response.strip()}")
        else:
            print("Serial connection not open.")

    def disconnect(self):
        if self.ser is not None:
            self.ser.close()
            print("Disconnected from printer.")

# G-code generator function
def generate_gcode(start, end):
    gcode = []
    gcode.append(f"G1 Z75 {velocity}") # Raise Z-axis to avoid hitting the board
    gcode.append(f"G1 X{start[0]} Y{start[1]} Z75 {velocity}")  # Move above start position
    # Make sure gripper is open
    gcode.append(f"G1 Z{z_stop}") # Lower it to pick up the piece at z_stop height
    # Add command to close gripper. Move extruder servo to close gripper?
    gcode.append(f"G1 Z75 {velocity}") # Raise Z-axis to avoid hitting the board
    gcode.append(f"G1 X{end[0]} Y{end[1]} Z10 {velocity}")  # Move above end position
    gcode.append(f"G1 Z10 {velocity}")  # Lower Z-axis to place piece
    # Open gripper
    gcode.append(f"G1 Z75 {velocity}") # Raise Z-axis to avoid hitting the board
    gcode.append(f"G1 X0 Y0 Z75 {velocity}") # Move gripper to home position (back left corner of the board)
    return gcode

# Initialize the printer controller
controller = PrinterController(port="/dev/ttyUSB0", baudrate=115200)

# Connect to the printer once
controller.connect()

# Main control loop
try:
    # Home printer
    controller.send_gcode(["G28"])
    print("Homing printer...")
    time.sleep(5)  # Wait for homing to complete
    print("Printer homed.")

    while True:
        # Simulate receiving a move (you could replace this with input from a chess engine or user input)
        move = input("Enter a move in the format 'e2 e4' (or type 'quit' to exit): ")

        if move.lower() == "quit":
            break

        # Parse the move (for simplicity, assume valid input)
        start_square, end_square = move.split()

        # Define the coordinates of each square on the chessboard
        # TODO: Add the coordinates of all squares. This can be done with a constant distance between squares and a function.
        chessboard_coords = {
            'e4': (50, 90), 
            'e5': (50, 100),
        }

        if start_square in chessboard_coords and end_square in chessboard_coords:
            start_pos = chessboard_coords[start_square]
            end_pos = chessboard_coords[end_square]

            # Generate G-code for the move
            gcode_commands = generate_gcode(start_pos, end_pos)

            # Send G-code to the printer
            controller.send_gcode(gcode_commands)
        else:
            print("Invalid move. Please enter a valid move.")
finally:
    # Always ensure the connection is closed when exiting
    controller.disconnect()
