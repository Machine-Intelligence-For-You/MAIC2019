TILES_COLOR = ["black", "white"]
import math
import time


class RulesGame:
    # TBV
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

    # TBV
    def desableSteal(self):
        self.canSteal = False

    # TBV
    def choice(self, x, y):
        self.humainConfirmation = (self.humainConfirmation + 1) % 2
        if (self.humainConfirmation == 1):
            return (self.xtemp, self.xtemp)
        else:
            self.xtemp = x
            self.ytemp = y

    # Checked
    def is_empty_cell(self, cell):
        i, j = cell
        if self.is_place_on_board(cell) and not self.board.squares[i][j].isPiece() :
            return True
        return False

    # Checked
    def get_empty_cells(self):
        empty_cells = list()
        for i in range(self.row):
            for j in range(self.col):
                if not self.board.squares[i][j].isPiece():
                    empty_cells.append((i, j))
        return empty_cells

    # # Not used seems
    # def get_player_pieces_on_board(self, player_number):
    #     squares = self.board.squares
    #     color = TILES_COLOR[player_number]
    #     pieces = list()
    #     for i in range(self.row):
    #         for j in range(self.col):
    #             if squares[i][j].piece.getColor() == color:
    #                 pieces.append((i, j))
    #     return pieces

    # Checked
    def get_playable_pieces(self, player_number):  # Return all on board player tiles coordinates
        squares = self.board.get_board_array()
        color = TILES_COLOR[player_number]
        playable = list()
        for i in range(self.row):
            for j in range(self.col):
                if squares[i][j] is not None and squares[i][j] == color:
                    playable.append((i, j))
        return playable

    # # Not used seems
    # def get_all_empty_cells(self):  # Return all empty tiles
    #     squares = self.board.squares
    #     empty_tiles = list()
    #     for i in range(self.row):
    #         for j in range(self.col):
    #             if not squares[i][j].isPiece():
    #                 empty_tiles.append((i, j))
    #     return empty_tiles

    # Checked
    def get_possible_moves(self, cell):  # Return the theoretical possibles moves of a tile on a x y axis
        i, j = cell
        if self.board.squares[i][j].isPiece():
            return [(cell[0] + a[0], cell[1] + a[1]) for a in
                    [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if ((0 <= cell[0] + a[0] < self.row) and (0 <= cell[1] + a[1] < self.col))]
        return None

    # Checked
    def is_place_on_board(self, cell):  # Check if the given cell exists on board
        i, j = cell
        if i in range(0, self.row) and j in range(0, self.col):
            return True
        return False

    # Checked
    def get_no_empty_cell_color(self, cell):  # Returns the color of the piece on the given no-empty cell.
        i, j = cell
        if not self.is_empty_cell(cell) and self.is_place_on_board(cell):
            return self.board.squares[i][j].piece.getColor()
        return None

    # Checked
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
            elif len(instruction) == 4:
                print("zopa")
                print((instruction[2], instruction[3]) in self.get_piece_actual_moves((instruction[0], instruction[1]), player_number))
                if (instruction[2], instruction[3]) not in self.get_piece_actual_moves((instruction[0], instruction[1]), player_number):
                    return False
        else:
            print("niveau de vol", instruction, len(instruction))
            if not len(instruction) == 2:
                print("que ?")
                return False
            for a in instruction:
                print("la ?")
                if not isinstance(a, int):
                    print("hein?")
                    return False
            print("niveau 2")
            print(self.get_no_empty_cell_color(instruction), TILES_COLOR[(player_number +  1)%2])
            print(not self.get_no_empty_cell_color(instruction) == TILES_COLOR[(player_number +  1)%2])
            print(instruction[0] == instruction[1] == -1)
            if not self.get_no_empty_cell_color(instruction) == TILES_COLOR[(player_number +  1)%2]:
                return False
            elif instruction[0] == instruction[1] == -1:
                return True
        print("lvl 3")
        return True




    # # On the way to be removed
    # def get_piece_possible_moves(self, player_number,
    #                              cell):  # Return possible move of tile, knowing the player and coord of tile
    #     (r, c) = (cell[0], cell[1])
    #     patterns = [1, -1]
    #     squares = self.board.squares
    #     possible_moves = list()
    #     color = TILES_COLOR[player_number]
    #     # print ("tcho 5")
    #     for pattern in patterns:
    #         # print ("tcho 5p")
    #         if self.is_place_on_board((r + pattern, c)):
    #             # print ("tcho 6")
    #             if squares[r + pattern][c].isPiece() == False:
    #                 # print ("tcho 7")
    #                 possible_moves.append(((r + pattern, c)))
    #
    #         if self.is_place_on_board((r + (2 * pattern), c)) and squares[r + pattern][c].isPiece():
    #             # print ("tcho 8p")
    #             if (squares[r + pattern][c].isPiece() and squares[r + pattern][c].piece.getColor() != color and
    #                     squares[r + (2 * pattern)][c].isPiece() == False):
    #                 possible_moves.append((r + (2 * pattern), c))
    #                 # print ("tcho 9")
    #         if self.is_place_on_board((r, c + pattern)):
    #             # print ("tcho 10")
    #             if squares[r][c + pattern].isPiece() == False:
    #                 # print ("tcho 11")
    #                 possible_moves.append(((r, c + pattern)))
    #         if self.is_place_on_board((r, c + (2 * pattern))):
    #             if squares[r][c + pattern].isPiece():
    #                 # print ("tcho 12")
    #                 if (squares[r][c + pattern].isPiece() and squares[r][c + pattern].piece.getColor() != color and
    #                         squares[r][c + (2 * pattern)].isPiece() == False):
    #                     possible_moves.append((r, c + (2 * pattern)))
    #         # print ("tcho 13")
    #     return possible_moves

    # Checked
    def get_movable_pieces_by_player(self, player_number):  # Returns for a player all the pieces he can move
        pieces = self.get_playable_pieces(player_number)
        print("reseau")
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

    # On the way to be removed
    # def tileCanMove(self, player_number, cell):
    #     (r, c) = (cell[0], cell[1])
    #     color = TILES_COLOR[player_number]
    #     squares = self.board.squares
    #     if squares[r][c].piece.getColor() == color and len(
    #             self.get_piece_possible_moves(player_number, cell[0, cell[1]])) > 0:
    #         return True
    #     return False

    def is_stuck(self, player_number):
        return len(self.get_movable_pieces_by_player(player_number)) == 0

    def play(self,instruction):

        print ("-------------Gain----------------")
        print(self.players[0].captured_pieces)
        print(self.players[1].captured_pieces)
        print("--------------Fin Gain------------")
        board=self.board
        color=TILES_COLOR[self.board.currentPlayer]
        print ("tcho 1", instruction)

        if (len(instruction)==2):
            print("ok")


            if(instruction[0]==instruction[1] and instruction[0]==-1 and self.players[(self.board.currentPlayer+1)%2].player_pieces_in_hand>0):                      #Ici on vole dans la reserve de l'adversaire
                print ("Vole dans la reserve")
                self.players[(self.board.currentPlayer+1)%2].player_pieces_in_hand-=1
                self.players[self.board.currentPlayer].captured_pieces+=1

            elif(self.canSteal and board.squares[instruction[0]][instruction[1]].isPiece()):
                # print ("zomm")
                if board.squares[instruction[0]][instruction[1]].piece.getColor()!=color:
                    board.remove_piece((instruction[0],instruction[1]))
                    self.players[self.board.currentPlayer].captured_pieces+=1
                    self.board.currentPlayer=(self.board.currentPlayer+1)%2
                    self.checkForEnd()
                    self.panel.updateCurrentPlayer(self.board.currentPlayer)
                    self.canSteal=False

            elif not board.squares[instruction[0]][instruction[1]].isPiece():
                print ("kokoni")
                if self.players[self.board.currentPlayer].player_pieces_in_hand>0:

                    self.board.add_piece(instruction,self.board.currentPlayer)
                    # print (self.board.currentPlayer)
                    self.players[self.board.currentPlayer].player_pieces_in_hand-=1
                    # print ("Hello World",instruction)
                    self.board.currentPlayer=(self.board.currentPlayer+1)%2
                    print("lolololo")
                    self.checkForEnd()
                    print("hohohohoh")
                    self.panel.updateCurrentPlayer(self.board.currentPlayer)
                    print("Heeeeeeeeeeeeeeeeelpppppppppppp")

        elif(len(instruction)==4):
            # print ("tcho 2")
            # print (board.squares[instruction[0]][instruction[1]].isPiece())
            if(board.squares[instruction[0]][instruction[1]].isPiece()):
                print ("tcho 3")
                if(board.squares[instruction[0]][instruction[1]].getPiece().getColor()==color):
                    # print ("tcho 4")
                    if((instruction[2],instruction[3]) in  self.get_piece_actual_moves((instruction[0],instruction[1]), self.board.currentPlayer)):
                        # print("en fin")
                        if (math.sqrt(math.pow(instruction[2]-instruction[0],2)+math.pow(instruction[3]-instruction[1],2))==1):
                            # print ("tcho 8")
                            self.board.move_piece((instruction[0],instruction[1]),(instruction[2],instruction[3]),self.board.currentPlayer)
                            # self.canSteal=True
                            self.board.currentPlayer=(self.board.currentPlayer+1)%2
                            self.checkForEnd()
                            self.panel.updateCurrentPlayer(self.board.currentPlayer)
                            # print ("tcho 8 fin?")
                        else:
                            # print ("tcho 8 altern")
                            board.move_piece((instruction[0],instruction[1]),(instruction[2],instruction[3]),self.board.currentPlayer)
                            # self.board.currentPlayer=(self.board.currentPlayer+1)%2
                            # print ("allons 1")
                            if(instruction[0]==instruction[2]):
                                # print ("bouyashaka 1")
                                if instruction[1]-instruction[3] > 0:
                                    print ("bouyashaka 2",instruction,instruction[0],instruction[1]-1)
                                    board.remove_piece((instruction[0],instruction[1]-1))
                                    self.limitPlay=0

                                else:
                                    print ("bouyashaka 3")
                                    board.remove_piece((instruction[0],instruction[1]+1))
                                    self.limitPlay=0
                                self.canSteal=True
                                self.players[self.board.currentPlayer].captured_pieces+=1
                                self.checkForEnd()

                                # game.panel.updateCurrentPlayer(self.board.currentPlayer)
                            else:
                                print ("bouyashaka 4")
                                print(instruction, "b4")
                                if instruction[0]-instruction[2] >0:
                                    # print (instruction,(instruction[0]-1,instruction[1]))
                                    board.remove_piece((instruction[0]-1,instruction[1]))
                                    self.limitPlay=0

                                else:
                                    print ("bouyashaka 5")
                                    # print (instruction,(instruction[0]+1,instruction[1]))
                                    board.remove_piece((instruction[0]+1,instruction[1]))
                                    self.limitPlay=0
                                self.canSteal=True
                                self.players[self.board.currentPlayer].captured_pieces+=1
                                self.checkForEnd()
                                print("lalalala")
                                # game.panel.updateCurrentPlayer(self.currentPlayer)





        else:
            print("there are some problem with your insctruction format")
        # print ("suuuu")
        self.panel.updateScore((self.players[0].captured_pieces,self.players[1].captured_pieces),(self.players[0].player_pieces_in_hand,self.players[1].player_pieces_in_hand))
        # return self.board.currentPlayer
        self.limitPlay+=1
        if self.limitPlay==200:
            self.gameOneGoing=False

    def checkForEnd(self):
        print("checking debut")
        print(self.players[0].captured_pieces, self.players[1].captured_pieces)
        if (self.players[0].player_pieces_in_hand == 0 and self.isPlayerStuck(0)) or self.players[0].captured_pieces == 12:

            # end = QMessageBox.information(game, "End", f"Player {self.players[0].name} wins")
            self.gameOneGoing = False
        elif (self.players[1].player_pieces_in_hand == 0 and self.isPlayerStuck(1)) or self.players[1].captured_pieces == 12:
            # end = QMessageBox.information(game, "End", f"Player {self.players[1].name} wins")
            self.gameOneGoing = False
        print("fin checkin end")

    def isPlayerStuck(self, player_number):
        print ("c'est comment ?")
        print(self.get_movable_pieces_by_player(player_number))
        if len(self.get_movable_pieces_by_player(player_number)) == 0:
            return True
        else:
            return False
