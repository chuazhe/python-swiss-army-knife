import sys
import sqlite3
import os
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QStackedWidget, QLabel, QMessageBox
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Swiss Army Knife")
        self.setFixedSize(QSize(600, 300))


        self.db_path = os.path.join(os.path.dirname(__file__), "reporting_log.db")
        self.init_db()


        central_widget = QWidget()
        main_layout = QHBoxLayout()


        left_panel = QWidget()
        left_layout = QVBoxLayout()
        self.combobox = QComboBox()
        self.combobox.addItems(["Option 1", "Option 2", "Option 3"])
        left_layout.addWidget(self.combobox)
        button = QPushButton("Go!")
        left_layout.addWidget(button)

        log_button = QPushButton("View Log")
        left_layout.addWidget(log_button)
        left_layout.addStretch()
        left_panel.setLayout(left_layout)


        self.stacked_panel = QStackedWidget()


        option1_widget = QWidget()
        option1_layout = QVBoxLayout()
        option1_layout.addWidget(QLabel("Paste your text here:"))
        option1_layout.addWidget(QTextEdit(""))
        option1_layout.addWidget(QLabel("Generated Text:"))
        generated_text = QTextEdit("")
        generated_text.setReadOnly(True)
        option1_layout.addWidget(generated_text)
        option1_widget.setLayout(option1_layout)


        option2_widget = QWidget()
        option2_layout = QVBoxLayout()
        option2_layout.addWidget(QLabel("This is Option 2 layout"))
        option2_layout.addWidget(QTextEdit("Option 2 content here"))
        option2_widget.setLayout(option2_layout)


        option3_widget = QWidget()
        option3_layout = QVBoxLayout()
        option3_layout.addWidget(QLabel("This is Option 3 layout"))
        option3_layout.addWidget(QTextEdit("Option 3 content here"))
        option3_widget.setLayout(option3_layout)


        self.stacked_panel.addWidget(option1_widget)
        self.stacked_panel.addWidget(option2_widget)
        self.stacked_panel.addWidget(option3_widget)


        self.combobox.currentIndexChanged.connect(self.handle_combobox_change)

        button.clicked.connect(self.handle_button_click)

        log_button.clicked.connect(self.show_log)


        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.stacked_panel, 2)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            detail TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        conn.close()

    def log_action(self, action, detail=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO log (action, detail) VALUES (?, ?)", (action, detail))
        conn.commit()
        conn.close()

    def handle_combobox_change(self, index):
        self.stacked_panel.setCurrentIndex(index)
        option = self.combobox.currentText()
        self.log_action("Option Selected", option)

    def handle_button_click(self):
        option = self.combobox.currentText()
        self.log_action("Go Button Clicked", option)

    def show_log(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT action, detail, timestamp FROM log ORDER BY id DESC LIMIT 20")
        rows = c.fetchall()
        conn.close()
        log_text = "\n".join([f"[{timestamp}] {action}: {detail}" for action, detail, timestamp in rows])
        if not log_text:
            log_text = "No log entries yet."
        QMessageBox.information(self, "Reporting Log", log_text)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
