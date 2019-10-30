# Created by HaroldKS at 30/10/2019 : 10:38
TILES_COLOR = ["black", "white"]
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from panel import Panel
from board import Board
from util import Trace, TimeoutError
from rulesgame import RulesGame
import argparse
import time


class GameWindow(QMainWindow):

    depth_to_cover = 9

    def __init__(self, row, col, players, timeout=.50, sleep_time = .500,parent = None):
        super(GameWindow, self).__init__(parent)
        self.setWindowTitle("[*] MAIC 2019 - Yote Game")
        self.saved = True
        self.statusBar()
        self.gameOneGoing = False
        self.setWindowIcon(QtGui.QIcon("pieces/icon.png"))
        layout = QHBoxLayout()
        layout.addStretch()
        self.row=row
        self.col=col
        self.players=players
        self.board = Board(row, col)
        self.board_size = (row, col)
        layout.addWidget(self.board)
        layout.addSpacing(15)
        self.panel = Panel(self.board, [players[0].name,players[1].name])
        layout.addWidget(self.panel)
        layout.addStretch()
        content = QWidget()
        content.setLayout(layout)
        self.rulesgame = RulesGame(self.board,self.players,self.panel,self.gameOneGoing)
        self.setCentralWidget(content)
        self.createMenu()
        self.timeout = timeout
        self.sleep_time = sleep_time
        self.trace = Trace(self.board.get_board_array())

        self.random_player = AI(self.board.currentPlayer, self.board_size)



    @QtCore.pyqtSlot(int, QGraphicsObject)
    def coord(self):
        print("fff")
        # print(GameWindow.message)


    def createMenu(self):
        menu = self.menuBar()
        #Game Menu
        gameMenu = menu.addMenu("Game")

        #New Game Submenu
        newGameAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/New file.png")), 'New Game', self)
        newGameAction.setShortcut(QtGui.QKeySequence.New)
        newGameAction.setStatusTip("New game Luncher")

        newGameAction.triggered.connect(self.newGame)

        gameMenu.addAction(newGameAction)

        gameMenu.addSeparator()

        #Load Game Submenu
        loadGameAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Open file.png")), 'Load Game', self)
        loadGameAction.setShortcut(QtGui.QKeySequence.Open)
        loadGameAction.setStatusTip("Load a previous game")
        loadGameAction.triggered.connect(self.loadGame)
        gameMenu.addAction(loadGameAction)

        #Save Game
        saveGameAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Save.png")), 'Save Game', self)
        saveGameAction.setShortcut(QtGui.QKeySequence.Save)
        saveGameAction.setStatusTip("Save current game")
        saveGameAction.triggered.connect(self.saveGame)
        gameMenu.addAction(saveGameAction)

        gameMenu.addSeparator()

        #Exit and close game
        exitGameAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Close.png")), 'Exit Game', self)
        exitGameAction.setShortcut(QtGui.QKeySequence.Quit)
        exitGameAction.setMenuRole(QAction.QuitRole)
        exitGameAction.setStatusTip("Exit and close window")
        exitGameAction.triggered.connect(self.exitGame)
        gameMenu.addAction(exitGameAction)

        menu.addSeparator()

        #Help Menu
        helpMenu = menu.addMenu("Help")

        #Rules
        gameRulesAction = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Help.png")), 'Rules', self)
        gameRulesAction.setMenuRole(QAction.AboutRole)
        gameRulesAction.triggered.connect(self.gameRules)
        helpMenu.addAction(gameRulesAction)

        helpMenu.addSeparator()

        #About
        aboutAction = QAction( 'About', self)
        aboutAction.setMenuRole(QAction.AboutRole)
        aboutAction.triggered.connect(self.about)
        helpMenu.addAction(aboutAction)

    def newGame(self):
        newGame = QMessageBox.question(self, 'New Game', "You're about to start a new Game.", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if newGame == QMessageBox.Yes:
            self.resetForNewGame()
            self.startBattle()
        else:
            pass

    def resetForNewGame(self):
        self.board.resetBoard()
        self.board.score = [0, 0]
        self.gameOneGoing = True
        self.rulesgame.gameOneGoing = True

        self.board.activeAllSquares()
        self.board.setCurrentPlayer(0)
        self.panel.resetPanelPlayer()
        self.board.currentPlayer = 0

        self.rulesgame.canSteal=False

        for player in self.players:
            player.reset_player_data()


    def startBattle(self):
        hit = 0

        while self.rulesgame.gameOneGoing:
            app.processEvents()
            hit += 1
            time.sleep(self.sleep_time)
            way_of_move = "exactly"
            try:
                instruction = self.players[self.board.currentPlayer].play(self.depth_to_cover, self.board.get_board_array(), self.rulesgame.canSteal)
            except TimeoutError:
                way_of_move = "randomly"
                print(f"Player {self.players[self.board.currentPlayer]} ({self.players[self.board.currentPlayer].get_name()}) exhauted his time credit for this turn. A random choice will be made.")
                self.random_player.set_states([self.players[self.board.currentPlayer].player_pieces,self.players[self.board.currentPlayer].player_pieces_in_hand, self.players[self.board.currentPlayer].captured_pieces,self.board.currentPlayer])
                instruction = self.random_player.play(self.depth_to_cover, self.board.get_board_array(), self.rulesgame.canSteal)



            if self.rulesgame.canSteal:
                print("Stealing phase : ")


            if not self.rulesgame.is_a_possible_action(instruction, self.rulesgame.canSteal, self.board.currentPlayer):
                print(f"Illegal move were returned by {self.players[self.board.currentPlayer].get_name()}. A random choice will be made")
                self.random_player.set_states([self.players[self.board.currentPlayer].player_pieces,self.players[self.board.currentPlayer].player_pieces_in_hand, self.players[self.board.currentPlayer].captured_pieces,self.board.currentPlayer])
                instruction = self.random_player.play(self.depth_to_cover, self.board.get_board_array(), self.rulesgame.canSteal)

            print(f'{self.players[self.board.currentPlayer].get_name()} (Player {self.board.currentPlayer}) {way_of_move} plays {instruction}')
            print(f"It's the {hit}th hit played by Player {self.board.currentPlayer} ({self.players[self.board.currentPlayer].get_name()})")
            if not self.rulesgame.canSteal:
                if len(instruction) == 2:
                    i, j = instruction
                    self.board.squares[i][j].setBackgroundColor("blue")
                    app.processEvents()
                    self.rulesgame.play(instruction)
                if len(instruction) == 4:
                    i, j, k, l = instruction
                    self.board.squares[i][j].setBackgroundColor("blue")
                    self.board.squares[k][l].setBackgroundColor("green")
                    time.sleep(self.sleep_time)
                    app.processEvents()
                    self.rulesgame.play(instruction)
                    app.processEvents()
            else:
                if not instruction[0] == instruction[1] == -1:
                    app.processEvents()
                    i, j = instruction
                    self.board.squares[i][j].setBackgroundColor("red")
                    time.sleep(self.sleep_time)
                    app.processEvents()
                self.rulesgame.play(instruction)
            self.board.setDefaultColors()


            self.trace.add_action(self.board.currentPlayer, instruction, self.rulesgame.canSteal, self.board.get_board_array(), self.board.score,(self.players[0].player_pieces_in_hand,self.players[1].player_pieces_in_hand))
            self.WhoWins()



        self.saveGame()
        print("\nIt's over.")

    def WhoWins(self):

        if self.rulesgame.gameOneGoing:
            if (self.players[0].player_pieces_in_hand==0 and self.rulesgame.isPlayerStuck(1)) or self.players[0].captured_pieces==12:
                print(f"\nPlayer 0 ({self.players[0].get_name()}) wins")
                end = QMessageBox.information(self, "End", f" {self.players[0].name} wins")

                # self.gameOneGoing = False
            elif (self.players[1].player_pieces_in_hand==0 and self.rulesgame.isPlayerStuck(0)) or self.players[1].captured_pieces==12:
                print(f"\nPlayer 1 ({self.players[1].get_name()}) wins")
                end = QMessageBox.information(self, "End", f" {self.players[1].name} wins")
                # self.gameOneGoing = False
            print ("\nNo winner")
        else:
            if (self.players[0].captured_pieces>self.players[1].captured_pieces):
                print(f"\nPlayer 0 ({self.players[0].get_name()}) wins")
                end = QMessageBox.information(self, "End", f" {self.players[0].name} wins")
            elif (self.players[0].captured_pieces<self.players[1].captured_pieces):
                print(f"\nPlayer 1 ({self.players[1].get_name()}) wins")
                end = QMessageBox.information(self, "End", f" {self.players[1].name} wins")
            else:
                print("Equality")
                end = QMessageBox.information(self,"End", "No winner")




    def loadStartBattle(self,actions, delay = 0.5):
        hit = 0
        for action in actions:
            instruction=action[1]
            app.processEvents()
            hit += 1
            time.sleep(delay)
            print(f"\nIt's the {hit}th hit played by Player {self.board.currentPlayer} ({self.players[self.board.currentPlayer].get_name()})")

            self.rulesgame.play(instruction)
            self.WhoWins()
        print("It's over.")



    def loadGame(self):
        name =QtWidgets.QFileDialog.getOpenFileName(self, 'Load Game')
        listBoard = None
        listBoard = self.trace.load_trace(name[0])
        self.resetForNewGame()
        actions = listBoard.get_actions()
        delay, ok = QInputDialog.getDouble(self,'Enter the delay','')
        if ok:
            self.loadStartBattle(actions, delay)



    def saveGame(self):
        if self.gameOneGoing:
            name =QtWidgets.QFileDialog.getSaveFileName(self, 'Save Game')
            self.trace.write(name[0])
        else:
            warning = QMessageBox.warning(self, "Warning", "No game ongoing")

    def exitGame(self):
        return True

    def gameRules(self):
        rules = "Yoté Rules \n " \
                "The game is played on a 5×6 board, which is empty at the beginning of the game. Each player has twelve pieces in hand. Players alternate turns, with White moving first. In a move, a player may either: \n" \
                "-Place a piece in hand on any empty cell of the board. \n" \
                "-Move one of their pieces already on the board orthogonally to an empty adjacent cell. \n" \
                "-Capture an opponent's piece if it is orthogonally adjacent to a player's piece, by jumping to the empty cell immediately beyond it. The captured piece is removed from the board, and the capturing player removes another of the opponent's pieces of his choosing from the board. \n" \
                "The player who captures all the opponent's pieces is the winner. The game can end in a draw if both players are left with three or fewer pieces. \n" \
                "For more informations : https://en.wikipedia.org/wiki/Yot%C3%A9";
        box = QMessageBox()
        box.about(self, "Rules", rules)

    def about(self):
        about = "MAIC 2019 Yote Game by MIFY"
        box = QMessageBox()
        box.about(self, "About", about)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.exitGame() == True:
            a0.accept()
        else:
            a0.ignore()
    def replayGame(self):
        import time
        self.resetForNewGame()
        name =QtWidgets.QFileDialog.getOpenFileName(self, 'Load Game')
        listBoard = None
        i = -1
        if name[0] != "":
            listBoard = self.trace.load_trace(name[0])
            if listBoard.winner == -1:
                warning = QMessageBox.warning(self, "Game Not ended", "This game is not yet finished. Load it to finish it")
            else:
                self.board.resetBoard()
                actions = listBoard.get_actions()

                for action in actions:
                    i+=1
                    app.processEvents()
                    if action[2] == 0:

                        self.board.currentPlayer = action[0]

                        self.board.putListBoard(action[3])
                        time.sleep(self.sleep_time)
                    elif action[2] == 1:
                        # self.panel.updateScore(action[4])
                        self.board.score = action[4]
                        self.board.currentPlayer = action[0]

                        self.board.putListBoard(actions[i-1][3])
                        origin=(action[1][0],action[1][1])
                        end=(-1,-1)
                        if(len(action[1])==4):
                            end = (action[1][2],action[1][3])
                        self.board.squares[origin[0]][origin[1]].setBackgroundColor("blue")
                        time.sleep(self.sleep_time)
                        self.board.squares[end[0]][end[1]].setBackgroundColor("green")
                        self.rulesgame.play((action[1][0],action[1][1],action[1][2],action[1][3]))
                        time.sleep(self.sleep_time)
                        self.board.putListBoard(action[3])
                        time.sleep(sleep_time)
                        self.board.setDefaultColors()



from randomplay import AI
if __name__ == "__main__":
    import sys
    import ctypes
    myappid = 'myfi.maic.yote.1.0'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='total number of seconds credited to each player')
    parser.add_argument('-ai0', help='path to the ai that will play as player 0')
    parser.add_argument('-ai1', help='path to the ai that will play as player 1')
    parser.add_argument('-s', help='time to show the board')
    args = parser.parse_args()

    # set the time to play
    timeout = float(args.t) if args.t is not None else .05
    sleep_time = float(args.s) if args.s is not None else .150

    player_type = ['human', 'human']
    player_type[0] = args.ai0 if args.ai0 != None else 'human'
    player_type[1] = args.ai1 if args.ai1 != None else 'human'
    for i in range(2):
        if player_type[i].endswith('.py'):
            player_type[i] = player_type[i][:-3]
    agents = [None for _ in range(2)]

    # load the agents
    for i in range(2):
        if player_type[i] != 'human':
            j = player_type[i].rfind('/')
            # extract the dir from the agent
            dir = player_type[i][:j]
            # add the dir to the system path
            sys.path.append(dir)
            # extract the agent filename
            file = player_type[i][j+1:]
            # create the agent instance
            agents[i] = getattr(__import__(file), 'AI')(i, (5, 6))

    if None in agents:
        raise Exception('Problems in  AI players instances. \n'
                        'Usage:\n'
                        '-t time credited \n'
                        '\t total number of seconds credited to each player \n'
                        '-ai0 ai0_file.py \n'
                        '\t path to the ai that will play as player 0 \n'
                        '-ai1 ai1_file.py\n'
                        '\t path to the ai that will play as player 1 \n'
                        '-s sleep time \n'
                        '\t time(in second) to show the board(or move)')
    game = GameWindow(5, 6, agents, sleep_time=sleep_time, timeout=timeout)
    game.show()
    sys.exit(app.exec_())
