from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys, os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
from ctr_energy import ctr_energy
from pyqtspinner.spinner import WaitingSpinner


class monitor(QMainWindow):
    def __init__(self):
        super(monitor, self).__init__()
        self.dirname = os.path.dirname(__file__)
        if self.dirname == "":
            self.dirname = os.getcwd()
        uic.loadUi(self.dirname + '/monitor.ui', self)
        self.db = ctr_energy()
        timenow = datetime.datetime.now()
        self.text_date.setDateTime(timenow)
        self.text_date.dateChanged.connect(lambda: self.run_new_thread("Load_data"))
        self.but_reload.clicked.connect(lambda: self.run_new_thread("Load_data"))
        self.run_new_thread("Load_data")
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_timeout)
        self.timer.start(30000)

    def timer_timeout(self):
        timenow = datetime.datetime.now()
        if int(timenow.strftime("%M")) == 1 or int(timenow.strftime("%M")) == 31:
            self.run_new_thread("Load_data")

    def init_table(self, so_tu):

        self.table.setRowCount(24 * 2)
        self.table.setColumnCount(1 + 4 * so_tu)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        column_name = ["Khung giờ"]
        for i in range(so_tu):
            column_name.append("Cabin")
            column_name.append("Power")
            column_name.append("Date record")
            column_name.append("")
        self.table.setHorizontalHeaderLabels(column_name)
        for i in range(24):
            newitem = QTableWidgetItem(str(i))
            newitem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # newitem.setBackground(QColor(255,0,0))
            self.table.setItem(i * 2, 0, newitem)

    def load_data(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        print(self.text_date.text())
        rs_data = self.db.get_data_server(self.text_date.text())
        if rs_data != None:
            if len(rs_data) > 0:
                list_pi = {}
                for i in range(len(rs_data)):
                    if rs_data[i][1] not in list_pi:
                        list_pi[rs_data[i][1]] = [rs_data[i]]
                    else:
                        list_pi[rs_data[i][1]].append(rs_data[i])

                if len(list_pi) > 0:
                    # print(list_pi)
                    self.init_table(len(list_pi))
                    count = 0
                    for pi in list_pi:

                        for data in list_pi[pi]:

                            if int(str(data[5]).split(' ')[1].split(':')[1]) < 30:
                                row = int(str(data[5]).split(' ')[1].split(':')[0]) * 2
                            else:
                                row = int(str(data[5]).split(' ')[1].split(':')[0]) * 2 + 1

                            # tủ
                            newitem = QTableWidgetItem(data[1])
                            newitem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            # newitem.setBackground(QColor(255,255,0))
                            self.table.setItem(row, count * 4 + 1, newitem)
                            # Giá trị
                            newitem = QTableWidgetItem(data[4])
                            newitem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            # newitem.setBackground(QColor(255,255,0))
                            self.table.setItem(row, count * 4 + 2, newitem)
                            # date
                            newitem = QTableWidgetItem(str(data[5]))
                            newitem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            # newitem.setBackground(QColor(255,255,0))
                            self.table.setItem(row, count * 4 + 3, newitem)

                        count += 1

    def run_new_thread(self, function):
        self.spinner = WaitingSpinner(self, True, True, Qt.ApplicationModal, roundness=457, fade=48.3, radius=20,
                                      lines=8, line_length=23.8, line_width=19.1, speed=1.5707963267948966,
                                      color=QColor(141, 141, 141))
        self.spinner.start()

        runnable = RequestRunnable(self, function)
        QThreadPool.globalInstance().start(runnable)

    @pyqtSlot(str)
    def responseRunnable(self, data):
        # print("Debug: ", data)
        nowtime = datetime.datetime.now()
        index = self.table.model().index(int(nowtime.strftime("%H")) * 2 + 5, 1)
        self.table.scrollTo(index)
        self.spinner.stop()


class RequestRunnable(QRunnable):
    def __init__(self, win, function):
        QRunnable.__init__(self)
        self.w = win
        self.fun = function

    def run(self):
        rs = False
        if self.fun == "Load_data":
            rs = self.w.load_data()

        QMetaObject.invokeMethod(self.w, "responseRunnable",
                                 Qt.QueuedConnection,
                                 Q_ARG(str, str(self.fun) + '||' + str(rs)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = monitor()

    window.show()
    app.exec_()
