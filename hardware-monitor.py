import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMenuBar, QAction, QStatusBar
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPalette

class FancyHardwareMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fancy Hardware Monitor")
        self.setGeometry(200, 200, 700, 500)

        # Setarea unui fundal întunecat
        self.setStyleSheet("font-size: 16px; background-color: #1e1e1e; color: #f5f5f5;")

        # Crearea unei bare de meniu
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Adăugarea secțiunilor în bara de meniu
        cpu_menu = menu_bar.addMenu("CPU")
        memory_menu = menu_bar.addMenu("Memory")
        disk_menu = menu_bar.addMenu("Disk")
        network_menu = menu_bar.addMenu("Network")

        # Crearea acțiunilor din meniu
        cpu_action = QAction("Show CPU Info", self)
        cpu_action.triggered.connect(self.show_cpu_info)
        cpu_menu.addAction(cpu_action)

        memory_action = QAction("Show Memory Info", self)
        memory_action.triggered.connect(self.show_memory_info)
        memory_menu.addAction(memory_action)

        disk_action = QAction("Show Disk Info", self)
        disk_action.triggered.connect(self.show_disk_info)
        disk_menu.addAction(disk_action)

        network_action = QAction("Show Network Info", self)
        network_action.triggered.connect(self.show_network_info)
        network_menu.addAction(network_action)

        # Zona pentru afișarea informațiilor hardware
        self.info_label = QLabel("Select a section from the menu.", self)
        self.info_label.setStyleSheet("font-size: 16px; color: #9C27B0;")
        self.setCentralWidget(self.info_label)

        # Timer pentru actualizarea informațiilor
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)  # Actualizare la fiecare 2 secunde

        # Variabile pentru a monitoriza secțiunea curentă
        self.current_section = None

        # Status bar pentru a arăta informații suplimentare
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("font-size: 16px; background-color: #212121; color: #03A9F4;")

    def update_stats(self):
        """Actualizează datele în funcție de secțiunea curentă."""
        if self.current_section == "CPU":
            self.show_cpu_info()
        elif self.current_section == "Memory":
            self.show_memory_info()
        elif self.current_section == "Disk":
            self.show_disk_info()
        elif self.current_section == "Network":
            self.show_network_info()

    def show_cpu_info(self):
        """Afișează informații despre CPU."""
        self.current_section = "CPU"
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        cpu_freq = psutil.cpu_freq()
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_info = (f"<b>CPU Usage (per core):</b> {cpu_usage}<br>"
                    f"<b>CPU Frequency:</b> {cpu_freq.current:.2f} MHz<br>"
                    f"<b>Cores:</b> {cpu_cores}, <b>Threads:</b> {cpu_threads}")
        self.info_label.setText(cpu_info)
        self.info_label.setStyleSheet("font-size: 16px; color: #03A9F4;")
        self.status_bar.showMessage("CPU Information")

    def show_memory_info(self):
        """Afișează informații despre memorie."""
        self.current_section = "Memory"
        memory_info = psutil.virtual_memory()
        swap_info = psutil.swap_memory()
        memory_info_text = (f"<b>Memory Total:</b> {memory_info.total / (1024 ** 3):.2f} GB<br>"
                            f"<b>Memory Used:</b> {memory_info.used / (1024 ** 3):.2f} GB<br>"
                            f"<b>Memory Free:</b> {memory_info.available / (1024 ** 3):.2f} GB<br>"
                            f"<b>Memory Usage:</b> {memory_info.percent}%<br>"
                            f"<b>Swap Total:</b> {swap_info.total / (1024 ** 3):.2f} GB<br>"
                            f"<b>Swap Used:</b> {swap_info.used / (1024 ** 3):.2f} GB<br>"
                            f"<b>Swap Free:</b> {swap_info.free / (1024 ** 3):.2f} GB<br>"
                            f"<b>Swap Usage:</b> {swap_info.percent}%")
        self.info_label.setText(memory_info_text)
        self.info_label.setStyleSheet("font-size: 16px; color: #E91E63;")
        self.status_bar.showMessage("Memory Information")

    def show_disk_info(self):
        """Afișează informații despre disc."""
        self.current_section = "Disk"
        disk_partitions = psutil.disk_partitions()
        disk_info_text = ""
        for partition in disk_partitions:
            disk_usage = psutil.disk_usage(partition.mountpoint)
            disk_info_text += (f"<b>Device:</b> {partition.device}<br>"
                               f"<b>Mountpoint:</b> {partition.mountpoint}<br>"
                               f"<b>Total Size:</b> {disk_usage.total / (1024 ** 3):.2f} GB<br>"
                               f"<b>Used:</b> {disk_usage.used / (1024 ** 3):.2f} GB<br>"
                               f"<b>Free:</b> {disk_usage.free / (1024 ** 3):.2f} GB<br>"
                               f"<b>Usage:</b> {disk_usage.percent}%<br><br>")
        self.info_label.setText(disk_info_text)
        self.info_label.setStyleSheet("font-size: 16px; color: #8BC34A;")
        self.status_bar.showMessage("Disk Information")

    def show_network_info(self):
        """Afișează informații despre rețea."""
        self.current_section = "Network"
        net_info = psutil.net_io_counters()
        network_info_text = (f"<b>Network Sent:</b> {net_info.bytes_sent / (1024 ** 2):.2f} MB<br>"
                             f"<b>Network Received:</b> {net_info.bytes_recv / (1024 ** 2):.2f} MB<br>"
                             f"<b>Packets Sent:</b> {net_info.packets_sent}<br>"
                             f"<b>Packets Received:</b> {net_info.packets_recv}")
        self.info_label.setText(network_info_text)
        self.info_label.setStyleSheet("font-size: 16px; color: #FFEB3B;")
        self.status_bar.showMessage("Network Information")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FancyHardwareMonitor()
    window.show()
    sys.exit(app.exec_())
