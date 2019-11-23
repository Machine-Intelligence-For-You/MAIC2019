TILES_COLOR = ["black", "green"]
import math


class RulesGame:

    def __init__(self, board, players, panel, gameOneGoing):
        self.gameOneGoing = gameOneGoing
        self.panel = panel
        self.players = players
        self.currentPlayer = 0
        self.board = board
        self.humainConfirmation = -1
        self.xtemp = -1
        self.ytemp = -1
        self.row = board.row
        self.col = board.col
        self.canSteal = False
        self.limitPlay=0

    def is_empty_cell(self, cell):
        i, j = cell
        if self.is_place_on_board(cell) and not self.board.squares[i][j].isPiece() :
            return True
        return False

    def get_empty_cells(self):
        empty_cells = list()
        for i in range(self.row):
            for j in range(self.col):
                if not self.board.squares[i][j].isPiece():
                    empty_cells.append((i, j))
        return empty_cells

    def get_playable_pieces(self, player_number):  # Return all on board player tiles coordinates
        squares = self.board.get_board_array()
        color = TILES_COLOR[player_number]
        playable = list()
        for i in range(self.row):
            for j in range(self.col):
                if squares[i][j] is not None and squares[i][j] == color:
                    playable.append((i, j))
        return playable

    def get_possible_moves(self, cell):  # Return the theoretical possibles moves of a tile on a x y axis
        i, j = cell
        if self.board.squares[i][j].isPiece():
            return [(cell[0] + a[0], cell[1] + a[1]) for a in
                    [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if ((0 <= cell[0] + a[0] < self.row) and (0 <= cell[1] + a[1] < self.col))]
        return None

    def is_place_on_board(self, cell):  # Check if the given cell exists on board
        i, j = cell
        if i in range(0, self.row) and j in range(0, self.col):
            return True
        return False

    def get_no_empty_cell_color(self, cell):  # Returns the color of the piece on the given no-empty cell.
        i, j = cell
        if not self.is_empty_cell(cell) and self.is_place_on_board(cell):
            return self.board.squares[i][j].piece.getColor()
        return None

    def get_piece_actual_moves(self, cell, player_number):  # Returns for a player and a given piece on board of the
        # player all possibles moves including winning moves.
        moves = list()
        i, j = cell
        color = TILES_COLOR[player_number]
        if self.get_possible_moves(cell) is not None:
            for move in self.get_possible_moves(cell):
                if self.is_empty_cell(move):
                    moves.append(move)
                elif self.get_no_empty_cell_color(move) != color:
                    k, l = move
                    if i == k and j < l and self.is_empty_cell((i, j + 2)):
                        moves.append((i, j + 2))
                    elif i == k and l < j and self.is_empty_cell((i, j - 2)):
                        moves.append((i, j - 2))
                    elif j == l and i < k and self.is_empty_cell((i + 2, j)):
                        moves.append((i + 2, j))
                    elif j == l and k < i and self.is_empty_cell((i - 2, j)):
                        moves.append((i - 2, j))
            return moves
        return None

    def is_a_possible_action(self, instruction, can_steal, player_number):
        if not can_steal:
            if not len(instruction) in [2, 4]:
                return False
            for a in instruction:
                if not isinstance(a, int):
                    return False
            if len(instruction) == 2:
                if not self.is_empty_cell(instruction):
                    return False
                if self.players[player_number].player_pieces_in_hand == 0:
                    return False
            elif len(instruction) == 4:
                if (instruction[2], instruction[3]) not in self.get_piece_actual_moves((instruction[0], instruction[1]), player_number):
                    return False
        else:
            if not len(instruction) == 2:
                return False
            for a in instruction:
                if not isinstance(a, int):
                    return False
            if instruction[0] == instruction[1] == -1:
                if self.players[(player_number + 1)%2].player_pieces_in_hand > 0:
                    return True
                return False
            elif not self.get_no_empty_cell_color(instruction) == TILES_COLOR[(player_number +  1)%2]:
                return False
        return True

    def get_movable_pieces_by_player(self, player_number):  # Returns for a player all the pieces he can move
        pieces = self.get_playable_pieces(player_number)
        moves = list()
        for piece in pieces:
            if len(self.get_piece_actual_moves(piece, player_number))>0:
                moves.append(piece)
        return moves

    def get_all_possibles_moves(self, player_number):
        moves = dict()
        moves["empty_cells"] = self.get_empty_cells()
        moves["pieces"] = self.get_movable_pieces_by_player(player_number)
        return moves

    def is_stuck(self, player_number):
        return len(self.get_movable_pieces_by_player(player_number)) == 0

    def play(self, instruction):
        print("\nScore before the move : ")
        print(f"Player {0} ({self.players[0].get_name()}) : {self.players[0].captured_pieces}\nPlayer {1} ({self.players[1].get_name()}) : {self.players[1].captured_pieces}")
        board = self.board
        color = TILES_COLOR[self.board.currentPlayer]

        if len(instruction)==2:
            if(instruction[0]==instruction[1] and instruction[0]==-1 and self.players[(self.board.currentPlayer+1)%2].player_pieces_in_hand>0):                      #Ici on vole dans la reserve de l'adversaire
                print ("Steal in the adversary hand")
                self.players[(self.board.currentPlayer+1)%2].player_pieces_in_hand-=1
                self.players[self.board.currentPlayer].captured_pieces+=1
                self.board.currentPlayer=(self.board.currentPlayer+1)%2
                self.checkForEnd()
                self.panel.updateCurrentPlayer(self.board.currentPlayer)
                self.canSteal = False

            elif(self.canSteal and board.squares[instruction[0]][instruction[1]].isPiece()):
                if board.squares[instruction[0]][instruction[1]].piece.getColor()!=color:
                    board.remove_piece((instruction[0],instruction[1]))
                    print(f"Steal the piece {instruction} on the board")
                    self.players[self.board.currentPlayer].captured_pieces+=1
                    self.board.currentPlayer=(self.board.currentPlayer+1)%2
                    self.checkForEnd()
                    self.panel.updateCurrentPlayer(self.board.currentPlayer)
                    self.canSteal=False

            elif not board.squares[instruction[0]][instruction[1]].isPiece():
                if self.players[self.board.currentPlayer].player_pieces_in_hand>0:
                    self.board.add_piece(instruction,self.board.currentPlayer)
                    self.players[self.board.currentPlayer].player_pieces_in_hand-=1
                    self.board.currentPlayer=(self.board.currentPlayer+1)%2
                    self.checkForEnd()
                    self.panel.updateCurrentPlayer(self.board.currentPlayer)

        elif(len(instruction)==4):
            if(board.squares[instruction[0]][instruction[1]].isPiece()):
                if(board.squares[instruction[0]][instruction[1]].getPiece().getColor()==color):
                    if((instruction[2],instruction[3]) in  self.get_piece_actual_moves((instruction[0],instruction[1]), self.board.currentPlayer)):
                        if (math.sqrt(math.pow(instruction[2]-instruction[0],2)+math.pow(instruction[3]-instruction[1],2))==1):
                            self.board.move_piece((instruction[0],instruction[1]),(instruction[2],instruction[3]),self.board.currentPlayer)
                            self.board.currentPlayer=(self.board.currentPlayer+1)%2
                            self.checkForEnd()
                            self.panel.updateCurrentPlayer(self.board.currentPlayer)
                        else:
                            board.move_piece((instruction[0],instruction[1]),(instruction[2],instruction[3]),self.board.currentPlayer)
                            if(instruction[0]==instruction[2]):
                                if instruction[1]-instruction[3] > 0:
                                    board.remove_piece((instruction[0],instruction[1]-1))
                                    self.limitPlay=0

                                else:
                                    board.remove_piece((instruction[0],instruction[1]+1))
                                    self.limitPlay=0
                                self.canSteal=True
                                self.players[self.board.currentPlayer].captured_pieces+=1
                                self.checkForEnd()
                            else:
                                if instruction[0]-instruction[2] >0:
                                    board.remove_piece((instruction[0]-1,instruction[1]))
                                    self.limitPlay=0
                                else:
                                    board.remove_piece((instruction[0]+1,instruction[1]))
                                    self.limitPlay=0
                                self.canSteal=True
                                self.players[self.board.currentPlayer].captured_pieces+=1
                                self.checkForEnd()
        else:
            print("there are some problem with your insctruction format")
        self.panel.updateScore((self.players[0].captured_pieces,self.players[1].captured_pieces),(self.players[0].player_pieces_in_hand,self.players[1].player_pieces_in_hand))
        self.limitPlay+=1
        if self.limitPlay==200:
            self.gameOneGoing=False

    def checkForEnd(self):
        print("\nScore after the move : ")
        print(f"Player {0} ({self.players[0].get_name()}) : {self.players[0].captured_pieces}\nPlayer {1} ({self.players[1].get_name()}) : {self.players[1].captured_pieces}")
        if (self.players[0].player_pieces_in_hand == 0 and self.isPlayerStuck(0)) or self.players[0].captured_pieces == 12:

            # end = QMessageBox.information(game, "End", f"Player {self.players[0].name} wins")
            self.gameOneGoing = False
        elif (self.players[1].player_pieces_in_hand == 0 and self.isPlayerStuck(1)) or self.players[1].captured_pieces == 12:
            # end = QMessageBox.information(game, "End", f"Player {self.players[1].name} wins")
            self.gameOneGoing = False

    def isPlayerStuck(self, player_number):
        if len(self.get_movable_pieces_by_player(player_number)) == 0:
            return True
        else:
            return False
