import psutil
from time import sleep
from threading import Thread
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from vortexui.windows import FMainWindow
from vortexui.widgets import FProgressBar
from vortexui.theme_engine import ThemeEngine
from core.sys_info import get_processes, get_sys_info
from PySide6.QtWidgets import QApplication, QFormLayout, QTableWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidgetItem

class SystemMonitorApp(FMainWindow):
    def __init__(self):
        super(SystemMonitorApp, self).__init__()

        self.setMinimumSize(500, 600)

        self.setWindowTitle("System Resources")
        self.theme_engine = ThemeEngine()
        self.total_mem = psutil.virtual_memory().total

        self.thread = None

        self.setStyleSheet(self.theme_engine.active_scheme(self.theme_engine.default_theme))        
        self.theme_engine.get_scroll_areas(self)
        self.theme_engine.get_check_boxes(self)
        


        self.upper_layout = QHBoxLayout()
        self.res_info_layout = QFormLayout()
        self.res_info_layout_extra = QFormLayout()
        self.processes_table = QTableWidget()
        

        self.cpu_usage = FProgressBar()
        self.mem_usage = FProgressBar()
        self.swap_usage = FProgressBar()
        self.cpu_usage.setMaximumWidth(200)
        self.swap_usage.setMaximumWidth(200)
        self.mem_usage.setMaximumWidth(200)

        

        self.uptime_val = QLabel()

        self.upper_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.res_info_layout_extra.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.upper_layout.addLayout(self.res_info_layout)
        self.upper_layout.addLayout(self.res_info_layout_extra)

        self.res_info_layout.addRow("CPU: ", self.cpu_usage)
        self.res_info_layout.addRow("Memory: ", self.mem_usage)
        self.res_info_layout.addRow("Swap: ", self.swap_usage)

        self.res_info_layout_extra.addRow("Up time: ", self.uptime_val)
    

        self.add_layout(self.upper_layout)
        self.add_content(self.processes_table)

        self.prepare_table()

        self.start_get_sys_info()

        self.theme_engine.get_table_widgets(self)
    
    def refresh_table(self):
        procs = get_processes()
        self.processes_table.setRowCount(len(procs))
        for index, proc in enumerate(procs):
            self.processes_table.setItem(index, 0, QTableWidgetItem(proc['name']))
            self.processes_table.setItem(index, 1, QTableWidgetItem(proc['pid']))
            self.processes_table.setItem(index, 2, QTableWidgetItem(proc['mem']))

    def prepare_table(self):
        rows = ["Name", "PID", "MEM"]
        self.processes_table.setColumnCount(len(rows))
        self.processes_table.setHorizontalHeaderLabels(rows)
        self.processes_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.processes_table.verticalHeader().setVisible(False)


    def start_get_sys_info(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_sys_info_interval)
        self.timer.start(1000)


    def get_sys_info_interval(self):
        info = get_sys_info()
        self.cpu_usage.setValue(info['cpu'])
        self.mem_usage.setValue(info['mem'])
        self.swap_usage.setValue(info['swap'])
        self.uptime_val.setText(info['uptime'])

        self.processes_table.setRowCount(0)
        self.processes_table.clearContents()

        self.prepare_table()
        self.refresh_table()


app = QApplication()
font = QFont("vortexui/fonts/Rajdhani-Regular.ttf")
app.setFont(font)
win = SystemMonitorApp()
win.show()
app.exec()