# -*- coding: utf-8 -*-
import random
from util import timeout
from player import Player
TILES_COLOR = ["Black", "White"]


class AI(Player):

    # Team modify this
    name = "Dark Vador"

    def __init__(self, player_number, board_size):
        Player.__init__(self, player_number, board_size)

    def get_player_score(self):
        return self.captured_pieces

    def get_player_name(self):
        return self.name
    
    @timeout(seconds=0.1)
    def play(self, depth_to_cover, board, can_steal):
        if can_steal:
            ennemyPieces=[]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] is not None and TILES_COLOR[(self.player_number+1)%2].lower()==board[i][j].lower():
                        ennemyPieces.append((i,j))
            if not ennemyPieces:
                return -1, -1
            return ennemyPieces[random.randint(0,len(ennemyPieces)-1)]

        wantTomove=0
        if self.player_pieces_in_hand>0:
            wantTomove=random.randint(0, 1)
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
            return playable[random.randint(0, len(playable)-1)]
        else:
            temp=self.get_all_possibles_moves(board, self.player_number)["pieces"]
            playable=temp[random.randint(0, len(temp)-1)]
            temp=self.get_piece_actual_moves(board, playable, self.player_number)
            playableDestination=temp[random.randint(0, len(temp)-1)]
            return (playable[0],playable[1],playableDestination[0],playableDestination[1])
