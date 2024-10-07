# chessmate - robotic chess friend / opponent 


### What is it?

Chessmate is a robotic chess opponent created from a modified Creality Ender-3 3D Printer. A python script, located at `src/chess.py` communicates with the printer via serial communication. The script automatically converts moves into G-Code which is then sent to the printer. 

### Why does this even exist?

Have you ever wanted to play a quick game of chess, and then realized you have no friends? No problem. With chessmate, you can play chess on a physical board! Granted, the opponent is a robot, but you can look past that. Long gone are the days of playing online.

### How does it work?

A 3D printer is just an extruder that is able to move in a coordinate plane. It does this with G-Code, a human readible language that tells the machine where to move, and how. The Ender 3 uses the open-source [Marlin](https://marlinfw.org/) firmware, which is really easy to communicate with. The python script connects to the printer using the serial port and the [pyserial](https://pypi.org/project/pyserial/) library. After that, we simply send the G-Codwith `serial.write()`.

### Isn't this a waste of time? Can't you just play online?

Yes.

