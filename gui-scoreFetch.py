import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from scoreFetch import *

'''
    带有gui的成绩查询程序,可以修改下方账号密码方便登录
'''

UserId = "2018030402055"  # 账号
PassWd = ""  # 密码

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initWindow()
        self.initUI()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initWindow(self):
        self.resize(300, 250)
        self.center()
        self.setWindowTitle('成绩查询')

    def initUI(self):
        self.vbox = QVBoxLayout()
        # grid.addWidget()
        self.init_input_box(self.vbox)
        self.init_button(self.vbox)
        self.setLayout(self.vbox)

    def init_input_box(self, grid):
        self.user_hbox = QHBoxLayout()
        self.user_label = QLabel('账号：')
        self.user_label.setFont(QFont('SansSerif', 15))
        self.user_label.resize(self.user_label.sizeHint())
        self.user_input = QLineEdit()
        self.user_input.resize(50, 60)
        self.user_input.setText(UserId)
        self.user_hbox.addWidget(self.user_label)
        self.user_hbox.addWidget(self.user_input)
        grid.addLayout(self.user_hbox)
        self.passwd_hbox = QHBoxLayout()
        self.passwd_label = QLabel('密码：')
        self.passwd_label.setFont(QFont('SansSerif', 15))
        self.passwd_label.resize(self.passwd_label.sizeHint())
        self.passwd_input = QLineEdit()
        self.passwd_input.setEchoMode(2)
        self.passwd_input.setText(PassWd)
        self.passwd_hbox.addWidget(self.passwd_label)
        self.passwd_hbox.addWidget(self.passwd_input)
        grid.addLayout(self.passwd_hbox)

    def init_button(self, grid):
        # grid.addStretch(1)
        self.hbox = QHBoxLayout()
        self.login_button = QPushButton("登录")
        self.login_button.setFont(QFont('SansSerif', 10))
        self.login_button.clicked.connect(lambda: self.login_check())
        # self.login_button.setShortcut(QtCore.Qt.Key_Enter)
        self.hbox.addWidget(self.login_button)

        self.q_button = QPushButton("退出")
        self.q_button.setFont(QFont('SansSerif', 10))
        self.q_button.clicked.connect(lambda: QCoreApplication.instance().quit())
        self.hbox.addWidget(self.q_button)

        grid.addLayout(self.hbox)

    def login_check(self):
        user_id = self.user_input.text()
        passwd = self.passwd_input.text()
        if len(user_id) == 0 or len(passwd) == 0:
            QMessageBox.about(self, "警告", "请输入账号或密码")
            return
        # print(user_id)
        # print(passwd)
        spider = Spider()
        r_session = spider.login(user_id, passwd)
        login_status, page = spider.get_page(r_session)

        if not login_status:
            QMessageBox.about(self, "警告", "请输入正确的账号或密码")
            return

        lists = spider.parse_page(page)
        # print(lists)
        self.init_score_form(lists)

    def del_layout(self, grid):
        self.hbox.removeWidget(self.login_button)
        self.hbox.removeWidget(self.q_button)
        self.user_hbox.removeWidget(self.user_label)
        self.user_hbox.removeWidget(self.user_input)
        self.passwd_hbox.removeWidget(self.passwd_label)
        self.passwd_hbox.removeWidget(self.passwd_input)

    def init_score_form(self, lists):
        self.resize(1400, 800)
        self.center()
        self.del_layout(self.vbox)
        clen = len(lists)
        rlen = len(lists[0])
        table = QTableWidget(clen, rlen)
        # table.verticalHeader().hide()
        table.setHorizontalHeaderLabels(['序号', '开课学期', '课程编号', '课程名称', '总成绩',
                                         '学分', '平时成绩', '期中成绩', '实验成绩', '期末成绩',
                                         '课程属性', '课程性质', '备注', '考试性质'])
        table.horizontalHeader().setSectionResizeMode(1)
        table.verticalHeader().setSectionResizeMode(1)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # table.setSortingEnabled(True)

        for i in range(clen):
            for j in range(rlen):
                item = QTableWidgetItem(str(lists[i][j]))
                item.setFont(QFont('SansSerif', 10))
                # print(str(lists[i][j]))
                # item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                table.setItem(i, j, item)

        self.vbox.addWidget(table)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif str(e.key()) == '16777220':
            self.login_check()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
