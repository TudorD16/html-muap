import os
import sys
import socket
import time
import random
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLineEdit, QTextEdit, QMessageBox)

# Commands and simulated messages
messages = {
    "init": "The precondition has been initialized.",
    "powercli Multiapp.exe -t":"On",
    "getscan register mov eax, eay: shell True":"",
    "1/0,12": "Register OK.",
    "0/0,8": "Register OK.",
    "start,1/0/0": "eax=1;\neay=0;",
    "restart_service": "The service has been restarted.",
    "X/1,0": "256 Bytes",
    "X/1,1": "18 Bytes",
    "CLI/1/0/0,t": "Positive Response()",
    "cfg,0/0/1":"Session terminated.",
    "launch_multiapp": "Launching Multiapp.exe..."
}

# Display error as a popup window using PyQt5
def show_error(title, message):
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setWindowTitle(title)
    error_box.setText(message)
    error_box.exec_()
    sys.exit(1)  # Close application after showing error

# Check internet connection
def check_internet():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        show_error("Error", "You are not connected to the internet.")
        return False

# Check if 'Multiapp.exe' exists in the same folder
def check_file():
    if os.path.isfile("Multiapp.exe"):
        return True
    else:
        show_error("Error", "'Multiapp.exe' file not found in the same folder.")
        return False

# Save each output to log.txt
def save_to_log(command, response):
    with open("log.txt", "a") as log:
        log.write(f"Command: {command}\nResponse: {response}\n---\n")

# Process command and save to log
def process_command(command):
    if command in messages:
        response = messages[command]
        if command == "launch_multiapp":  # Launch Multiapp.exe
            try:
                subprocess.Popen(["Multiapp.exe"], shell=True)  # Start the executable
            except Exception as e:
                response = f"Failed to launch Multiapp.exe: {str(e)}"
    else:
        response = "Unknown command. Please try again."
    save_to_log(command, response)
    return response

# Simulate commands in command line
def simulate_command_cli():
    while True:
        command = input("Enter a command: ")
        response = process_command(command)

        # Introduce a random delay between 1 and 3 seconds
        time.sleep(random.randint(1, 3))

        print(f"Response: {response}")

# GUI application class
class CommandSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shell Integrator")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter a command...")
        self.command_input.returnPressed.connect(self.submit_command)  # Connect Enter key
        self.layout.addWidget(self.command_input)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_command)
        self.layout.addWidget(self.submit_button)

        self.response_display = QTextEdit(self)
        self.response_display.setReadOnly(True)
        self.layout.addWidget(self.response_display)

    def submit_command(self):
        command = self.command_input.text()
        response = process_command(command)

        # Introduce a random delay between 1 and 3 seconds
        time.sleep(random.randint(1, 3))

        self.response_display.append(f"Command: {command}\nResponse: {response}\n")
        self.command_input.clear()

# Main function
def main():
    # Initial checks
    if not check_internet() or not check_file():
        sys.exit(1)  # Close the application if any check fails

    # Ask user to choose mode
    mode = input("Choose mode: Enter '1' for Command Line or '2' for GUI: ")
    if mode == '1':
        simulate_command_cli()
    elif mode == '2':
        app = QApplication(sys.argv)
        window = CommandSimulatorApp()
        window.show()
        sys.exit(app.exec_())
    else:
        print("Invalid choice. Please restart the application and choose 1 or 2.")

if __name__ == "__main__":
    main()
