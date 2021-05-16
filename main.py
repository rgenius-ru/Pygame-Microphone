# pyuic5 -o form.py ui/form.ui

import sys

from Modules.base_station import BaseStation

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QTableWidgetItem

from Modules.ui.form import Ui_main_form
from Modules.ui import reg_dialog, results


class Form(QMainWindow, Ui_main_form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals_slots()
        self.run_game_Button.setEnabled(False)
        self.end_game_Button.setEnabled(False)
        self.commandButton.setEnabled(False)
        self.onePlayerButton.setEnabled(False)

    def closeEvent(self, *event) -> None:
        base_station.stop()

    def _connect_signals_slots(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_Reg.triggered.connect(self.reg)
        self.action_Fon.triggered.connect(self.fon)
        self.action_Music.triggered.connect(self.music)
        self.action_One_Player.triggered.connect(self.one_player)
        self.action_Command_Game.triggered.connect(self.command_game)
        self.action_Run_Game.triggered.connect(self.run_game)
        self.action_End_Game.triggered.connect(self.end_game)

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

            self.create_table(self.cmd_1_tableWidget, app.team_1)
            self.create_table(self.cmd_2_tableWidget, app.team_2)

            count_1 = len(app.team_1.members)
            count_2 = len(app.team_2.members)
            self.onePlayerButton.setEnabled(count_1 > 1)
            self.commandButton.setEnabled((count_1 > 0) and (count_2 > 0))

        elif response == QDialog.Rejected:
            print("RegDialog: Cancel")

    def create_table(self, table_widget, team):
        table_widget.setRowCount(0)
        table_widget.clear()
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

    def music(self):
        print('music')
        pass

    def one_player(self):
        print('one_player')
        game.player_mode = 'one'
        self.game_mode_label.setText('Одиночная игра')
        self.run_game_Button.setEnabled(True)

        if game_round.is_started:
            game_round.first_player()
        else:
            game_round.is_started = True
            game_round.current_team = app.team_1
            game_round.first_player()

        _max_steps = len(app.team_1.members)
        game_round.max_steps = _max_steps
        game_round.current_step = 1

        _team_name = game_round.current_team.name
        _player_id = game_round.current_team.current_player_id
        _player_name = game_round.current_player_name

        self.cmd_1_tableWidget.selectRow(_player_id - 1)

        print('Название команды:', _team_name)
        print('Имя игрока', _player_name)
        print('Id игрока:', _player_id)

        _text = 'Играет: ' + _player_name + ' из команды: ' + _team_name
        self.current_player_label.setText(_text)

    def command_game(self):
        print('command_game')
        game.player_mode = 'multi'
        self.game_mode_label.setText('Командная игра')
        self.run_game_Button.setEnabled(True)

        if game_round.is_started:
            game_round.first_player()
        else:
            game_round.is_started = True
            game_round.current_team = app.team_1
            game_round.first_player()

        _max_steps = 2 * max(len(app.team_1.members), len(app.team_2.members))
        game_round.max_steps = _max_steps
        game_round.current_step = 1

        _team_name = game_round.current_team.name
        _player_id = game_round.current_team.current_player_id
        _player_name = game_round.current_player_name

        self.cmd_1_tableWidget.selectRow(_player_id - 1)

        print('Название команды:', _team_name)
        print('Имя игрока', _player_name)
        print('Id игрока:', _player_id)

        _text = 'Играет: ' + _player_name + ' из команды: ' + _team_name
        self.current_player_label.setText(_text)

    def fon(self):
        print('fon')
        pass

    def run_game(self):
        print('run_game')
        game.current_score = 0
        self.score_label.setText(str(game.current_score))
        game.started = True
        self.end_game_Button.setEnabled(True)
        self.run_game_Button.setEnabled(False)

        _team_name = game_round.current_team.name
        _player_id = game_round.current_team.current_player_id
        _player_name = game_round.current_player_name

        print('Игра запущена:', game_round.is_started)
        print('Название команды:', _team_name)
        print('Имя игрока', _player_name)
        print('Id игрока:', _player_id)

    def end_game(self):
        if game.started:
            game.started = False
            self.run_game_Button.setEnabled(True)
            self.end_game_Button.setEnabled(False)
            print('end_game')

            if game.player_mode == 'multi':
                game_round.next_team()

            game_round.next_player()

            if game_round.current_step < game_round.max_steps:
                game_round.current_step += 1
                dialog = ResultsDialog(self)
                dialog.score_label.setText(str(game.current_score))
                dialog.exec()
            else:
                game_round.is_started = False
                self.run_game_Button.setEnabled(False)
                print('Найти победителя')

            _team_name = game_round.current_team.name
            _player_id = game_round.current_team.current_player_id
            _player_name = game_round.current_player_name

            if game_round.current_team == app.team_1:
                self.cmd_2_tableWidget.clearSelection()
                self.cmd_1_tableWidget.selectRow(_player_id - 1)
            elif game_round.current_team == app.team_2:
                self.cmd_1_tableWidget.clearSelection()
                self.cmd_2_tableWidget.selectRow(_player_id - 1)

            if not game_round.is_started:
                self.cmd_1_tableWidget.clearSelection()
                self.cmd_2_tableWidget.clearSelection()

            if not game_round.is_started:
                self.game_mode_label.setText('Ещё будете орать?')

            if game_round.is_started:
                _text = 'Играет: ' + _player_name + ' из команды: ' + _team_name
            else:
                _text = ''
            self.current_player_label.setText(_text)


class ResultsDialog(QDialog, results.Ui_dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        pass


class RegDialog(QDialog, reg_dialog.Ui_Dialog):
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
        self.current_player_id = None


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
        if game.started:
            if base_station.received_data:
                _volume = int(base_station.received_data[1:])
                if _volume > 16:
                    game.current_score += _volume
                    self.form.score_label.setText(str(game.current_score))


class Round:
    def __init__(self):
        self.is_started = False
        self.current_team = None
        self.current_player_id = None
        self.current_player_name = None
        self.max_steps = None
        self.current_step = None

    def first_player(self):
        if self.current_team:
            self.current_team.current_player_id = 1
            self.current_player_name = self.current_team.members.get(1)[0]

    def next_team(self):
        if game_round.current_team == app.team_1:
            game_round.current_team = app.team_2
        elif game_round.current_team == app.team_2:
            game_round.current_team = app.team_1

    def next_player(self):
        if self.current_team:
            if not self.current_team.current_player_id:
                self.current_team.current_player_id = 0

            if self.current_team.current_player_id < len(self.current_team.members):
                self.current_team.current_player_id += 1
            else:
                self.current_team.current_player_id = 1

            self.current_player_name = self.current_team.members.get(self.current_team.current_player_id)[0]


class Game:
    def __init__(self):
        self.current_score = 0
        self.started = False
        self.player_mode = None  # None or 'multi' or 'one'
        self.current_player = None


game = Game()
game_round = Round()

base_station = BaseStation()
base_station.start()

print('app start')
app = Application()
app.start()
