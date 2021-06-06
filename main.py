import datetime
import os
import sys
import time
import winsound
from sqlite3 import connect
from threading import Thread
import random
import PySide6
from functools import partial
from PySide6 import QtGui,  QtCore
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread
import QToggleSwitch

# -----------------------------------------------

class Timer(QThread):
    def __init__(self, h=0, m=0, s=0):
        super(Timer, self).__init__()
        self.h = h
        self.m = m
        self.s = s
        timer_in_progress = False

    def reset(self):
        self.h = window.ui.sp_hour.value()
        self.m = window.ui.sp_min.value()
        self.s = window.ui.sp_sec.value()

    def decrease(self):
        if self.h != 0 or self.m != 0 or self.s != 0 :
            if self.s == 0:
                self.s = 59
                if self.m != 0:
                    self.m -= 1
            else:
                self.s -= 1

            if self.m == 0:
                if self.h != 0:
                    self.m = 59
                    self.h -= 1
            return True
        else:
            return False

    def run(self):
        while self.decrease():
            if self.h < 10:
                self.H = '0' + str(self.h)
            else:
                self.H = str(self.h)

            if self.m < 10:
                self.M = '0' + str(self.m)
            else:
                self.M = str(self.m)

            if self.s < 10:
                self.S = '0' + str(self.s)
            else:
                self.S = str(self.s)

            window.ui.lbl_timer.setText(f"{self.H}:{self.M}:{self.S}")
            time.sleep(1)
        else:
            # QMessageBox.warning(PySide6.QtWidgets.QWidget, 'Warning', '@@@ Time Out @@@')
            # mes_box = QMessageBox()
            # mes_box.setText("@@@ Time Out @@@")
            # mes_box.exec()
            winsound.Beep(440, 250)
            Timer.timer_in_progress = False
# ----------------------------------------------------------------------------------





class StopWatch(QThread):
    def __init__(self):
        super(StopWatch, self).__init__()
        self.h = 0
        self.m = 0
        self.s = 0

    def reset(self):
        self.h = 0
        self.m = 0
        self.s = 0

    def increase(self):
        self.s += 1
        if self.s >=60:
            self.s = 0
            self.m += 1

        if self.m >= 60:
            self.m = 0
            self.h += 1

    def run(self):
        while True:
            self.increase()
            if self.h < 10:
                self.H = '0' + str(self.h)
            else:
                self.H = str(self.h)

            if self.m < 10:
                self.M = '0' + str(self.m)
            else:
                self.M = str(self.m)

            if self.s < 10:
                self.S = '0' + str(self.s)
            else:
                self.S = str(self.s)

            window.ui.lbl_stopwatch.setText(f"{self.H}:{self.M}:{self.S}")
            time.sleep(1)

# ---------------------------------------------------------------------------


class Alarm(QThread):
    def __init__(self, clock_h=0, clock_m=0, clock_s=0, days=[]):
        super(Alarm, self).__init__()
        self.h = clock_h  # "12:00:00 AM"
        self.m = clock_m
        self.s = clock_s
        self.days = days

    def run(self):
        while True:
            self.now = datetime.datetime.now()
            time.sleep(1)
            self.current_time = self.now.strftime('%H:%M:%S')
            self.current_day = self.now.strftime('%A')
            self.current_day = self.current_day[0:3].lower()

            alarm_time = f'{self.h}:{self.m}:{self.s}'

            print(alarm_time, self.current_time, self.current_day)
            if self.current_time == alarm_time and self.current_day in self.days :
                winsound.Beep(640, 500)
                break



# ************************************************************************
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.stopwatch = StopWatch()
        self.timer = Timer()
        self.alarm = Alarm()
        loader = QUiLoader()
        self.ui = loader.load('form.ui')

# --------------------------------------------------------------------------
        self.ui.btn_stopwatch_start.clicked.connect(self.startStopWatch)
        self.ui.btn_stopwatch_pause.clicked.connect(self.pauseStopWatch)
        self.ui.btn_stopwatch_reset.clicked.connect(self.stopStopWatch)
        self.ui.btn_record.clicked.connect(self.record_time)

        self.ui.tbl_records.setColumnCount(3)
        self.ui.tbl_records.setRowCount(0)
        self.ui.tbl_records.setHorizontalHeaderLabels(['Laps', 'Record', 'Total'])
# --------------------------------------------------------------------------
        self.ui.btn_timer_reset.clicked.connect(self.stopTimer)
        self.ui.btn_timer_start.clicked.connect(self.startTimer)
        self.ui.btn_timer_pause.clicked.connect(self.pauseTimer)
        Timer.timer_in_progress = False
        #self.ui.p_bar.setValue(100)
# --------------------------------------------------------------------------
        self.ui.btn_active.clicked.connect(self.startAlarm)
        self.ui.btn_deactive.clicked.connect(self.stopAlarm)


        self.ui.show()



# ----------------------------
    def startAlarm(self):
        self.ui.lbl_alarm.setText('Alarm Active')

        self.alarm.h = self.ui.alarm_hour.text()
        self.alarm.m = self.ui.alarm_min.text()
        self.alarm.s = self.ui.alarm_sec.text()

        if len(self.alarm.h) < 2:
            self.alarm.h = '0'+self.alarm.h
        if len(self.alarm.m) < 2:
            self.alarm.m = '0'+self.alarm.m
        if len(self.alarm.s) < 2:
            self.alarm.s = '0'+self.alarm.s

        self.alarm.days = []
        if self.ui.chb_sat.isChecked():
            self.alarm.days.append('sat')
        if self.ui.chb_sun.isChecked():
            self.alarm.days.append('sun')
        if self.ui.chb_mon.isChecked():
            self.alarm.days.append('mon')
        if self.ui.chb_thu.isChecked():
            self.alarm.days.append('thu')
        if self.ui.chb_wen.isChecked():
            self.alarm.days.append('wen')
        if self.ui.chb_thr.isChecked():
            self.alarm.days.append('thr')
        if self.ui.chb_fri.isChecked():
            self.alarm.days.append('fri')

        self.alarm.start()

    def stopAlarm(self):
        self.ui.lbl_alarm.setText('Alarm OFF')
        self.alarm.terminate()

        self.ui.alarm_hour.setValue(0)
        self.ui.alarm_min.setValue(0)
        self.ui.alarm_sec.setValue(0)

# --------------------------
    def record_time(self):

        total = self.ui.lbl_stopwatch.text()
        result = self.db_fetch()
        if result:
            last_total = result[-1][2]
            new_record = self.record_calculator(total, last_total)
        else:
            new_record = total

        # print(new_record, total)

        my_con = connect('time.db')
        my_cursor = my_con.cursor()
        my_cursor.execute(f"INSERT INTO time(record, total) VALUES('{new_record}','{total}')")
        my_con.commit()
        result = self.db_fetch()
        result = result[-3:]


        self.ui.tbl_records.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.ui.tbl_records.insertRow(row_num)
            for column_num, data in enumerate(row_data):
                self.ui.tbl_records.setItem(row_num, column_num, QTableWidgetItem(str(data)))

        # table = TableView(result, 4, 3)
        # self.ui.table.setGeometry(QtCore.QRect(150, 70, 93, 28))
        # table.show()

    def record_calculator(self, total, last_record):
        t_h = int(total[0:2])
        t_m = int(total[3:5])
        t_s = int(total[6:])
        l_h = int(last_record[0:2])
        l_m = int(last_record[3:5])
        l_s = int(last_record[6:])

        total_sec = t_h*3600 + t_m*60 + t_s
        last_sec = l_h*3600 + l_m*60 + l_s
        delay = total_sec - last_sec

        if delay//3600 < 10:
            record_h = '0' + str(delay//3600)
        else:
            record_h = str(delay // 3600)
        if delay%3600//60 < 10:
            record_m = '0' + str(delay%3600//60)
        else:
            record_m = str(delay%3600//60)
        if delay%3600%60 < 10:
            record_s = '0' + str(delay%3600%60)
        else:
            record_s = str(delay%3600%60)

        return f"{record_h}:{record_m}:{record_s}"

    def db_fetch(self):
        my_con = connect('time.db')
        my_cursor = my_con.cursor()
        my_cursor.execute("SELECT * FROM time")
        result = my_cursor.fetchall()
        my_con.close()
        return result

    def startStopWatch(self):
        self.del_db()
        self.stopwatch.start()


    def pauseStopWatch(self):
        self.stopwatch.terminate()

    def stopStopWatch(self):
        self.stopwatch.terminate()
        self.stopwatch.reset()
        self.ui.lbl_stopwatch.setText("00:00:00")

        self.del_db()
        self.ui.tbl_records.setRowCount(0)

    def del_db(self):
        my_con = connect('time.db')
        my_cursor = my_con.cursor()
        my_cursor.execute(f"DELETE FROM time")
        my_cursor.execute(f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='time'")
        my_con.commit()
        my_con.close()

# ------------------------------------------------------

    def stopTimer(self):
        self.timer.terminate()
        self.timer.reset()
        self.ui.lbl_timer.setText("00:00:00")
        Timer.timer_in_progress = False

    def startTimer(self):
        if not Timer.timer_in_progress:
            self.timer.h = self.ui.sp_hour.value()
            self.timer.m = self.ui.sp_min.value()
            self.timer.s = self.ui.sp_sec.value()
            Timer.timer_in_progress = True

            # self.ui.p_bar.setValue(100)

        else:
            current_timer = self.ui.lbl_timer.text()
            self.timer.h = int(current_timer[0:2])
            self.timer.m = int(current_timer[3:5])
            self.timer.s = int(current_timer[6:])

        self.timer.start()

    def pauseTimer(self):
        self.timer.terminate()



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())




'''
class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self):
        horHeaders = ['Laps', 'Time', 'Total']
        for n, key in enumerate(self.data):
            for m, item in enumerate(self.data[n]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
'''