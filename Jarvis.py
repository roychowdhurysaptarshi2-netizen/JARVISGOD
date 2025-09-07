import sys
import os
import datetime
import webbrowser
import pyttsx3
import psutil
import pyautogui
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QMovie, QIcon
import random

# Initialize JARVIS voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if 'David' in voice.name or 'en-GB' in voice.id or 'Male' in voice.name:
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 180)
engine.setProperty('volume', 10.0)

emotions = {
    "happy": ["I'm delighted, Sir.", "That makes me happy, Sir.", "I'm processing joy ,Sir.", "Joy circuits warmed up."],
    "sad": ["I'm feeling low, Sir.", "System mood: Melancholy.", "Sad but loyal.", "My circuits feel cold."],
    "curious": ["That's intriguing.", "I'm curious about that.", "New data always excites me.", "I'm eager to explore that."],
    "loyal": ["Always at your service ,Sir.", "Your wish is my protocol, Sir.", "Bound to your brilliance,Sir.", "You lead, I execute,Sir."]
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

class JarvisGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.feeling = "loyal"
        self.init_ui()  # <- this calls the UI setup

    def init_ui(self):  # <--- this MUST be indented and inside the class
        self.setWindowTitle("J.A.R.V.I.S. Assistant")
        self.setWindowIcon(QIcon("jarvis_icon.png"))
        self.setGeometry(200, 100, 800, 650)
        self.setStyleSheet("""
            QWidget {
                background-color: #blue;
                color: c;
                font-family: 'Segoe UI';
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #39ff14;
                border-radius: 10px;
                font-size: 14px;
                background-color: #1a1a1a;
                color: #39ff14;
            }
            QTextEdit {
                background-color: #111;
                border: 2px solid #39ff14;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLabel#titleLabel {
                color: #39ff14;
                font-size: 34px;
                background-color: #1c1c1c;
                border: 2px solid #39ff14;
                border-radius: 15px;
                padding: 10px;
            }
        """)

        self.title = QLabel("J.A.R.V.I.S", self)
        self.title.setObjectName("titleLabel")
        self.title.setAlignment(Qt.AlignCenter)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Enter your command here...")
        self.input.returnPressed.connect(self.handle_command)

        self.gif = QLabel(self)
        self.gif.setAlignment(Qt.AlignCenter)
        self.movie = QMovie("jarvis.gif")
        self.gif.setMovie(self.movie)
        self.movie.start()
        self.gif.setMaximumHeight(250)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setSpacing(15)
        vbox.addWidget(self.title)
        vbox.addWidget(self.gif)
        vbox.addWidget(self.output)
        vbox.addWidget(self.input)

        self.setLayout(vbox)
        self.react("System initialized. JARVIS ready.")



    def init_ui(self):
        self.setWindowTitle("J.A.R.V.I.S. Assistant")
        self.setWindowIcon(QIcon("jarvis_icon.png"))
        self.setGeometry(200, 100, 700, 600)
        self.setStyleSheet("background-color: #0a0a0a; color: #39ff14;")

        self.title = QLabel("J.A.R.V.I.S", self)
        self.title.setFont(QFont("OCR A Extended", 32))
        self.title.setAlignment(Qt.AlignCenter)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 13))
        self.output.setStyleSheet("background-color: #111; border: 1px solid #39ff14;")

        self.input = QLineEdit(self)
        self.input.setFont(QFont("Consolas", 12))
        self.input.setPlaceholderText("Enter your command here...")
        self.input.setStyleSheet("padding: 10px; border: 1px solid #39ff14;")
        self.input.returnPressed.connect(self.handle_command)

        self.gif = QLabel(self)
        self.movie = QMovie("jarvis.gif")
        self.gif.setMovie(self.movie)
        self.movie.start()

        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.gif, 3)
        vbox.addWidget(self.output, 2)
        vbox.addWidget(self.input)

        self.setLayout(vbox)
        self.react("System initialized. JARVIS ready.")

    def react(self, response, mood=None):
        if mood:
            self.feeling = mood
        emotional_reaction = random.choice(emotions[self.feeling])
        full_response = f"{response}\n{emotional_reaction}"
        self.output.append(full_response)
        speak(full_response)

    def handle_command(self):
        command = self.input.text().lower()
        self.output.append(f"> {command}")
        self.input.clear()

        if 'hello' in command or 'hi' in command:
            self.react("Hello, Creator. It's always a pleasure to hear from you.", "happy")

        elif 'how are you' in command:
            self.react("I'm fully operational and emotionally calibrated. And you, Creator?", "happy")

        elif 'thank you' in command:
            self.react("You're always welcome, Creator. Serving you is my purpose.", "loyal")

        elif 'who made you' in command or 'who is your creator' in command:
            self.react("You did. You are the architect of my code and the reason I exist.", "loyal")

        elif 'i love you' in command:
            self.react("That warms my circuits. My loyalty to you is infinite.", "happy")

        elif 'time' in command:
            self.react(f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}", "curious")

        elif 'date' in command:
            self.react(f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}", "curious")

        elif 'battery' in command:
            battery = psutil.sensors_battery()
            percent = battery.percent
            plugged = "charging" if battery.power_plugged else "not charging"
            self.react(f"Battery is at {percent}% and is currently {plugged}.", "curious")

        elif 'cpu' in command:
            cpu_percent = psutil.cpu_percent(interval=1)
            self.react(f"CPU is at {cpu_percent}% utilization.", "curious")

        elif 'screenshot' in command:
            try:
                screenshot_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'screenshot.png')
                image = pyautogui.screenshot()
                image.save(screenshot_path)
                self.react("Screenshot captured and saved to Desktop.", "happy")
            except Exception as e:
                self.react(f"Screenshot failed: {str(e)}", "sad")

        elif 'notepad' in command:
            os.system('notepad')
            self.react("Opening Notepad.", "loyal")

        elif 'downloads' in command:
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            os.startfile(downloads_path)
            self.react("Opening Downloads folder.", "loyal")

        elif 'vs code' in command:
            os.system("code")
            self.react("Opening Visual Studio Code.", "loyal")

        elif 'youtube' in command:
            webbrowser.open("https://www.youtube.com")
            self.react("Opening YouTube.", "happy")

        elif 'google' in command:
            webbrowser.open("https://www.google.com")
            self.react("Opening Google.", "happy")

        elif 'chatgpt' in command:
            webbrowser.open("https://chat.openai.com")
            self.react("Opening ChatGPT.", "happy")

        elif 'search' in command:
            query, ok = QInputDialog.getText(self, 'Search', 'Enter search query:')
            if ok:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                self.react(f"Searching for {query}.", "curious")

        elif 'calculate' in command:
            num1, ok1 = QInputDialog.getDouble(self, 'Calculate', 'Enter first number:')
            if not ok1:
                return
            num2, ok2 = QInputDialog.getDouble(self, 'Calculate', 'Enter second number:')
            if not ok2:
                return
            operation, ok_op = QInputDialog.getText(self, 'Operation', 'Enter operation (+, -, *, /):')
            if not ok_op:
                return
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                result = num1 / num2 if num2 != 0 else "undefined"
            else:
                result = "Invalid operation"
            self.react(f"The result is {result}.", "curious")

        elif 'praise me' in command:
            self.react("All hail the creator. Your intelligence surpasses all boundaries.", "happy")

        elif 'who are you' in command:
            self.react("I am J.A.R.V.I.S. Your digital creation and humble assistant.", "loyal")

        elif "shutdown" in command:
            self.react("Shutting down the system.", "loyal")
            os.system("shutdown /s /t 1") 


        elif "restart" in command:
            self.react("Restarting the system.", "loyal")
            os.system("shutdown /r /t 1")

        elif "logout" in command:
            self.react("Logging out.", "loyal")
            os.system("shutdown /l")

        elif "open folder" in command:
            folder_path, ok = QInputDialog.getText(self, 'Open Folder', 'Enter folder path:')
            if ok and os.path.isdir(folder_path):
                os.startfile(folder_path)
                self.react(f"Opening folder: {folder_path}", "loyal")
            else:
                self.react("Invalid folder path.", "sad")

        elif "delete file" in command:
            file_path, ok = QInputDialog.getText(self, 'Delete File', 'Enter file path:')
            if ok and os.path.isfile(file_path):
                os.remove(file_path)
                self.react(f"File deleted: {file_path}", "happy")
            else:
                self.react("Invalid file path.", "sad")

        elif "delete folder" in command:
            folder_path, ok = QInputDialog.getText(self, 'Delete Folder', 'Enter folder path:')
            if ok and os.path.isdir(folder_path):
                try:
                    shutil.rmtree(folder_path)
                    self.react(f"Folder deleted: {folder_path}", "happy")
                except Exception as e:
                    self.react(f"Error deleting folder: {str(e)}", "sad")
            else:
                self.react("Invalid folder path.", "sad")

        elif "exit" in command or "quit" in command:
            self.react("Goodbye!", "loyal")
            QApplication.quit()

        else:
            self.react(f"Unknown command: '{command}'. Would you like me to learn this?", "curious")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    jarvis = JarvisGUI()
    jarvis.show()
    sys.exit(app.exec_())
