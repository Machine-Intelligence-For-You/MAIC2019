# -*- coding: utf-8 -*-
import random
from player import Player
TILES_COLOR = ["Black", "White"]
class AI(Player):

    #Team modify this
    name = "Dark Vador Oh"
    def __init__(self, player_number, board_size):
        Player.__init__(self, player_number, board_size)



    def get_player_score(self):
        return self.captured_pieces

    def get_player_name(self):
        return self.name
    """
    The following functions may be removed. I'm seeing if it's okey to seperate the tiles on board ans the others
    """
    def add_captured_pieces(self):
        self.captured_pieces += 1

    def reduce_player_pieces(self):
        self.player_pieces -= 1



    def play(self, depth_to_cover, board, can_steal):

        #while(1):
        #    a=0
        #    print(a)
        if can_steal:
            ennemyPieces=[]
            print("je suis la")
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] is not None and TILES_COLOR[(self.player_number+1)%2].lower()==board[i][j].lower():
                        ennemyPieces.append((i,j))
            print("je suis pas la")
            print(ennemyPieces)
            if not ennemyPieces:
                return  (-1, -1)
            return ennemyPieces[random.randint(0,len(ennemyPieces)-1)]

        wantTomove=0

        if self.player_pieces_in_hand>0:

            wantTomove=random.randint(0, 1)
            # print (wantTomove)
            # print (len(board),len(board[0]))
            print("herre")
            if(len(self.get_all_possibles_moves(board, self.player_number)["empty_cells"])==len(board)*len(board[0])):
                wantTomove=0
                print ("NOWWW 1")

            print ("GOLLD")
            if(len(self.get_movable_pieces_by_player(board, self.player_number))==0):
                wantTomove=0
                print ("NOWWW 2")
        else:
            wantTomove=1

        if wantTomove==0:
            playable=[]
            i=-1
            print ("Avec puissance 1")
            for line in board:
                i+=1
                j=-1
                for case in line:
                    j+=1
                    if case is None:
                        playable.append((i,j))
            # print (playable)
            return playable[random.randint(0, len(playable)-1)]
        else:
            print ("TCHOHOOO")
            temp=self.get_all_possibles_moves(board, self.player_number)["pieces"]
            print(temp)
            # print (self.get_all_possibles_moves(self.player_number,board))
            playable=temp[random.randint(0, len(temp)-1)]
            print ("Avec puissance 2")
            temp=self.get_piece_actual_moves(board, playable, self.player_number)
            print(playable, temp)
            playableDestination=temp[random.randint(0, len(temp)-1)]
            print("lol")
            print((playable[0],playable[1],playableDestination[0],playableDestination[1]))
            return (playable[0],playable[1],playableDestination[0],playableDestination[1])