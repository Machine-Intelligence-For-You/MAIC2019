# -*- coding: utf-8 -*-
from random import *
from util import timeout
import random
from player import Player


TILES_COLOR = ["black", "green"]


class AI(Player):

    name = "SMA"

    def __init__(self, player_number, board_size):
        Player.__init__(self, player_number, board_size)
        self.my_preview_piece_on_board=0
        self.my_piece_in_hand=0
        self.opponent_preview_piece_on_board=0
        self.opponent_piece_in_hand=0

    def get_player_score(self):
        return self.captured_pieces

    def get_player_name(self):
        return self.name

    def _cutoff(self, board, depth, nbr):
        if len(self.get_all_possibles_moves(board,self.player_number)) == 0 or self.captured_pieces==12 or depth==2+nbr:
            return True
        else:
            return False

    def _opponent_piece_on_board(self, board):
        ennemyPieces=list()
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] is not None and TILES_COLOR[(self.player_number+1)%2].lower()==board[i][j].lower():
                    ennemyPieces.append((i,j))
        return ennemyPieces

    def _my_piece_on_board(self, board):
        myPieces=list()
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] is not None and TILES_COLOR[(self.player_number)].lower()==board[i][j].lower():
                    myPieces.append((i,j))
        return myPieces 

    def _evaluate(self, board, is_me,new_piece):
       
        value = 0
        if is_me:
            opponent_color = TILES_COLOR[(self.player_number + 1) % 2].lower()
            player_number = self.player_number
            pieces_in_hand=self.my_piece_in_hand-new_piece
            my_piece_on_board = len(self.get_playable_pieces(board,player_number))
            captured_pieces = self.opponent_preview_piece_on_board + new_piece - len(self._opponent_piece_on_board(board))
            my_piece_captured = self.my_preview_piece_on_board + new_piece - len(self._my_piece_on_board(board))
            liste = self.get_playable_pieces(board, player_number)
            for piece in liste:
                i, j = piece
                danger = False
                if self.get_no_empty_cell_color(board, (i, j + 1)) == opponent_color:
                    if self.is_empty_cell(board, (i, j - 1)):
                        danger = True
                if self.get_no_empty_cell_color(board, (i, j - 1)) == opponent_color:
                    if self.is_empty_cell(board, (i, j + 1)):
                        danger = True
                if self.get_no_empty_cell_color(board, (i + 1, j)) == opponent_color:
                    if self.is_empty_cell(board, (i - 1, j)):
                        danger = True
                if self.get_no_empty_cell_color(board, (i - 1, j)) == opponent_color:
                    if self.is_empty_cell(board, (i + 1, j)):
                        danger = True
                if self.get_no_empty_cell_color(board,(i,j + 1)) == opponent_color and self.get_no_empty_cell_color(
                board, (i, j - 1)) == opponent_color:
                    if not(self.is_empty_cell(board, (i + 1, j)) and self.is_empty_cell(board, (i - 1, j))):
                        value -= 4

                if self.get_no_empty_cell_color(board,(i + 1,j)) == opponent_color and self.get_no_empty_cell_color(
                    board, (i - 1, j)) == opponent_color:
                    if not(self.is_empty_cell(board, (i, j + 1)) and self.is_empty_cell(board, (i, j - 1))):
                        value -= 4

                if i == 0 and (j == 0 or j == len(board[0]) - 1):
                    danger = False
                if i == len(board)-1 and (j == 0 or j == len(board[0]) - 1):
                    danger = False

                if danger == False:
                    value += 2
                elif danger == True:
                    value -= 2

            value += captured_pieces
            if captured_pieces > my_piece_captured:
                value += 2
            elif captured_pieces < my_piece_captured:
                value -= 2
            return value
        else:
            player_number = (self.player_number + 1) % 2
            opponent_color = TILES_COLOR[self.player_number].lower()
            pieces_in_hand=self.opponent_piece_in_hand-new_piece
            my_piece_on_board = len(self.get_playable_pieces(board,player_number))
            captured_pieces= self.my_preview_piece_on_board + new_piece - len(self._my_piece_on_board(board))
            my_piece_captured = self.opponent_preview_piece_on_board + new_piece - len(self._opponent_piece_on_board(board))
            liste = self.get_playable_pieces(board, player_number)
            for piece in liste:
                i, j = piece
                danger = False
                if self.get_no_empty_cell_color(board, (i, j + 1)) == opponent_color:
                    if self.is_empty_cell(board, (i, j - 1)):
                        danger = True
                if self.get_no_empty_cell_color(board, (i, j - 1)) == opponent_color:
                    if self.is_empty_cell(board, (i, j + 1)):
                        danger = True
                if self.get_no_empty_cell_color(board, (i + 1, j)) == opponent_color:
                    if self.is_empty_cell(board, (i - 1, j)):
                        danger = True
                if self.get_no_empty_cell_color(board, (i - 1, j)) == opponent_color:
                    if self.is_empty_cell(board, (i + 1, j)):
                        danger = True

                if self.get_no_empty_cell_color(board,(i,j + 1)) == opponent_color and self.get_no_empty_cell_color(
                     board, (i, j - 1)) == opponent_color:
                    if not(self.is_empty_cell(board, (i + 1, j)) and self.is_empty_cell(board, (i - 1, j))):
                        value -= 4

                if self.get_no_empty_cell_color(board,(i + 1,j)) == opponent_color and self.get_no_empty_cell_color(
                    board, (i - 1, j)) == opponent_color:
                    if not(self.is_empty_cell(board, (i, j + 1)) and self.is_empty_cell(board, (i, j - 1))):
                        value -= 4

                if i == 0 and (j == 0 or j == len(board[0]) - 1):
                    danger = False
                if i == len(board)-1 and (j == 0 or j == len(board[0]) - 1):
                    danger = False

                if danger == False:
                    value += 2
                elif danger==True:
                    value -= 2
            
            value += my_piece_captured
            if captured_pieces > my_piece_captured  :
                value += 2
            elif captured_pieces < my_piece_captured:
                value -= 2
            return value

    def _apply_action_empty(self,action,board,player_number):
        new_board=self.clone(board)
        x,y=action[0],action[1]
        new_board[x][y]=TILES_COLOR[player_number]
        return new_board

    def _apply_action_pieces(self,action,board,player_number):
        new_board=self.clone(board)
        origin_x,origin_y,destination_x,destination_y=action[0][0],action[0][1],action[1][0],action[1][1]
        new_board[destination_x][destination_y]=new_board[origin_x][origin_y]
        new_board[origin_x][origin_y]=None
        if origin_x==destination_x and destination_y==origin_y+2:
            new_board[origin_x][origin_y+1]=None
        if origin_x==destination_x and destination_y==origin_y-2:
            new_board[origin_x][origin_y-1]=None
        if origin_x+2==destination_x and destination_y==origin_y:
            new_board[origin_x+1][origin_y]=None
        if origin_x-2==destination_x and destination_y==origin_y:
            new_board[origin_x-1][origin_y]=None
        return new_board

    def clone(self,tab):
        copy=[]
        for item in tab:
            temp=[]
            for i in item:
                temp.append(i)
            copy.append(temp)
        return copy

    def _can_eat(self,board,player_number):
        moves=list()
        opponent_color=TILES_COLOR[(player_number+1)%2].lower()
        for piece in self.get_movable_pieces_by_player(board,player_number):
            i, j = piece
            if  self.get_no_empty_cell_color(board, (i,j+1)) == opponent_color:
                if self.is_empty_cell(board, (i, j + 2)):               
                    actions=list()
                    actions.append(piece)
                    actions.append((i, j + 2))
                    moves.append(actions)
                            
            if  self.get_no_empty_cell_color(board, (i,j-1)) == opponent_color:
                if self.is_empty_cell(board, (i, j - 2)):
                    actions=list()
                    actions.append(piece)
                    actions.append((i, j - 2))
                    moves.append(actions)
                           
            if  self.get_no_empty_cell_color(board, (i+1,j)) == opponent_color:
                if self.is_empty_cell(board, (i + 2, j)):
                    actions=list()
                    actions.append(piece)
                    actions.append((i + 2, j))
                    moves.append(actions)
                            
            if self.get_no_empty_cell_color(board, (i-1,j)) == opponent_color:
                if self.is_empty_cell(board, (i - 2, j)):
                    actions=list()
                    actions.append(piece)
                    actions.append((i - 2, j))
                    moves.append(actions)
        return moves

    def _successors(self,board, is_me,new_piece,wantTomove=None,im_i_win=None):

        eat_list=list()
        player_number=self.player_number if is_me else (self.player_number+1)%2
        possibles_actions=dict()
        successors_pairs_list=list()
        pieces_in_hand=self.my_piece_in_hand-new_piece if is_me else self.opponent_piece_in_hand-new_piece
        if wantTomove==True:
            if im_i_win==True :
                eat_list=self._can_eat(board,player_number)
                if len(eat_list) > 0:
                    for eatable in eat_list:
                        successors_pairs_list.append((eatable,self._apply_action_pieces(eatable ,board,player_number),new_piece))
                shuffle(successors_pairs_list)
                return successors_pairs_list

            elif im_i_win==False :
                opponent_eat=list()
                opponent_eat=self._can_eat(board,(player_number+1)%2)
                opponent_eat_list=list()
                if len(opponent_eat)>0:
                    for piece in opponent_eat:
                        origin_x,origin_y=piece[0]
                        destination_x,destination_y=piece[1]
                        if origin_x==destination_x and destination_y==origin_y+2:
                            opponent_eat_list.append((origin_x,origin_y+1))
                        if origin_x==destination_x and destination_y==origin_y-2:
                            opponent_eat_list.append((origin_x,origin_y-1))
                        if origin_x+2==destination_x and destination_y==origin_y:
                            opponent_eat_list.append((origin_x+1,origin_y))
                        if origin_x-2==destination_x and destination_y==origin_y:
                            opponent_eat_list.append((origin_x-1,origin_y))
                    liste=list()
                    good_liste=list()
                        
                    for piece in opponent_eat_list:
                        for destination in self.get_piece_actual_moves(board,piece,player_number):
                            good_liste=self._get_best_move_put(board,player_number,[[piece,destination]],True)
                            for action in good_liste:
                                liste.append(action)
                    if len(liste)>0:

                        for elem in liste:
                            successors_pairs_list.append((elem,self._apply_action_pieces(elem,board,player_number),new_piece))
                        shuffle(successors_pairs_list)
                        return successors_pairs_list
                    else:
                        liste=[]
                        for piece in opponent_eat:
                            x,y=piece[1]
                        
                            if self.get_no_empty_cell_color(board,(x-1,y))==TILES_COLOR[player_number]:
                                actions=list()
                                actions.append((x-1,y))
                                actions.append((x,y))
                                liste.append(actions)
                            if self.get_no_empty_cell_color(board,(x+1,y))==TILES_COLOR[player_number]:
                                actions=list()
                                actions.append((x+1,y))
                                actions.append((x,y))
                                liste.append(actions)
                            if self.get_no_empty_cell_color(board,(x,y-1))==TILES_COLOR[player_number]:
                                actions=list()
                                actions.append((x,y-1))
                                actions.append((x,y))
                                liste.append(actions)
                            if self.get_no_empty_cell_color(board,(x,y+1))==TILES_COLOR[player_number]:
                                actions=list()
                                actions.append((x,y+1))
                                actions.append((x,y))
                                liste.append(actions)
                            if pieces_in_hand>0:
                                if len(self._get_best_empty_put(board,player_number,[piece[1]],True))>0:
                                    successors_pairs_list.append((piece[1],self._apply_action_empty(piece[1],board,player_number),new_piece+1))
                        if len(liste)>0:
                            for elem in self._get_best_move_put(board,player_number,liste,True):
                                successors_pairs_list.append((elem,self._apply_action_pieces(elem,board,player_number),new_piece))
                            
                        if len(successors_pairs_list)>0:
                            shuffle(successors_pairs_list)
                            return successors_pairs_list

                        else:
                            for elem in opponent_eat_list:
                                for action in self.get_piece_actual_moves(board,elem,player_number):
                                    actions=list()
                                    actions.append(elem)
                                    actions.append(action)
                                    successors_pairs_list.append((actions,self._apply_action_pieces(actions,board,player_number),new_piece))
                            shuffle(successors_pairs_list)
                            return successors_pairs_list

            else: 
                best_list=self._get_best_move_situation(board,player_number,self.get_movable_pieces_by_player(board,player_number))
                if len(best_list)>0:
                    for action in best_list:
                        successors_pairs_list.append((action,self._apply_action_pieces(action ,board,player_number),new_piece))
                    shuffle(successors_pairs_list)
                    return successors_pairs_list

                successors_pairs_list=self._get_all_best_moves_successors(board,player_number,new_piece)

                if len(successors_pairs_list)==0:
                    successors_pairs_list=self._get_all_moves_successors(board,player_number,new_piece)
                shuffle(successors_pairs_list)

                return successors_pairs_list
            
        elif wantTomove==False:
            liste=self.get_empty_cells(board)
            action_list=self._get_best_empty_put(board,player_number,liste,False)
            best_list=self._get_best_situation(board,player_number,action_list)

            if len(best_list)>0:
                for action in best_list:
                    successors_pairs_list.append((action,self._apply_action_empty(action,board,player_number),new_piece+1))
                shuffle(successors_pairs_list)
                return successors_pairs_list

            elif len (action_list)>0:
                for action in action_list:
                    successors_pairs_list.append((action,self._apply_action_empty(action,board,player_number),new_piece+1))
                shuffle(successors_pairs_list)
                return successors_pairs_list
                
            else:
                for elem in liste:
                    successors_pairs_list.append((elem,self._apply_action_empty(elem,board,player_number),new_piece+1))
                shuffle(successors_pairs_list)
                return successors_pairs_list
            
        else:
            if pieces_in_hand<=0:
                    successors_pairs_list=self._get_all_best_moves_successors(board,player_number,new_piece)
                    if len(successors_pairs_list)==0:
                        successors_pairs_list=self._get_all_moves_successors(board,player_number,new_piece)
            else:
                successors_pairs_list=self._get_all_best_successors(board,player_number,new_piece)
                if len(successors_pairs_list)==0:
                    successors_pairs_list=self._get_all_successors(board,player_number,new_piece)
        shuffle(successors_pairs_list)

        return successors_pairs_list
    
    def _get_best_move_situation(self,board,player_number,liste):
        my_color=TILES_COLOR[player_number].lower()
        opponent_color=TILES_COLOR[(player_number+1)%2].lower()
        situation_list=list()
        for elem in liste:
            for destination in self.get_piece_actual_moves(board,elem,player_number):
                good_liste=self._get_best_move_put(board,player_number, [[elem,destination]] ,False)
                for action in good_liste:
                    good=False
                    i,j=action[1]
                    
                    if self.get_no_empty_cell_color(board,(i,j+1))==opponent_color and  self.get_no_empty_cell_color(board,(i,j-1))==opponent_color:
                        if self.is_empty_cell(board,(i+1,j)) or self.is_empty_cell(board,(i-1,j)):
                            good=True
                        elif not(self.is_place_on_board((i+1,j))) or not(self.is_place_on_board((i-1,j))):
                            good=True
                    if self.get_no_empty_cell_color(board,(i+1,j))==opponent_color and  self.get_no_empty_cell_color(board,(i-1,j))==opponent_color:
                        if self.is_empty_cell(board,(i,j+1)) or self.is_empty_cell(board,(i,j-1)):
                            good=True
                        elif not(self.is_place_on_board((i,j+1))) or not(self.is_place_on_board((i,j-1))):
                            good=True
                    if good==True: 
                        situation_list.append(action)
        return situation_list

    def _get_best_situation(self,board,player_number,empty_list):
        my_color=TILES_COLOR[player_number].lower()
        opponent_color=TILES_COLOR[(player_number+1)%2].lower()
        situation_list=list()
        x=len(board)-1
        y=len(board[0])-1
        matrixb=set([(0,1),(0,2),(0,3),(0,4)]) & set(empty_list)
        matrixg=set([(1,0),(2,0),(3,0)]) & set(empty_list)
        matrixh=set([(x,1),(x,2),(x,3),(x,4)]) & set(empty_list)
        matrixd=set([(1,y),(2,y),(3,y)]) & set(empty_list)
        for elem in empty_list:
            good=False
            second=False
            i,j=elem
            if not self.is_empty_cell(board,(i,j+1)) and not self.is_empty_cell(board,(i,j-1)) and  self.get_no_empty_cell_color(board,(i,j+1))==opponent_color and  self.get_no_empty_cell_color(board,(i,j-1))==opponent_color:
                if self.is_empty_cell(board,(i+1,j)) and self.is_empty_cell(board,(i-1,j)):
                    good=True
            if not self.is_empty_cell(board,(i+1,j)) and not self.is_empty_cell(board,(i-1,j)) and  self.get_no_empty_cell_color(board,(i+1,j))==opponent_color and  self.get_no_empty_cell_color(board,(i-1,j))==opponent_color:
                if self.is_empty_cell(board,(i,j+1)) and self.is_empty_cell(board,(i,j-1)):
                    good=True
            if good==True: 
                situation_list.append(elem)
        if self.is_empty_cell(board,(0,0)) and (self.get_no_empty_cell_color(board,(0,1))==opponent_color or self.get_no_empty_cell_color(board,(1,0))==opponent_color):
            situation_list.append((0,0))
        if self.is_empty_cell(board,(0,len(board[0])-1)) and (self.get_no_empty_cell_color(board,(0,len(board[0])-2))==opponent_color or self.get_no_empty_cell_color(board,(1,len(board[0])-1))==opponent_color):
            situation_list.append((0,len(board[0])-1))
        if self.is_empty_cell(board,(len(board)-1,0)) and (self.get_no_empty_cell_color(board,(len(board)-2,0))==opponent_color or self.get_no_empty_cell_color(board,(len(board)-1,1))==opponent_color):
            situation_list.append((len(board)-1,0))
        if self.is_empty_cell(board,(len(board)-1,len(board[0])-1)) and (self.get_no_empty_cell_color(board,(len(board)-2,len(board[0])-1))==opponent_color or self.get_no_empty_cell_color(board,(len(board)-1,len(board[0])-2))==opponent_color):
            situation_list.append((len(board)-1,len(board[0])-1))
        for elem in matrixb:
            x,y=elem
            if len(self._get_best_empty_put(board,player_number,[elem],False))>0 and self.get_no_empty_cell_color(board,(x+1,y))==opponent_color:
                situation_list.append(elem)
        for elem in matrixh:
            x,y=elem
            if len(self._get_best_empty_put(board,player_number,[elem],False))>0 and self.get_no_empty_cell_color(board,(x-1,y))==opponent_color:
                situation_list.append(elem)

        for elem in matrixd:
            x,y=elem
            if len(self._get_best_empty_put(board,player_number,[elem],False))>0 and self.get_no_empty_cell_color(board,(x,y-1))==opponent_color:
                situation_list.append(elem)
        for elem in matrixg:
            x,y=elem
            if len(self._get_best_empty_put(board,player_number,[elem],False))>0 and self.get_no_empty_cell_color(board,(x,y+1))==opponent_color:
                situation_list.append(elem)

        return situation_list


    def _get_best_move_put(self,board,player_number,liste,can_eat_me):
        my_color=TILES_COLOR[(player_number)].lower()
        opponent_color=TILES_COLOR[(player_number+1)%2].lower()
        action_list=list()
        for action in liste:
            origin_x,origin_y=action[0]
            i,j=action[1]
            danger=False

            if self.get_no_empty_cell_color(board,(i,j+1)) == opponent_color:
                if self.is_empty_cell(board,(i,j-1)) or action[0]==(i,j-1):
                    danger=True
            if  self.get_no_empty_cell_color(board,(i,j-1)) == opponent_color:
                if self.is_empty_cell(board,(i,j+1)) or action[0]==(i,j+1):
                    danger=True
            if self.get_no_empty_cell_color(board,(i+1,j)) == opponent_color:
                if self.is_empty_cell(board,(i-1,j)) or action[0]==(i-1,j):
                    danger=True
            if  self.get_no_empty_cell_color(board,(i-1,j)) == opponent_color:
                if self.is_empty_cell(board,(i+1,j)) or action[0]==(i+1,j):
                    danger=True
           
            if  can_eat_me==False:
                if self.get_no_empty_cell_color(board,(i+2,j))==my_color or self.get_no_empty_cell_color(board,(i-2,j))==my_color or self.get_no_empty_cell_color(board,(i,j+2))==my_color or self.get_no_empty_cell_color(board,(i,j-2))==my_color:
                    danger=True
            if  self.get_no_empty_cell_color(board,(i,j + 1)) == opponent_color and self.get_no_empty_cell_color(
                board, (i, j - 1)) == opponent_color:
                if not(self.is_empty_cell(board, (i + 1, j)) or self.is_empty_cell(board, (i - 1, j))):
                    danger = True
            if self.get_no_empty_cell_color(board,(i + 1, j)) == opponent_color and self.get_no_empty_cell_color(
                board, (i - 1, j)) == opponent_color:
                if not(self.is_empty_cell(board, (i, j + 1)) or self.is_empty_cell(board, (i, j - 1))):
                    danger = True
            if i==0 and (j==0 or j==len(board[0])-1):
                danger=False
            if i==len(board)-1 and (j==0 or j==len(board[0])-1):
                danger=False

            if danger==False:
                action_list.append(action)

        return action_list


 
    def _get_best_empty_put(self,board,player_number,liste,can_eat_me):
        my_color=TILES_COLOR[(player_number)].lower()
        opponent_color=TILES_COLOR[(player_number+1)%2].lower()
        action_list=list()
        for action in liste:
            i,j=action
            danger=False
            if self.get_no_empty_cell_color(board,(i,j+1)) == opponent_color:
                if self.is_empty_cell(board,(i,j-1)) :
                    danger=True
            if  self.get_no_empty_cell_color(board,(i,j-1)) == opponent_color:
                if self.is_empty_cell(board,(i,j+1)) :
                    danger=True
            if self.get_no_empty_cell_color(board,(i+1,j)) == opponent_color:
                if self.is_empty_cell(board,(i-1,j)) :
                    danger=True
            if  self.get_no_empty_cell_color(board,(i-1,j)) == opponent_color:
                if self.is_empty_cell(board,(i+1,j)) :
                    danger=True
           
            if  can_eat_me==False:
                if self.get_no_empty_cell_color(board,(i+2,j))==my_color or self.get_no_empty_cell_color(board,(i-2,j))==my_color or self.get_no_empty_cell_color(board,(i,j+2))==my_color or self.get_no_empty_cell_color(board,(i,j-2))==my_color:
                    danger=True
            if  self.get_no_empty_cell_color(board,(i,j + 1)) == opponent_color and self.get_no_empty_cell_color(
                board, (i, j - 1)) == opponent_color:
                if not(self.is_empty_cell(board, (i + 1, j)) and self.is_empty_cell(board, (i - 1, j))):
                    danger = True
            if self.get_no_empty_cell_color(board,(i + 1, j)) == opponent_color and self.get_no_empty_cell_color(
                board, (i - 1, j)) == opponent_color:
                if not(self.is_empty_cell(board, (i, j + 1)) and self.is_empty_cell(board, (i, j - 1))):
                    danger = True
            if i==0 and (j==0 or j==len(board[0])-1):
                danger=False
            if i==len(board)-1 and (j==0 or j==len(board[0])-1):
                danger=False

            if danger==False:
                action_list.append(action)

        return action_list

    def _get_all_best_successors(self,board,player_number,new_piece):
        successors_pairs_list=list()
        action_list=list()
        situation_list=list()

        for piece in self.get_movable_pieces_by_player(board,player_number):
            for destination in self.get_piece_actual_moves(board,piece,player_number):

                good_liste=self._get_best_move_put(board,player_number, [[piece,destination]] ,False)
                for action in good_liste:
                    successors_pairs_list.append((action,self._apply_action_pieces(action,board,player_number),new_piece))

        liste=self.get_empty_cells(board)
        action_list=self._get_best_empty_put(board,player_number,liste,False)
        if len (action_list)>0:
            for action in action_list:
                successors_pairs_list.append((action,self._apply_action_empty(action,board,player_number),new_piece+1))
        return successors_pairs_list

    def _get_all_best_moves_successors(self,board,player_number,new_piece):
        successors_pairs_list=list()
        for piece in self.get_movable_pieces_by_player(board,player_number):
            for destination in self.get_piece_actual_moves(board,piece,player_number):
                good_liste=self._get_best_move_put(board,player_number, [[piece,destination]] ,False)
                for action in good_liste:
                    successors_pairs_list.append((action,self._apply_action_pieces(action,board,player_number),new_piece))

            if len(successors_pairs_list)==0:
                for destination in self.get_piece_actual_moves(board,piece,player_number):
                    good_liste=self._get_best_move_put(board,player_number, [[piece,destination]] ,True)
                    for action in good_liste:
                        successors_pairs_list.append((action,self._apply_action_pieces(action,board,player_number),new_piece))

        return successors_pairs_list

    def _get_all_successors(self,board,player_number,new_piece):
        successors_pairs_list=list()
        liste=self.get_all_possibles_moves(board,player_number)
        for playable in liste['pieces']:
            for action in self.get_piece_actual_moves(board, playable, player_number):
                actions=list()
                actions.append(playable)
                actions.append(action)
                successors_pairs_list.append((actions,self._apply_action_pieces(actions,board,player_number),new_piece))
        for piece in liste['empty_cells']:
            successors_pairs_list.append((action,self._apply_action_empty(action,board,player_number),new_piece+1))
        return successors_pairs_list

    def _get_all_moves_successors(self,board,player_number,new_piece):
        successors_pairs_list=list()
        for playable in self.get_movable_pieces_by_player(board,player_number):
            for action in self.get_piece_actual_moves(board, playable, player_number):
                actions=list()
                actions.append(playable)
                actions.append(action)
                successors_pairs_list.append((actions,self._apply_action_pieces(actions,board,player_number),new_piece))
        return successors_pairs_list

    def _get_all_move_list(self, board,player_number):
        liste=list()
        for elem in self.get_all_possibles_moves(board, player_number)["pieces"]:
            for destination in self.get_piece_actual_moves(board, elem, player_number):
                liste.append([elem,destination])
        return liste

    def _get_want_to_move(self, board, is_me,new_piece):
       
        if is_me:
            player_number=self.player_number 
            opponent_number=(self.player_number+1)%2
            pieces_in_hand=self.my_piece_in_hand-new_piece
            my_piece_on_board=len(self._my_piece_on_board(board))
        else:
            player_number=(self.player_number+1)%2 
            opponent_number=self.player_number 
            pieces_in_hand=self.opponent_piece_in_hand-new_piece
            my_piece_on_board=len(self._opponent_piece_on_board(board))

        if (len(self.get_movable_pieces_by_player(board, player_number)) == 0):
            if pieces_in_hand >0:
                return [False]
            else:
                return [False]
            
        else:
            opponent_eat = list()
            my_eatable = list()
            opponent_eat = self._can_eat(board, opponent_number)
            my_eatable = self._can_eat(board, player_number)

            if len(my_eatable)>0:
                return [True,True]
            elif len(opponent_eat)>0 :
                return [True,False]

            else:
                put=len(self._get_best_empty_put(board, player_number, self.get_empty_cells(board),False))
                if  pieces_in_hand > 0 and my_piece_on_board < 5 and put > 0:
                    return [False]
                    
                elif len(self._get_best_move_put(board, player_number, self._get_all_move_list(board,player_number),False)) > 0:
                    if pieces_in_hand>0 and put>0:
                        a = [True,True,False,True, False,True,True,True,True,False]
                        shuffle(a)
                        a = choice(a)
                        return [a]
                    else:
                        return [True]

                else:
                    if pieces_in_hand > 0:
                            a = [True, False]
                            shuffle(a)
                            a = choice(a)
                            return [a]
                    else:
                        return [True]

    def _get_best_action(self,board,nbr):
            
            inf = float("inf")
        
            def max_value(board, alpha, beta, depth, new_piece):
                if self._cutoff(board, depth, nbr):
                    evaluation=self._evaluate(board,True,new_piece)
                    return evaluation, None

                move_return=self._get_want_to_move(board,True,new_piece)
                successors_pairs_list=list()
                if len(move_return)==1:
                    successors_pairs_list=self._successors(board,True,new_piece,move_return[0])
                elif len(move_return)==2:
                    successors_pairs_list=self._successors(board,True,new_piece,move_return[0],move_return[1])
                if successors_pairs_list==[]:
                    return min_value(board, alpha, beta, depth+1,new_piece)
                else:
                    val = -inf
                    action = None
                    for a, b, c in successors_pairs_list:
                        v, _ = min_value(b, alpha, beta, depth + 1, c)
                        if v > val:
                            val = v
                            action = a
                            if v >= beta:
                                return v, a
                            alpha = max(alpha, v)
                    return val, action
        
            def min_value(board, alpha, beta, depth, new_piece):
                if self._cutoff(board, depth, nbr):
                    evaluation=self._evaluate(board, False, new_piece)
                    return evaluation, None
                move_return=self._get_want_to_move(board,False,new_piece)
                successors_pairs_list=list()
                if len(move_return)==1:
                    successors_pairs_list=self._successors(board,False,new_piece,move_return[0])
                elif len(move_return)==2:
                    successors_pairs_list=self._successors(board,False,new_piece,move_return[0],move_return[1])
                    
                if successors_pairs_list==[]:
                    return max_value(board, alpha, beta, depth+1,new_piece)
                else:
                    val = inf
                    action = None
                    for a, b, c in successors_pairs_list:
                        v, _ = max_value(b, alpha, beta, depth + 1, c)
                        if v < val:
                            val = v
                            action = a
                            if v <= alpha:
                                return v, a
                            beta = min(beta, v)
                    return val, action
                    
            _, action = max_value(board, -inf, inf, 0, 0)
            return action

    def _good_steal(self,board,player_number):
        moves=list()
        opponent_color=TILES_COLOR[(player_number+1)%2].lower()
        for piece in self.get_playable_pieces(board,player_number):
            i, j = piece
            if self.get_no_empty_cell_color(board, (i, j + 2)) == opponent_color:
                if  self.get_no_empty_cell_color(board, (i,j+1)) == opponent_color:
                    moves.append((i, j + 2))
                            
            if self.get_no_empty_cell_color(board, (i, j - 2)) == opponent_color:
                if  self.get_no_empty_cell_color(board, (i,j-1)) == opponent_color:
                    moves.append((i, j - 2))
                           
            if self.get_no_empty_cell_color(board, (i + 2, j)) == opponent_color:
                if  self.get_no_empty_cell_color(board, (i+1,j)) == opponent_color:
                    moves.append((i + 2, j))
                            
            if self.get_no_empty_cell_color(board, (i - 2, j)) == opponent_color:
                if self.get_no_empty_cell_color(board, (i-1,j)) == opponent_color:
                    moves.append((i - 2, j))
        return moves
    
    def _get_quatre_bords(self,board,player_number):
        opponent_color=TILES_COLOR[(player_number+1)%2].lower()
        a=len(board)-1
        b=len(board[0])-1
        liste=[(0,0),(0,b),(a,0),(a,b)]
        good=[]
        for elem in liste:
            i,j=elem
            if board[i][j]==opponent_color:
                good.append(elem)
        return good
    
    def _get_autre_bords(self,board,player_number):
        opponent_color=TILES_COLOR[(player_number+1)%2].lower()
        a=len(board)-1
        b=len(board[0])-1
        good=[]
        for j in [0,b]:
            for i in range(a+1):
                if board[i][j]==opponent_color:
                    good.append((i,j))
        for i in [0,a]:
            for j in range(b+1):
                if board[i][j]==opponent_color:
                    good.append((i,j))
        return good
    
    @timeout(seconds=0.1)
    def play(self, depth_to_cover, board, can_steal):
        self.my_preview_piece_on_board=len(self._my_piece_on_board(board))
        self.my_piece_in_hand=self.player_pieces_in_hand
        self.opponent_preview_piece_on_board=len(self._opponent_piece_on_board(board))
        self.opponent_piece_in_hand=12-self.captured_pieces-self.opponent_preview_piece_on_board
        
        if can_steal:
            opponent_eat=self._can_eat(board,(self.player_number+1)%2)
            opponent_eat_list=list()
            good_steal=self._good_steal(board,self.player_number)
            quatre_bords=self._get_quatre_bords(board,self.player_number)
            autre_bords=self._get_autre_bords(board,self.player_number)
            if len(opponent_eat)>0:
                for piece in opponent_eat:
                    opponent_eat_list.append(piece[0])
                return opponent_eat_list[random.randint(0,len(opponent_eat_list)-1)]
            elif len(good_steal)>0:
                opponent_eat_list=good_steal
                return opponent_eat_list[random.randint(0,len(opponent_eat_list)-1)]
            elif len(quatre_bords)>0 :
                return quatre_bords[random.randint(0,len(quatre_bords)-1)]
            elif len(autre_bords)>0 :
                return autre_bords[random.randint(0,len(autre_bords)-1)]
            else:
                return-1,-1


        else:
            sm=self._get_best_action(board,0)
            
            if type(sm) is  list:
                origin=list(sm[0])
                destination=list(sm[1])
                return (origin[0],origin[1],destination[0],destination[1])
            
            elif type(sm) is tuple:
                if self.player_pieces_in_hand==0:
                    liste = list()
                    for playable in self.get_movable_pieces_by_player(board,self.player_number):
                        for action in self.get_piece_actual_moves(board, playable, self.player_number):
                            actions=list()
                            actions.append(playable)
                            actions.append(action)
                            liste.append(actions)
                    shuffle(liste)
                    sm=liste[randint(0, len(liste)-1)]
                    origin=list(sm[0])
                    destination=list(sm[1])
                    return (origin[0],origin[1],destination[0],destination[1])

                else:
                    return (sm[0],sm[1])