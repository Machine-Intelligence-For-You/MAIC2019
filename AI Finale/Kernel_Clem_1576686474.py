# -*- coding: utf-8 -*-
import random
from util import timeout
from player import Player
import time
import copy
TILES_COLOR = ["Black", "green"]
import sys


class AI(Player):

    # Team modify this
    name = "Kernel_Clem"

    def __init__(self, player_number, board_size):
        Player.__init__(self, player_number, board_size)
        self.previous_play = (-1,-1)

    def get_player_score(self):
        return self.captured_pieces

    def get_player_name(self):
        return self.name
    
    def potential_Win_Play(self, board, cell, player_number):
        i, j = cell
        possible = self.get_possible_moves(cell)
        if  possible is not None:
            for move in possible:
                if (not self.is_empty_cell(board, move)) and self.get_no_empty_cell_color(board, move) != self.TILES_COLOR[player_number]:
                    k, l = move
                    if i == k and j < l and self.is_empty_cell(board, (i, j + 2)):
                        return 1
                    elif i == k and l < j and self.is_empty_cell(board, (i, j - 2)):
                        return 1
                    elif j == l and i < k and self.is_empty_cell(board, (i + 2, j)):
                        return 1
                    elif j == l and k < i and self.is_empty_cell(board, (i - 2, j)):
                        return 1
        return 0

    def winning_pieces_by_player(self, board, player_number):
        pieces = self.get_playable_pieces(board, player_number)
        moves = list()
        for piece in pieces:
            if self.potential_Win_Play(board, piece, player_number):
                moves.append(piece)
        return moves

    def get_piece_winning_moves(self, board, playable, player_number):
        i, j = playable
        possible = self.get_possible_moves(playable)
        random.shuffle(possible)
        win = []
        if  possible is not None:
            for move in possible:
                if (not self.is_empty_cell(board, move)) and self.get_no_empty_cell_color(board, move) != self.TILES_COLOR[player_number]:
                    k, l = move
                    if i == k and j < l and self.is_empty_cell(board, (i, j + 2)):
                        win.append((i, j + 2))
                    elif i == k and l < j and self.is_empty_cell(board, (i, j - 2)):
                        win.append((i, j - 2))
                    elif j == l and i < k and self.is_empty_cell(board, (i + 2, j)):
                        win.append((i + 2, j))
                    elif j == l and k < i and self.is_empty_cell(board, (i - 2, j)):
                        win.append((i - 2, j))
        return win

    def type(self,cell1,cell2):
        if (max(cell2[0],cell1[0]),max(cell1[1],cell2[1])) in [cell1,cell2]:
            return (1)

        else:
            return (2)

    def occasion(self,board,cell1,cell2,player_number):
        if self.is_empty_cell(board,cell1) or self.is_empty_cell(board,cell2) or self.distance(cell1,cell2)!=2:
            return None
        if cell1[0]==cell2[0]:
            if self.get_no_empty_cell_color(board, (cell1[0],min(cell1[1],cell2[1])+1)) != self.TILES_COLOR[player_number]:
                if self.is_empty_cell(board, (cell1[0], min(cell1[1],cell2[1])-1)) and self.is_empty_cell(board, (cell1[0], max(cell1[1],cell2[1])+1)):
                    dang = self.move_in_Danger(board, None, (cell1[0],min(cell1[1],cell2[1])+1), (player_number+1)%2)
                    if dang[0]==1:
                        return None
                    return([[(cell1[0],min(cell1[1],cell2[1])+1)],self.get_no_empty_cell_color(board, (cell1[0],min(cell1[1],cell2[1])+1)) != self.TILES_COLOR[(player_number+1)%2]])
            return None

        elif cell1[1]==cell2[1]:
            if self.get_no_empty_cell_color(board, (cell1[1],min(cell1[0],cell2[0])+1)) != self.TILES_COLOR[player_number]:
                if self.is_empty_cell(board, (cell1[1], min(cell1[0],cell2[0])-1)) and self.is_empty_cell(board, (cell1[1], max(cell1[0],cell2[0])+1)):
                    dang = self.move_in_Danger(board, None, (cell1[1],min(cell1[0],cell2[0])+1), (player_number+1)%2)
                    if dang[0]==1:
                        return None
                    return([[(cell1[1],min(cell1[0],cell2[0])+1)],self.get_no_empty_cell_color(board, (cell1[1],min(cell1[0],cell2[0])+1)) != self.TILES_COLOR[(player_number+1)%2]])
            return None

        else:
            type = self.type(cell1,cell2)
            cells = []
            dec =[]
            if type == 1:
                if self.get_no_empty_cell_color(board, (max(cell2[0],cell1[0])-1,max(cell1[1],cell2[1]))) != self.TILES_COLOR[player_number]:
                    if self.is_empty_cell(board, (max(cell2[0],cell1[0])+1,max(cell1[1],cell2[1]))) and self.is_empty_cell(board, (min(cell2[0],cell1[0]),min(cell1[1],cell2[1])-1)):
                        dang = self.move_in_Danger(board, None, (max(cell2[0],cell1[0])-1,max(cell1[1],cell2[1])), (player_number+1)%2)
                        if dang[0]!=1:                     
                            cells.append((max(cell2[0],cell1[0])-1,max(cell1[1],cell2[1])))
                            dec.append(self.get_no_empty_cell_color(board, (max(cell2[0],cell1[0])-1,max(cell1[1],cell2[1]))) != self.TILES_COLOR[(player_number+1)%2])
                if self.get_no_empty_cell_color(board, (max(cell2[0],cell1[0]),max(cell1[1],cell2[1])-1)) != self.TILES_COLOR[player_number]:
                    if self.is_empty_cell(board, (max(cell2[0],cell1[0]),max(cell1[1],cell2[1])+1)) and self.is_empty_cell(board, (min(cell2[0],cell1[0])-1,min(cell1[1],cell2[1]))):
                        dang = self.move_in_Danger(board, None, (max(cell2[0],cell1[0]),max(cell1[1],cell2[1])-1), (player_number+1)%2)
                        if dang[0]!=1:     
                            cells.append((max(cell2[0],cell1[0]),max(cell1[1],cell2[1])-1))
                            dec.append(self.get_no_empty_cell_color(board, (max(cell2[0],cell1[0]),max(cell1[1],cell2[1])-1)) != self.TILES_COLOR[(player_number+1)%2])
                if len(cells)>0:
                    return([cells,dec])
                return None

            elif type == 2:
                if self.get_no_empty_cell_color(board, (max(cell2[0],cell1[0])-1,max(cell1[1],cell2[1])-1)) != self.TILES_COLOR[player_number]:
                    if self.is_empty_cell(board, (max(cell2[0],cell1[0])+1,min(cell1[1],cell2[1]))) and self.is_empty_cell(board, (min(cell2[0],cell1[0]),max(cell1[1],cell2[1])+1)):
                        dang = self.move_in_Danger(board, None, (max(cell2[0],cell1[0])-1,max(cell1[1],cell2[1])-1), (player_number+1)%2)
                        if dang[0]!=1:
                            cells.append((max(cell2[0],cell1[0])-1,max(cell1[1],cell2[1])-1))
                            dec.append(self.get_no_empty_cell_color(board, (max(cell2[0],cell1[0])-1,max(cell1[1],cell2[1])-1)) != self.TILES_COLOR[(player_number+1)%2])
                if self.get_no_empty_cell_color(board, (max(cell2[0],cell1[0]),max(cell1[1],cell2[1]))) != self.TILES_COLOR[player_number]:
                    if self.is_empty_cell(board, (max(cell2[0],cell1[0]),min(cell1[1],cell2[1])-1)) and self.is_empty_cell(board, (min(cell2[0],cell1[0])-1,max(cell1[1],cell2[1]))):
                        dang = self.move_in_Danger(board, None, (max(cell2[0],cell1[0]),max(cell1[1],cell2[1])), (player_number+1)%2)
                        if dang[0]!=1:
                            cells.append((max(cell2[0],cell1[0]),max(cell1[1],cell2[1])))
                            dec.append(self.get_no_empty_cell_color(board, (max(cell2[0],cell1[0]),max(cell1[1],cell2[1]))) != self.TILES_COLOR[(player_number+1)%2])
                if len(cells)>0:
                    return([cells,dec])
                return None

    def Occasion(self,board,player_number):
        out = []
        plays = self.get_playable_pieces(board, player_number)
        for cell1 in plays:
            for cell2 in plays:
                if cell1!=cell2:
                    occas = self.occasion(board,cell1,cell2,player_number)
                    if occas!=None:
                        out+=occas[0]

        return (list(set(out)))

    def fill(self,board,player_number,instruc):
        c = copy.deepcopy(board)
        if len(instruc)==2:
            x,y = instruc
            c[x][y] = self.TILES_COLOR[player_number]
        if len(instruc)==4:
            x,y,z,t = instruc
            c[x][y] = None
            c[z][t] = self.TILES_COLOR[player_number]

            if self.distance((x,y),(z,t))!=1:
                x,y = (min(x,z)+abs(z-x)//2,min(y,t)+abs(y-t)//2)
                c[x][y] = None
        return c


    def move_in_Danger_by(self,board, src, dest, piec):
        i,j = piec
        k,l = dest
        if i == k and j == l-1:
            if self.is_empty_cell(board, (i, j + 2)) or (i, j + 2) == src:
                return 1
        elif i == k and l == j-1:
            if self.is_empty_cell(board, (i, j - 2)) or (i, j - 2) == src:
                return 1
        elif j == l and i == k-1:
            if self.is_empty_cell(board, (i + 2, j)) or (i + 2, j) == src:
                return 1
        elif j == l and k == i-1:
            if self.is_empty_cell(board, (i - 2, j)) or (i - 2, j) == src:
                return 1
        return 0

    def move_in_Danger(self,board, src, dest, player_number):
        out = 0
        for piec in self.get_playable_pieces(board, (player_number+1)%2):
            if self.move_in_Danger_by(board, src, dest, piec):
                out +=1
        return [out>0,out]

    def distance(self,piece,cell):
        return (abs(cell[0]-piece[0]) + abs(cell[1]-piece[1]))

    def Distance(self,piece,Set,board):
        d = len(board)+len(board[0])
        for cell in Set:
        	dis = self.distance(piece,cell)
        	if dis<d:
        		d = dis
        return (d)

    def distanceSet(self,Set1,Set2,board):
        out = []
        for cell in Set1:
            out.append(self.Distance(cell,Set2,board))
        return (out)

    def Dangers(self, board, player_number):
        P_Movable = self.get_movable_pieces_by_player(board, player_number)
        Danger = {}

        for cell in P_Movable:
            d = self.move_in_Danger(board, None, cell, player_number)
            if d[0]==True:
                Danger[cell]=d[1]
        return Danger

    def Solve(self, board, player_number):
        P_Movable = self.get_movable_pieces_by_player(board, player_number)
        out = {}
        Danger = self.Dangers(board, player_number)
        random.shuffle(P_Movable)
        for cell in P_Movable:
            d = self.get_piece_actual_moves(board, cell, player_number)
            for move in d:
                copy_b = board.copy()
                copy_b = self.fill(copy_b, player_number,(cell[0],cell[1],move[0],move[1]))
                Dang   = self.Dangers(copy_b, player_number)
                if sum(Dang.values())==0:
                    if not self.Risky(board, player_number, (cell[0],cell[1],move[0],move[1])):
                        return ((cell[0],cell[1],move[0],move[1]))
                if sum(Dang.values()) - sum(Danger.values())<=0:
                    out[(cell[0],cell[1],move[0],move[1])] = sum(Dang.values())

        if self.player_pieces_in_hand>0:
            Set = [(i,j) for i in range(len(board)) for j in range(len(board[0]))]
            random.shuffle(Set)
            for cell in Set:
                if not self.is_empty_cell(board,cell):
                    continue
                copy_b = board.copy()
                copy_b = self.fill(copy_b, player_number,(cell[0],cell[1]))
                Dang   = self.Dangers(copy_b, player_number)
                if sum(Dang.values())==0:
                    if not self.Risky(board, player_number, (cell[0],cell[1])):
                        return ((cell[0],cell[1]))
                if sum(Dang.values()) - sum(Danger.values())<=0:
                    out[(cell[0],cell[1])] = sum(Dang.values())
        return out

    def Move_No_Problems(self,board,cell, player_number):
        P_Movable = self.get_movable_pieces_by_player(board, player_number)
        Danger = self.Dangers(board, player_number)
        for piece in P_Movable:
            if cell in self.get_piece_actual_moves(board, piece, player_number):
                copy_b = board.copy()
                copy_b = self.fill(copy_b, player_number,(piece[0],piece[1],cell[0],cell[1]))
                Dang   = self.Dangers(copy_b, player_number)
                if sum(Dang.values()) - sum(Danger.values())<=0:
                    return ((piece[0],piece[1],cell[0],cell[1]))

        if self.player_pieces_in_hand>0:
            copy_b = board.copy()
            copy_b = self.fill(copy_b, player_number,(cell[0],cell[1]))
            Dang   = self.Dangers(copy_b, player_number)
            if sum(Dang.values())==0:
                return ((cell[0],cell[1]))
        return None

    def shuffle(self, studentDict):
        keys =  list(studentDict.keys())
        random.shuffle(keys)

        ShuffledStudentDict = dict()
        for key in keys:
            ShuffledStudentDict.update({key:studentDict[key]})
        return(ShuffledStudentDict)

    def get_Border(self,board,cell,player_number):
    	x,y=cell
    	return [(x+a,y+b) for a in [-1,0,1] for b in [-1,0,1] if (a,b)!=(0,0) if self.is_empty_cell(board, (x+a,y+b))]

    def Opponent(self, board, player_number, depth_to_cover = 9, can_steal = 0):
        if can_steal:
            ennemyPieces=[]
            ennemy_Potential_Pieces = []
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] is not None and TILES_COLOR[(self.player_number+1)%2].lower()==board[i][j].lower():
                        ennemyPieces.append((i,j))
                        if self.potential_Win_Play(board, (i,j), (self.player_number+1)%2):
                            ennemy_Potential_Pieces.append((i,j))
            if not ennemy_Potential_Pieces:
                if (self.get_player_score()+len(ennemyPieces))<12:
                    return (-1, -1)

                random.shuffle(ennemyPieces)
                distance = self.distanceSet(ennemyPieces,self.get_playable_pieces(board, self.player_number),board)
                if self.get_playable_pieces(board, self.player_number)>=self.get_playable_pieces(board, (self.player_number+1)%2):
                	return ennemyPieces[distance.index(min(distance))]
                return ennemyPieces[distance.index(max(distance))]
            return ennemy_Potential_Pieces[random.randint(0,len(ennemy_Potential_Pieces)-1)]

        Winning_Pieces = self.winning_pieces_by_player(board, self.player_number)
        if len(Winning_Pieces) != 0:
            playable=Winning_Pieces[random.randint(0, len(Winning_Pieces)-1)]
            Destination=self.get_piece_winning_moves(board, playable, self.player_number)
            return (playable[0],playable[1],Destination[0],Destination[1])
        
        P_Movable = self.get_movable_pieces_by_player(board, self.player_number)
        random.shuffle(P_Movable)
        Danger = []

        for cell in P_Movable:
            if self.move_in_Danger(board, None, cell, self.player_number):
                Danger.append(cell)

        random.shuffle(Danger)
        if Danger:
            for cell in Danger:
            	mov = self.get_piece_actual_moves(board, cell, self.player_number)
            	random.shuffle(mov)
            	for move in mov:
                    if not self.move_in_Danger(board, cell, move, self.player_number) and not self.dang_move(board, cell, move, self.player_number):
                        return (cell[0],cell[1],move[0],move[1])
            	
            	if len(mov)==1:
            		if not self.move_in_Danger(board, None, mov[0], self.player_number):
            			return(mov[0])

        Empty = []
        NoDangerE = []
        FavorE = {}
        if len(self.get_playable_pieces(board, self.player_number))>=9 or self.player_pieces_in_hand == 0:
            NoDanger = []
            Favor = []
            if P_Movable:
                for piece in P_Movable:
                    for move in self.get_piece_actual_moves(board, piece, self.player_number):
                        if not self.move_in_Danger(board, piece, move, self.player_number) and not self.dang_move(board, piece, move, self.player_number):
                            counter = 0
                            for pie in P_Movable:
                                if pie != piece:
                                    if self.move_in_Danger(board, piece, pie, self.player_number) or self.dang_move(board, piece, pie, self.player_number):
                                        break
                                    counter +=1
                            if counter == len(P_Movable)-1:
                                NoDanger.append((piece[0],piece[1],move[0],move[1]))
                                if self.potential_Win_Play(board, move, self.player_number):
                                    Favor.append((piece[0],piece[1],move[0],move[1]))
                
                if not Favor:
                	if NoDanger:
                		return NoDanger[random.randint(0,len(NoDanger)-1)]

                else :
                    return Favor[random.randint(0,len(Favor)-1)]

        if self.player_pieces_in_hand>0:
            Empty = self.get_empty_cells(board)
            random.shuffle(Empty)
            if len(Empty) == len(board)*len(board[0]):
                return Empty[random.randint(0, len(Empty)-1)]

            NoDanger = []
            Favor    = {}
            for cell in Empty:
                if not self.move_in_Danger(board, None, cell, self.player_number):
                    NoDanger.append(cell)
                    temp = self.count_winning_moves(board, cell, self.player_number)
                    if len(temp)>0:
                        Favor[cell] = len(temp)

            if not Favor:
                if NoDanger:
                    return NoDanger[random.randint(0,len(NoDanger)-1)]
            else :
                return max(Favor, key=Favor.get)
            
            if Empty:
                return Empty[random.randint(0, len(Empty)-1)]

        if P_Movable:
            playable=P_Movable[random.randint(0, len(P_Movable)-1)]
            temp=self.get_piece_actual_moves(board, playable, self.player_number)
            Destination=temp[random.randint(0, len(temp)-1)]
            return (playable[0],playable[1],Destination[0],Destination[1])

    def Risky(self,board, player_number, move):
        copy_b = board.copy()
        copy_b = self.fill(copy_b,player_number,move)
        elt = self.Opponent(board, (player_number+1)%2)
        if elt != None:
            copy_b = self.fill(copy_b,(player_number+1)%2,elt)
            plays = self.get_playable_pieces(copy_b, player_number)
            for pl in plays:
                copy_c = copy_b.copy()
                copy_c = self.fill(copy_c,player_number,pl)
                Dang = self.Dangers(copy_c, player_number)
                if sum(Dang.values())==0:
                    return 0
            return 1
        return 0

    @timeout(seconds = 0.1)
    def play(self, depth_to_cover, board, can_steal):
        tim = time.time()
        if can_steal:
            ennemyPieces=[]
            ennemy_Potential_Pieces = []
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] is not None and TILES_COLOR[(self.player_number+1)%2].lower()==board[i][j].lower():
                        ennemyPieces.append((i,j))
                        if self.potential_Win_Play(board, (i,j), (self.player_number+1)%2):
                            ennemy_Potential_Pieces.append((i,j))
            if not ennemy_Potential_Pieces:
                if (self.get_player_score()+len(ennemyPieces))<12:
                    return (-1, -1)

                random.shuffle(ennemyPieces)
                distance = self.distanceSet(ennemyPieces,self.get_playable_pieces(board, self.player_number),board)
                if distance:
                    if self.get_playable_pieces(board, self.player_number)>=self.get_playable_pieces(board, (self.player_number+1)%2):
                        cp = distance.copy()
                        while 1 in cp:
                            cp.remove(1)
                        if cp:
                            return ennemyPieces[distance.index(min(cp))]
                    return ennemyPieces[distance.index(max(distance))]
            return ennemy_Potential_Pieces[random.randint(0,len(ennemy_Potential_Pieces)-1)]

        Danger = self.Dangers(board, self.player_number)
        Winning_Pieces = self.winning_pieces_by_player(board, self.player_number)

        if len(Winning_Pieces) != 0:
            random.shuffle(Winning_Pieces)
            for piece in Winning_Pieces:
                Win = self.get_piece_winning_moves(board, piece, self.player_number)
                for win in Win:
                    copy_b = board.copy()
                    copy_b = self.fill(copy_b,self.player_number,(piece[0],piece[1],win[0],win[1]))
                    Dang   = self.Dangers(copy_b, self.player_number)
                    if sum(Dang.values()) - sum(Danger.values()) <=1:
                        return((piece[0],piece[1],win[0],win[1]))
        
        if Danger:
            solve = self.Solve(board,self.player_number)
            if type(solve) != dict:
                return (solve)
            occas = self.Occasion(board,(self.player_number+1)%2)
            random.shuffle(occas)
            for oc in occas:
                if not self.is_empty_cell(board,oc):
                    continue
                copy_b = board.copy()
                copy_b = self.fill(copy_b,self.player_number,(oc[0],oc[1]))
                Dang   = self.Dangers(copy_b, self.player_number)
                if sum(Dang.values()) - sum(Danger.values()) <=0:
                    if self.player_pieces_in_hand > 0:
                        return((oc[0],oc[1]))

            if solve:
                return min(solve, key=solve.get)

        Empty = []
        NoDangerE = []
        FavorE = {}
        if len(self.get_playable_pieces(board, self.player_number))<=12 or self.player_pieces_in_hand == 0:
            occas = self.Occasion(board,(self.player_number+1)%2)
            random.shuffle(occas)
            for oc in occas:
                if not self.is_empty_cell(board,oc):
                    continue
                mv = self.Move_No_Problems(board,oc, self.player_number)
                if mv != None:
                    return (mv)

            x,y = len(board),len(board[0])
            Priv = [(0,0),(x-1,0),(0,y-1),(x-1,y-1)]
            if self.player_pieces_in_hand>8:
                if self.player_pieces_in_hand==12:
                    p = Priv
                    self.previous_play = p[random.randint(0, len(p)-1)]
                    return self.previous_play

                if self.player_pieces_in_hand>9 and self.get_no_empty_cell_color(board,self.previous_play)==self.TILES_COLOR[self.player_number]:
                    plays = self.get_piece_actual_moves(board, self.previous_play, self.player_number)
                    for play in plays:
                        if self.distance(self.previous_play,play)==1 and self.move_in_Danger(board,None,play,self.player_number)[0]==0:
                            return play
                if self.player_pieces_in_hand==9 and self.get_no_empty_cell_color(board,self.previous_play)==self.TILES_COLOR[self.player_number]:
                    plays = self.get_Border(board, self.previous_play, self.player_number)
                    for play in plays:
                        if self.distance(self.previous_play,play)==2 and self.previous_play[0]!=play[0] and self.previous_play[1]!=play[1] and self.move_in_Danger(board,None,play,self.player_number)[0]==0:
                            return play

            NoDanger = {}
            Favor = {}
            NoDangerE = {}
            P_Movable = self.get_movable_pieces_by_player(board, self.player_number)
            random.shuffle(P_Movable)
            if P_Movable:
                Danger = self.Dangers(board, self.player_number)
                for piece in P_Movable:
                    for move in self.get_piece_actual_moves(board, piece, self.player_number):
                        copy_b = board.copy()
                        copy_b = self.fill(copy_b,self.player_number,(piece[0],piece[1],move[0],move[1]))
                        Dang = self.Dangers(copy_b, self.player_number)
                        if sum(Dang.values()) - sum(Danger.values()) <=0:
                            if not self.Occasion(copy_b,self.player_number):
                                if self.potential_Win_Play(copy_b, (move[0],move[1]), self.player_number):
                                    return ((piece[0],piece[1],move[0],move[1]))
                                Favor[(piece[0],piece[1],move[0],move[1])] = sum(Dang.values())
                            NoDangerE[(piece[0],piece[1],move[0],move[1])] = sum(Dang.values())
                        NoDanger[(piece[0],piece[1],move[0],move[1])] = sum(Dang.values())

                if Favor:
                    Favor = self.shuffle(Favor)
                    return min(Favor, key=Favor.get)
                if NoDangerE:
                    NoDangerE = self.shuffle(NoDangerE)
                    return min(NoDangerE, key=NoDangerE.get)
                if self.player_pieces_in_hand == 0:
                    if NoDanger:
                        NoDanger = self.shuffle(NoDanger)
                        return min(NoDanger, key=NoDanger.get)
                else:
                    Reserve = NoDanger

        if self.player_pieces_in_hand>0:
            x,y = len(board),len(board[0])
            Priv = [(0,0),(x-1,0),(0,y-1),(x-1,y-1)]
            Empty = self.get_empty_cells(board)
            if len(Empty) == len(board)*len(board[0]):
                p = Priv+[(x//2,y//2)]
                return p[random.randint(0, len(p)-1)]

            random.shuffle(Empty)
            NoDanger = {}

            occas = self.Occasion(board,(self.player_number+1)%2)
            random.shuffle(occas)
            for oc in occas:
                if not self.is_empty_cell(board,oc):
                    continue
                Danger = self.Dangers(board, self.player_number)
                copy_b = board.copy()
                copy_b = self.fill(copy_b,self.player_number,(oc[0],oc[1]))
                Dang = self.Dangers(copy_b, self.player_number)
                if sum(Dang.values()) - sum(Danger.values()) <=0:
                    if not self.Occasion(copy_b,self.player_number):
                        return (oc)
                    NoDanger[(oc[0],oc[1])] = sum(Dang.values())

            if NoDanger:
                NoDanger = self.shuffle(NoDanger)
                return min(NoDanger, key=NoDanger.get)

            NoDanger = {}
            for cell in Empty:
                Danger = self.Dangers(board, self.player_number)
                copy_b = board.copy()
                copy_b = self.fill(copy_b,self.player_number,(cell[0],cell[1]))
                Dang = self.Dangers(copy_b, self.player_number)
                if sum(Dang.values()) - sum(Danger.values()) <=0:
                    if not self.Occasion(copy_b,self.player_number):
                        if self.potential_Win_Play(copy_b, cell, self.player_number):
                            return (cell)
                        NoDangerE[cell] = sum(Dang.values())
                    NoDanger[cell] = sum(Dang.values())

            if NoDangerE:
                NoDangerE = self.shuffle(NoDangerE)
                return min(NoDangerE, key=NoDangerE.get)

            random.shuffle(Priv)
            emp = {}
            for elt in Priv:
                if self.is_empty_cell(board,elt):
                    emp[elt] = self.Distance(elt,self.get_playable_pieces(board,(self.player_number+1)%2),board)

            if emp:
                emp = self.shuffle(emp)
                return min(emp, key=emp.get)

            if NoDanger:
                NoDanger = self.shuffle(NoDanger)
                return min(NoDanger, key=NoDanger.get)

        if P_Movable:
            if Reserve:
                Reserve = self.shuffle(Reserve)
                return min(Reserve, key=Reserve.get)