# pyuic5 -o form.py ui/form.ui

import sys

from Modules.base_station import BaseStation

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QTableWidgetItem

from Modules.ui.form import Ui_main_form
from Modules.ui import reg_dialog, results, rang


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

        if not game_round.is_started:
            game_round.is_started = True
            game_round.current_team = app.team_1
            app.team_1.clear_score()
            app.team_2.clear_score()
            self.create_table(self.cmd_1_tableWidget, app.team_1)
            self.create_table(self.cmd_2_tableWidget, app.team_2)
            self.score_label.setText('0')

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

        if not game_round.is_started:
            game_round.is_started = True
            game_round.current_team = app.team_1
            app.team_1.clear_score()
            app.team_2.clear_score()
            self.create_table(self.cmd_1_tableWidget, app.team_1)
            self.create_table(self.cmd_2_tableWidget, app.team_2)
            self.score_label.setText('0')
            self.cmd_1_itogi_label.clear()
            self.cmd_2_itogi_label.clear()

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

            _team_name = game_round.current_team.name
            _player_id = game_round.current_team.current_player_id
            _player_name = game_round.current_player_name

            if game_round.current_team == app.team_1:
                app.team_1.members.get(_player_id)[1] = str(game.current_score)
                self.cmd_1_tableWidget.item(_player_id - 1, 1).setText(str(game.current_score))
                _sum_scores = game_round.current_team.get_sum_scores()
                self.cmd_1_itogi_label.setText(str(_sum_scores))
            else:
                app.team_2.members.get(_player_id)[1] = str(game.current_score)
                self.cmd_2_tableWidget.item(_player_id - 1, 1).setText(str(game.current_score))
                _sum_scores = game_round.current_team.get_sum_scores()
                self.cmd_2_itogi_label.setText(str(_sum_scores))

            game_round.next_player()

            if game_round.current_step < game_round.max_steps:
                game_round.current_step += 1
                dialog = ResultsDialog(self)
                dialog.score_label.setText(str(game.current_score))
                dialog.exec()
            else:
                game_round.is_started = False
                self.run_game_Button.setEnabled(False)

            _team_name = game_round.current_team.name
            _player_id = game_round.current_team.current_player_id
            _player_name = game_round.current_player_name

            if not game_round.is_started:
                rang_table = game_round.get_rang_table()
                text = ''
                dialog = RangDialog(self)
                if game.player_mode == 'one':
                    dialog.team_2_tableWidget.setMaximumWidth(0)

                    members = game_round.current_team.members.items()
                    rating_table = sorted(members, reverse=True, key=lambda score: int(score[1][1]))
                    print('\nСортированный рейтинг')
                    print(rating_table)
                    rating_table = dict(rating_table)
                    print(rating_table)
                    team = Team()
                    team.members = rating_table
                    dialog.create_table(dialog.team_1_tableWidget, team)

                    if len(rang_table) == 1:
                        name = list(rang_table.values())[0][0]
                        text = 'Победитель ' + name + '!'
                    elif len(rang_table) == len(game_round.current_team.members):
                        text = 'Ничья!'
                    elif len(game_round.current_team.members) > len(rang_table) >= 2:
                        text = 'Победители '
                        for winner in rang_table.values():
                            text += winner[0] + ' '
                        text += ' !!!'
                elif game.player_mode == 'multi':
                    members = app.team_1.members.items()
                    rating_table = sorted(members, reverse=True, key=lambda score: int(score[1][1]))
                    print('\nСортированный рейтинг')
                    print(rating_table)
                    rating_table = dict(rating_table)
                    print(rating_table)
                    team = Team()
                    team.members = rating_table
                    dialog.create_table(dialog.team_1_tableWidget, team)

                    members = app.team_2.members.items()
                    rating_table = sorted(members, reverse=True, key=lambda score: int(score[1][1]))
                    print('\nСортированный рейтинг')
                    print(rating_table)
                    rating_table = dict(rating_table)
                    print(rating_table)
                    team = Team()
                    team.members = rating_table
                    dialog.create_table(dialog.team_2_tableWidget, team)

                    if len(rang_table) > 1:
                        text = 'Ничья!'
                    else:
                        text = 'Победила команда ' + rang_table[0].name + '!'

                print(text)
                dialog.win_name_label.setText(text)
                dialog.exec()

            if game_round.current_team == app.team_1:
                self.cmd_2_tableWidget.clearSelection()
                self.cmd_1_tableWidget.selectRow(_player_id - 1)
            else:
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


class RangDialog(QDialog, rang.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals_slots()

    def _connect_signals_slots(self):
        pass

    def create_table(self, table_widget, sorted_rating):
        table_widget.setRowCount(0)
        table_widget.clear()
        table_widget.setColumnCount(2)
        table_header = "Ник", "Баллы"
        table_widget.setHorizontalHeaderLabels(table_header)

        if not sorted_rating.members:
            sorted_rating.members = {1: ['', '']}

        for index, member in enumerate(sorted_rating.members.items()):
            if member:
                table_widget.setRowCount(table_widget.rowCount() + 1)
                name, scores = member[1]
                table_widget.setItem(index, 0, QTableWidgetItem(name))
                table_widget.setItem(index, 1, QTableWidgetItem(scores))

        table_widget.horizontalHeader().setStretchLastSection(True)
        # table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget.setColumnWidth(0, 150)
        table_widget.item(0, 1).setFlags(table_widget.item(0, 1).flags() & ~Qt.ItemIsEditable)


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
        self.members = {1: ['', '']}
        self.current_player_id = 0
        self._sum_scores = None

    def clear_score(self):
        for member in self.members.items():
            member[1][1] = ''

    def get_sum_scores(self):
        self._sum_scores = 0
        for member in self.members.items():
            if member[1][1]:
                self._sum_scores += int(member[1][1])
        return self._sum_scores


class Application:
    def __init__(self):
        # self.team_1 = Team('Команда 1')
        # self.team_2 = Team('Команда 2')

        # self.team_1 = Team('Мстители')
        # self.team_1.members = {1: ['Ванёк', ''], 2: ['Санёк', '']}
        self.team_1 = Team('')
        self.team_1.members = {1: ['', '']}

        # self.team_2 = Team('Разрушители')
        # self.team_2.members = {1: ['Кира', ''], 2: ['Белла', ''], 3: ['Мила', '']}
        self.team_2 = Team('')
        self.team_2.members = {1: ['', '']}

        self._app = QApplication(sys.argv)
        self.form = Form()
        self.form.setStyleSheet(stylesheet)
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
        self.current_player_name = None
        self.max_steps = None
        self.current_step = None
        self.winner_player_id = None
        self.winner_player_name = None
        self.winner_team = None

    def get_rang_table(self):
        table = dict()
        scores = []

        if game.player_mode == 'one':
            members = self.current_team.members
            print('\nУчастики')
            print(members)
            for member in members:
                score = members.get(member)[1]
                if score:
                    scores.append(int(score))
                else:
                    scores.append(0)

            max_score = max(scores)
            print('\nРейтинг участников')
            print(scores)
            print('\nМакс балл')
            print(max_score)
            for index, score in enumerate(scores, 1):
                if score == max_score:
                    table.update({index: members.get(index)})

            print('\nПобедители')
            print(table)

        elif game.player_mode == 'multi':
            print('\nУчастики команды 1')
            print(app.team_1.members)
            print('\nУчастики команды 2')
            print(app.team_2.members)

            print('\nИтоговый счёт команды 1')
            team1_score = app.team_1.get_sum_scores()
            print(team1_score)
            print('\nИтоговый счёт команды 2')
            team2_score = app.team_2.get_sum_scores()
            print(team2_score)

            if team1_score > team2_score:
                return [app.team_1]
            if team1_score < team2_score:
                return [app.team_2]
            if team1_score == team2_score:
                return [app.team_1, app.team_2]

        return table

    def first_player(self):
        if self.current_team:
            self.current_team.current_player_id = 1
            self.current_player_name = self.current_team.members.get(1)[0]

    def next_team(self):
        if self.current_team == app.team_1:
            self.current_team = app.team_2
        elif self.current_team == app.team_2:
            self.current_team = app.team_1

    def next_player(self):
        if game.player_mode == 'multi':
            self.next_team()

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
        self.player_mode = None   # None or 'multi' or 'one'
        self.current_player = None


stylesheet = """
    QMainWindow {
        background-image: url("Modules/ui/resources/background2.jpg"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

game = Game()
game_round = Round()

base_station = BaseStation()
base_station.start()

print('app start')
app = Application()
app.start()
