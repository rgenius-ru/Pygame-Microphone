# pyuic5 -o form.py ui/form.ui

import sys

from Modules.base_station import BaseStation

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QTableWidgetItem

from Modules.ui.form import Ui_main_form
from Modules.ui.reg_dialog import Ui_Dialog


class Form(QMainWindow, Ui_main_form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals_slots()

    def closeEvent(self, *event) -> None:
        base_station.stop()

    def _connect_signals_slots(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_Reg.triggered.connect(self.reg)
        self.action_Fon.triggered.connect(self.fon)
        self.action_Music.triggered.connect(self.music)
        self.action_One_Player.triggered.connect(self.one_player)
        self.action_Command_Game.triggered.connect(self.command_game)

    def reg(self):
        dialog = RegDialog(self)
        response = dialog.exec()
        if response == QDialog.Accepted:
            print("RegDialog: Accepted")

            name1 = dialog.team_1_name_lineEdit.text()
            table1 = dialog.team_1_tableWidget
            app.update_team(app.team_1, name1, table1)

            name2 = dialog.team_2_name_lineEdit.text()
            table2 = dialog.team_2_tableWidget
            app.update_team(app.team_2, name2, table2)

            self.command_1_label.setText(name1)
            self.command_2_label.setText(name2)
        elif response == QDialog.Rejected:
            print("RegDialog: Cancel")

    def music(self):
        pass

    def one_player(self):
        pass

    def command_game(self):
        pass

    def fon(self):
        pass


class RegDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals_slots()

        self.team_1_name_lineEdit.setText(app.team_1.name)
        self.team_2_name_lineEdit.setText(app.team_2.name)

        self.create_table(self.team_1_tableWidget, app.team_1)
        self.create_table(self.team_2_tableWidget, app.team_2)
        # ui = loadUi("ui/reg.ui", self)
        # print(ui)

    def create_table(self, table_widget, team):
        # table_widget.setRowCount(1)
        table_widget.setColumnCount(2)
        table_header = "Ник", "Баллы"
        table_widget.setHorizontalHeaderLabels(table_header)

        if not team.members:
            team.members = {1: ['', '']}

        for row, member in team.members.items():
            if member and isinstance(row, int):
                table_widget.setRowCount(table_widget.rowCount() + 1)
                name, scores = member
                table_widget.setItem(row - 1, 0, QTableWidgetItem(name))
                table_widget.setItem(row - 1, 1, QTableWidgetItem(scores))

        table_widget.horizontalHeader().setStretchLastSection(True)
        # table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget.setColumnWidth(0, 150)
        table_widget.item(0, 1).setFlags(table_widget.item(0, 1).flags() & ~Qt.ItemIsEditable)

    def _connect_signals_slots(self):
        self.action_team_1_add_member.triggered.connect(self.team_1_add_member)
        self.action_team_2_add_member.triggered.connect(self.team_2_add_member)
        self.action_team_1_del_member.triggered.connect(self.team_1_del_member)
        self.action_team_2_del_member.triggered.connect(self.team_2_del_member)

    def team_1_add_member(self):
        self.team_add_member(self.team_1_tableWidget)

    def team_2_add_member(self):
        self.team_add_member(self.team_2_tableWidget)

    def team_add_member(self, table_widget):
        table_widget.setRowCount(table_widget.rowCount() + 1)
        table_widget.setItem(table_widget.rowCount() - 1, 0, QTableWidgetItem(''))
        table_widget.setItem(table_widget.rowCount() - 1, 1, QTableWidgetItem(''))

    def team_1_del_member(self):
        self.team_del_member(self.team_1_tableWidget)

    def team_2_del_member(self):
        self.team_del_member(self.team_2_tableWidget)

    def team_del_member(self, table_widget):
        for item in table_widget.selectedItems():
            if table_widget.rowCount() > 1:
                table_widget.removeRow(item.row())


class Team:
    def __init__(self, name=''):
        self.name = name
        self.members = None


class Application:
    def __init__(self):
        # self.team_1 = Team('Команда 1')
        # self.team_2 = Team('Команда 2')

        self.team_1 = Team('Мстители')
        self.team_1.members = {1: ['Ванёк', ''], 2: ['Санёк', '']}

        self.team_2 = Team('Разрушители')
        self.team_2.members = {1: ['Кира', ''], 2: ['Белла', ''], 3: ['Мила', '']}

        self._app = QApplication(sys.argv)
        self.form = Form()
        self.volume = None

        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.setInterval(100)  # in milliseconds
        self.timer.timeout.connect(self.game_update)
        self.timer.start()

    def update_volume(self):
        volume = base_station.received_data

        if not volume:
            volume = 0
        elif len(volume) > 1:
            volume = int(volume[1:]) * 100 // 255
            if volume > 100:
                volume = 100
            elif volume < 0:
                volume = 0

        self.form.progressBar.setValue(volume)
        # print(volume)

    def update_team(self, team, name, table_widget):
        team.name = name
        team.members.clear()

        for row in range(table_widget.rowCount()):
            member = []
            for col in range(table_widget.columnCount()):
                if table_widget.item(row, col):
                    member.append(table_widget.item(row, col).text())
                else:
                    member.append('')

                team.members.update({
                    row + 1: member
                })

        print(team.name, team.members)

    def start(self):
        """Start function."""
        self.form.show()
        self.update_volume()

        sys.exit(self._app.exec())

    def game_update(self):
        # Game Loop
        self.update_volume()


def start_round():
    pass


base_station = BaseStation()
base_station.start()

print('app start')
app = Application()
app.start()
