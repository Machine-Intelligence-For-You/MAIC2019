# -*- coding: utf-8 -*-
import random
from util import timeout
from player import Player
from typing import List,Dict,Union
TILES_COLOR = ["black", "green"]


class AI(Player):

    # Team modify this
    name = "HGN"

    def __init__(self, player_number, board_size):
        Player.__init__(self, player_number, board_size)

    def get_player_score(self):
        return self.captured_pieces

    def get_player_name(self):
        return self.name
    
    @timeout(0.1)
    def play(self, depth_to_cover, board, can_steal):
        if can_steal:
            ennemyPieces=[]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] is not None and TILES_COLOR[(self.player_number+1)%2].lower()==board[i][j].lower():
                        ennemyPieces.append((i,j))
            ennemyPiecesFilter = self.side_enemy_piece(board, ennemyPieces)
            if any(ennemyPiecesFilter):
                ennemyPieces = ennemyPiecesFilter
            if not ennemyPieces:
                return -1, -1
            return ennemyPieces[random.randint(0,len(ennemyPieces)-1)]

        wantTomove=0
        if self.player_pieces_in_hand>0 and len(self.get_playable_pieces(board, self.player_number)) < 11 and self.are_not_blocked(board):
            temp = self.get_all_possibles_moves(board, self.player_number)["pieces"]
            if type(self.gain_pieces(board, temp)) is list:
                wantTomove = 0
            else:
                wantTomove = 1
            if(len(self.get_all_possibles_moves(board, self.player_number)["empty_cells"])==len(board)*len(board[0])):
                wantTomove=0
            if(len(self.get_movable_pieces_by_player(board, self.player_number))==0):
                wantTomove=0
        else:
            wantTomove=1

        if wantTomove==0:
            playable=[]
            i=-1
            for line in board:
                i+=1
                j=-1
                for case in line:
                    j+=1
                    if case is None:
                        playable.append((i,j))
            playable = self.place_to_move(board,playable)
            return playable[random.randint(0, len(playable)-1)]
        else:
            temp=self.get_all_possibles_moves(board, self.player_number)["pieces"]
            #playable=temp[random.randint(0, len(temp)-1)]
            playable_int = self.gain_pieces(board, temp)
            if type(playable_int) is list:
                playable = playable_int[random.randint(0, len(playable_int) - 1)]
            else:
                playable = playable_int
            temp=self.get_piece_actual_moves(board, playable, self.player_number)
            #playableDestination=temp[random.randint(0, len(temp)-1)]
            playableDestination = self.optimal_moves(board,temp, playable)
            return (playable[0],playable[1],playableDestination[0],playableDestination[1])


    '''  Function added by HGN '''
    def can_move_now(self,board,cell):
        i,j=cell
        side = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
        side_ii = [(i, j - 2), (i, j + 2), (i - 2, j), (i + 2, j)]
        for index,position in enumerate(side):
            if self.is_place_on_board(position):
                col = self.get_no_empty_cell_color(board,position)
                if col is not None and col.lower()==TILES_COLOR[self.player_number].lower():
                    if index==0:
                        cl = side_ii[index]
                        if self.is_place_on_board(cl):
                            col_sl = self.get_no_empty_cell_color(board,cl)
                            if col_sl is not None and col.lower()==TILES_COLOR[(self.player_number+1)%2].lower():
                                return False
                    if index==1:
                        cl = side_ii[index]
                        if self.is_place_on_board(cl):
                            col_sl = self.get_no_empty_cell_color(board,cl)
                            if col_sl is not None and col.lower() == TILES_COLOR[(self.player_number + 1) % 2].lower():
                                return False
                    if index==2:
                        cl = side_ii[index]
                        if self.is_place_on_board(cl):
                            col_sl = self.get_no_empty_cell_color(board,cl)
                            if col_sl is not None and col.lower() == TILES_COLOR[(self.player_number + 1) % 2].lower():
                                return False
                    if index==3:
                        cl = side_ii[index]
                        if self.is_place_on_board(cl):
                            col_sl = self.get_no_empty_cell_color(board,cl)
                            if col_sl is not None and col.lower() == TILES_COLOR[(self.player_number + 1) % 2].lower():
                                return False
        return True


    def get_adverse_positions(self,board):
        player_number = (self.player_number+1)%2
        adverse_pieces = self.get_playable_pieces(board,player_number=player_number)
        return adverse_pieces

    def zone_mort(self,board):
        cells = [(2, 2), (3, 2)]
        adverse_pieces = self.get_adverse_positions(board)
        if len(adverse_pieces)==1 or len(adverse_pieces)==0:
            for cell in cells:
                if cell in adverse_pieces:
                    return True
        return False

    def zone_attaque(self,board):
        pieces_attaque =[]
        adverse_pieces = self.get_adverse_positions(board)
        for cell in adverse_pieces:
            if cell[0]>0 and cell[0]<4 and cell[1]>0 and cell[1]<5:
                pieces_attaque.append(cell)
        if pieces_attaque:
            return pieces_attaque
        return None

    def zone_defense(self,board):
        pieces_defense = []
        adverse_pieces = self.get_adverse_positions(board)
        for cell in adverse_pieces:
            if cell[0]==0 or cell[0]==4 or cell[1]==0 or cell[1]==5:
                pieces_defense.append(cell)
        if pieces_defense:
            return pieces_defense
        return None

    def place_to_move(self,board,playable):
        if self.zone_mort(board):
            cells = [(0,0),(4,0),(0,5),(4,5)]
            my_pieces = self.get_playable_pieces(board,self.player_number)
            if len(my_pieces)<5:
                for cell in cells:
                    if self.is_empty_cell(board,cell):
                        return [cell]
        pieces_attaque = self.zone_attaque(board)
        if pieces_attaque is not None:
            for piece in pieces_attaque:
                i,j =piece
                if piece[1]==1:
                    if not self.can_be_gain_for_empty_cell(board,(i,j-1)):
                        return [(i,j-1)]
                if piece[1]==2 or piece[1]==3:
                    if piece[0]==3:
                        if not self.can_be_gain_for_empty_cell(board, (i+1, j)):
                            return [(i+1,j)]
                    else:
                        if not self.can_be_gain_for_empty_cell(board, (i-1, j)):
                            return[(i-1,j)]
                if piece[1]==4:
                    if not self.can_be_gain_for_empty_cell(board, (i, j+1)):
                        return [(i,j+1)]

        pieces = self.zone_defense(board)
        if pieces is not None:
            for piece in pieces:
                i,j =piece
                if piece[1]==0 or piece[1]==5:
                    if piece[1]<2:
                        cl=(i+2,j)
                        if self.is_empty_cell(board,cl):
                            if not self.can_be_gain_for_empty_cell(board, cl):
                                return [cl]
                        else:
                            if self.is_empty_cell(board,(cl[0]+1,cl[1])):
                                if not self.can_be_gain_for_empty_cell(board, (cl[0]+1,cl[1])):
                                    return [(cl[0]+1,cl[1])]
                    else:
                        cl = (i - 2, j)
                        if self.is_empty_cell(board, cl):
                            if not self.can_be_gain_for_empty_cell(board, cl):
                                return [cl]
                        else:
                            if self.is_empty_cell(board, (cl[0] - 1, cl[1])):
                                if not self.can_be_gain_for_empty_cell(board, (cl[0] - 1, cl[1])):
                                    return [(cl[0] - 1, cl[1])]
        return self.optimal_place(board,playable)

    def side_enemy_piece(self, board, enemy_pieces: List[tuple]) -> List[tuple]:
        """This function takes the ennemy_pieces list and return the list of pieces which
           contains ennemy pieces arround my pieces"""
        filter_ennemy_pieces = []
        for cell in enemy_pieces:
            i, j = cell
            side = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
            '''left = (i,j-1)
            right = (i,j+1)
            up = (i-1,j)
            bottom = (i+1,j)
            '''

            for position in side:
                if self.is_place_on_board(position):
                    color = self.get_no_empty_cell_color(board, position)
                    if color is not None and color.lower() == TILES_COLOR[self.player_number].lower():
                        if self.piece_can_move(board, cell, (self.player_number + 1) % 2):
                            if self.can_gain(board, cell, player=((self.player_number + 1) % 2)):
                                if cell not in filter_ennemy_pieces:
                                    filter_ennemy_pieces.append(cell)
        return filter_ennemy_pieces

    def optimal_moves(self, board, temp, playable) -> List[int]:
        """This function works with the playableDestination list and return the cell destination
           that can gain ennemy pieces or a optimal destination for my piece"""
        optimal_destination = ()
        optimal_side_destination = ()
        for k in range(len(temp)):
            playableDestination = temp[k]
            i, j = playableDestination[0], playableDestination[1]
            side = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
            if j == playable[1] - 2:
                return (i, j)
            if j == playable[1] + 2:
                return (i, j)
            if i == playable[0] - 2:
                return (i, j)
            if i == playable[0] + 2:
                return (i, j)
            # Verify if this destination can allow my ennemy to gain my piece
            if not optimal_destination:
                n = 0
                k = 0
                pos = 0  # Variable to incremente if my piece is on the extreme side where it can move to the corner
                for position in side:
                    x = position[0]
                    y = position[1]
                    if (j == 0 or j == len(board[0]) - 1) and (y == 0 or y == len(board[0]) - 1):
                        if position != playable:
                            if self.is_place_on_board(position):
                                col = self.get_no_empty_cell_color(board, position)
                                if col is None or col.lower() == TILES_COLOR[self.player_number].lower():
                                    optimal_destination = playableDestination
                    elif (i == 0 or i == len(board[0]) - 1) and (x == 0 or x == len(board) - 1):
                        if position != playable:
                            if self.is_place_on_board(position):
                                col = self.get_no_empty_cell_color(board, position)
                                if col is None or col.lower() == TILES_COLOR[self.player_number].lower():
                                    optimal_destination = playableDestination
                    if position != playable:
                        if self.is_place_on_board(position):
                            k = k + 1
                            col = self.get_no_empty_cell_color(board, position)
                            if col is None or col.lower() == TILES_COLOR[self.player_number].lower():
                                n = n + 1
                        else:
                            pos = pos + 1
                if (pos == 2):  # my move will take my piece to the corner
                    optimal_side_destination = playableDestination
                elif (n == k) and (not optimal_destination):  # if there is no pieces around my piece
                    if not self.can_be_gain_for_empty_cell(board, playableDestination):
                        optimal_destination = playableDestination
        if optimal_side_destination:
            #print(f"optimal_side_destination {optimal_side_destination}")
            return optimal_side_destination
        if optimal_destination:
            #print(f"optimal_destination {optimal_destination}")
            return optimal_destination
        return temp[random.randint(0, len(temp) - 1)]

    def gain_pieces(self, board, playables) -> List[tuple]:
        """This function take the playable pieces and return all pieces which can gain
           ennemy pieces"""

        for playable in playables:
            temp = self.get_piece_actual_moves(board, playable, self.player_number)
            for playableDestination in temp:
                i, j = playableDestination[0], playableDestination[1]
                if j == playable[1] - 2:
                    return playable
                if j == playable[1] + 2:
                    return playable
                if i == playable[0] - 2:
                    return playable
                if i == playable[0] + 2:
                    return playable

        return self.optimal_playable(board, playables)

    def optimal_playable(self, board, playables):
        """This function takes my playables pieces and return the one
           which have an ennemies pieces around or a optimal playable piece """
        temp = []
        for playable in playables:
            i, j = playable
            side = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
            cells = [(0, 0), (4, 0), (0, 5), (4, 5)]

            for index, position in enumerate(side):
                if self.is_place_on_board(position):
                    color = self.get_no_empty_cell_color(board, position)
                    if color is not None and color.lower() == TILES_COLOR[(self.player_number + 1) % 2].lower():
                        if self.piece_can_move(board, position, (self.player_number + 1) % 2):
                            if playable in cells:
                                if self.can_gain(board,playable,self.player_number):
                                    return playable
                                else:
                                    break
                            if self.can_gain_me(board, position,((self.player_number + 1) % 2),playable):
                                return playable
        if any(playables):
            for piece in playables:
                i, j = piece
                side = [(i, j - 2), (i, j + 2), (i - 2, j), (i + 2, j)]
                # ennemy_col = self.TILES_COLOR[(self.player_number+1)%2]
                for index, position in enumerate(side):
                    if self.is_place_on_board(position):
                        col = self.get_no_empty_cell_color(board, position)
                        if (col is None) or (col.lower() == TILES_COLOR[self.player_number].lower()):
                            if index == 0:
                                col_0 = self.get_no_empty_cell_color(board, (i, j - 1))
                                if col_0 is None:
                                    if piece not in temp:
                                        if self.can_move_now(board,piece):
                                            temp.append(piece)
                            elif index == 1:
                                col_1 = self.get_no_empty_cell_color(board, (i, j + 1))
                                if col_1 is None:
                                    if piece not in temp:
                                        if self.can_move_now(board, piece):
                                            temp.append(piece)
                            elif index == 2:
                                col_2 = self.get_no_empty_cell_color(board, (i - 1, j))
                                if col_2 is None:
                                    if piece not in temp:
                                        if self.can_move_now(board, piece):
                                            temp.append(piece)
                            elif index == 3:
                                col_3 = self.get_no_empty_cell_color(board, (i + 1, j))
                                if col_3 is None:
                                    if piece not in temp:
                                        if self.can_move_now(board, piece):
                                            temp.append(piece)

            if any(temp):
                return [temp[random.randint(0, len(temp) - 1)]]
        return playables

    def can_gain(self, board, cell, player):
        cell_destinations = self.get_piece_actual_moves(board, cell, player)
        for dest in cell_destinations:
            x, y = dest[0], dest[1]
            if y == cell[1] - 2:
                return True
            if y == cell[1] + 2:
                return True
            if x == cell[0] - 2:
                return True
            if x == cell[0] + 2:
                return True
        return False

    def can_be_gain(self, board, cell):
        i, j = cell
        player = self.TILES_COLOR[(self.player_number + 1) % 2]
        side = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
        for position in side:
            if self.is_place_on_board(position):
                col = self.get_no_empty_cell_color(board, position)
                if col is not None and col.lower() == TILES_COLOR[(self.player_number + 1) % 2].lower():
                    if self.can_gain(board, position, player):
                        return True
        return False

    def can_be_gain_for_empty_cell(self, board, cell):
        '''This function takes an empty place and return weither or not it's not a good place
            to place my piece
            '''
        i, j = cell
        n = 0
        side = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
        for index, position in enumerate(side):
            if self.is_place_on_board(position):
                col = self.get_no_empty_cell_color(board, position)
                if col is not None and col.lower() == TILES_COLOR[(self.player_number + 1) % 2].lower():
                    if index == 0:
                        cl = side[1]
                        if self.is_place_on_board(cl):
                            col_sl = self.get_no_empty_cell_color(board, cl)
                            if col_sl is not None:
                                n += 1
                        else:
                            n += 1
                    if index == 1:
                        cl = side[0]
                        if self.is_place_on_board(cl):
                            col_sl = self.get_no_empty_cell_color(board, cl)
                            if col_sl is not None:
                                n += 1
                        else:
                            n += 1
                    if index == 2:
                        cl = side[3]
                        if self.is_place_on_board(cl):
                            col_sl = self.get_no_empty_cell_color(board, cl)
                            if col_sl is not None:
                                n += 1
                        else:
                            n += 1
                    if index == 3:
                        cl = side[2]
                        if self.is_place_on_board(cl):
                            col_sl = self.get_no_empty_cell_color(board, cl)
                            if col_sl is not None:
                                n += 1
                        else:
                            n += 1
                else:
                    n += 1
            else:
                n += 1
        if n == 4:
            return False

        return True

    def optimal_place(self, board, empty_places):
        """This function take all the empty places on the board and return
        if exist the place not close to ennemy piece (or side to it)
        """
        for empty_place in empty_places:
            if not self.can_be_gain_for_empty_cell(board, empty_place):
                return [empty_place]

        return [empty_places[random.randint(0, len(empty_places) - 1)]]

    def are_not_blocked(self, board):
        """This function return a boolean to know if my six pieces on the
        board are blocked/can not move or not
        """
        playables = self.get_playable_pieces(board, self.player_number)
        if len(playables) != 0:
            for playable in playables:
                if len(self.get_piece_actual_moves(board, playable, self.player_number)) != 0:
                    return True
            return False
        return True

    def can_gain_me(self,board,cell,player,playable):
        """

        :param board:
        :param cell:  case to verify if it can be gain
        :param playable:  piece which can play
        :return: True or False
        """
        cell_destinations = self.get_piece_actual_moves(board, cell, player)
        for dest in cell_destinations:
            x, y = dest[0], dest[1]
            if y == cell[1] - 2:
                if x==playable[0]:
                    return True
            if y == cell[1] + 2:
                if x==playable[0]:
                    return True
            if x == cell[0] - 2:
                if y==playable[1]:
                    return True
            if x == cell[0] + 2:
                if y==playable[1]:
                    return True
        return False

    ''' End function added by HGN '''
