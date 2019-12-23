# -*- coding: utf-8 -*-
import random
from util import timeout
from player import Player
TILES_COLOR = ["black", "green"]
from copy import deepcopy
import math
from util import timeout

class AI(Player):
 
    # Team modify this
    name = "Zinzeg Team"

    def __init__(self, player_number, board_size):
        Player.__init__(self, player_number, board_size)
 
    def get_player_score(self):
        return self.captured_pieces

    def get_player_name(self):
        return self.name
 
    depth=9
    
    # fin du jeu dans le deroulement de minmax 
    def is_game_over(self ,board, data):
        ai_captured_pieces=data[0]
        ai_pieces_in_hand=data[1]
        adv_captured_pieces=data[2]
        adv_pieces_in_hand=data[3]
        #steal_on=data[4]
        if ((adv_pieces_in_hand == 0 and self.isPlayerStuck(board,(self.player_number+1)%2)) or ai_captured_pieces == 12):
            return True
        elif ((ai_pieces_in_hand == 0 and self.isPlayerStuck(board, self.player_number)) or adv_captured_pieces == 12):
            return True
        return False
    
    def isPlayerStuck(self, board, player_number):
        if len(self.get_movable_pieces_by_player(board,player_number)) == 0:
            return True
        else:
            return False
  
    # fonction d'evalution qui retourne une valeur : plus la valeur est grande plus IA a la chance de gagner
    def evaluation_function(self, board, player_number, data):
        """
        Returns: the value of evaluation
        """
        ai_captured_pieces=data[0]
        ai_pieces_in_hand=data[1]
        adv_captured_pieces=data[2]
        adv_pieces_in_hand=data[3]
        steal_on=data[4]
        if self.is_game_over(board, data):
            
            if (adv_pieces_in_hand == 0 and self.isPlayerStuck(board, (self.player_number+1)%2) or ai_captured_pieces == 12):
        #        print("Evaluation returns : 200\n")
                return 200 
            elif (ai_pieces_in_hand == 0 and self.isPlayerStuck(board, self.player_number) or adv_captured_pieces == 12):
        #        print("Evaluation returns : -200\n")
                return -200            
            return 0
        adv_dangerous_piece=0
        ai_dangerous_piece=0
        adv_dangerous_piece = len(self.get_eater_pieces(board, (self.player_number+1)%2))
        ai_dangerous_piece = len(self.get_eater_pieces(board, self.player_number))
        
        if self.player_number!=player_number :
            return ai_captured_pieces - adv_captured_pieces+0.14*ai_dangerous_piece-0.3*adv_dangerous_piece
        else:
            return ai_captured_pieces - adv_captured_pieces+0.3*ai_dangerous_piece-0.14*adv_dangerous_piece
        #print("Evaluation returns : {}\n".format(ai_captured_pieces - adv_captured_pieces))
        

    def get_piece_to_steal_by_player(self, board, player_number, data):
        ai_captured_pieces=data[0]
        ai_pieces_in_hand=data[1]
        adv_captured_pieces=data[2]
        adv_pieces_in_hand=data[3]
        #steal_on=data[4]
        liste_actions=[]
        liste_actions=self.get_eater_pieces(board,(player_number+1)%2)
        if len(liste_actions)!=0:
            return [liste_actions[random.randint(0,len(liste_actions)-1)]]
        elif self.player_number==player_number :                
            if (adv_pieces_in_hand) > 0:
                return [(-1,-1)]
        elif self.player_number!=player_number :                
            if (ai_pieces_in_hand) > 0:
                return [(-1,-1)]
        return liste_actions
    
    def get_eater_pieces(self, board, player_number):
        real_moves=[]
        pieces_movable=self.get_movable_pieces_by_player(board,player_number)
        if len(pieces_movable) != 0 :
            for piece in pieces_movable:
                next_cells=self.get_piece_actual_moves(board,piece,player_number)
                for next_cell in next_cells:
                    if math.sqrt(math.pow(next_cell[0]-piece[0],2)+math.pow(next_cell[1]-piece[1],2))!=1:
                        if piece[0]==next_cell[0]:
                            if piece[1]-next_cell[1] > 0:
                                if board[piece[0]][piece[1]-1]==TILES_COLOR[(player_number+1)%2] :
                                    real_moves.append(piece)
                                    break
                            else:
                                if board[piece[0]][piece[1]+1]==TILES_COLOR[(player_number+1)%2] :
                                    real_moves.append(piece)
                                    break
                        else:
                            if piece[0]-next_cell[0] > 0:
                                if board[piece[0]-1][piece[1]]==TILES_COLOR[(player_number+1)%2] :
                                    real_moves.append(piece)
                                    break
                            else:
                                if board[piece[0]+1][piece[1]]==TILES_COLOR[(player_number+1)%2] :
                                    real_moves.append(piece)
                                    break                      
        return real_moves
    
    def get_possible_actions(self,board, player_number, data): 
        ai_captured_pieces=data[0]
        ai_pieces_in_hand=data[1]
        adv_captured_pieces=data[2]
        adv_pieces_in_hand=data[3]
        steal_on=data[4] 

        ai_piece_in_board=0
        for i in board:
            ai_piece_in_board+=i.count(TILES_COLOR[self.player_number])
            
        liste_actions=list()
        if not steal_on:
            possible_moves=self.get_all_possibles_moves(board, player_number)["pieces"]
            for piece_cell in possible_moves:
                liste_depl=self.get_piece_actual_moves(board,piece_cell,player_number)
                depls=[]
                for next_cell in liste_depl:
                    if math.sqrt(math.pow(next_cell[0]-piece_cell[0],2)+math.pow(next_cell[1]-piece_cell[1],2))!=1:
                        if piece_cell[0]==next_cell[0]:
                            if piece_cell[1]-next_cell[1] > 0:
                                if board[piece_cell[0]][piece_cell[1]-1]==TILES_COLOR[(player_number+1)%2] :
                                    depls.append((piece_cell[0],piece_cell[1],next_cell[0],next_cell[1]))
                            else:
                                if board[piece_cell[0]][piece_cell[1]+1]==TILES_COLOR[(player_number+1)%2] :
                                    depls.append((piece_cell[0],piece_cell[1],next_cell[0],next_cell[1]))
                        else:
                            if piece_cell[0]-next_cell[0] > 0:
                                if board[piece_cell[0]-1][piece_cell[1]]==TILES_COLOR[(player_number+1)%2] :
                                    depls.append((piece_cell[0],piece_cell[1],next_cell[0],next_cell[1]))
                            else:
                                if board[piece_cell[0]+1][piece_cell[1]]==TILES_COLOR[(player_number+1)%2] :
                                    depls.append((piece_cell[0],piece_cell[1],next_cell[0],next_cell[1]))
                    else:
                        depls.append((piece_cell[0],piece_cell[1],next_cell[0],next_cell[1]))
                liste_actions+=depls
                
            #if ai_piece_in_board < 6 :
            random.shuffle(liste_actions) 
                
            possible_moves=[]    
            if self.player_number== player_number and ai_pieces_in_hand > 0 :
                liste_actions+=self.get_all_possibles_moves(board, player_number)["empty_cells"]
            if self.player_number!= player_number and adv_pieces_in_hand > 0 :
                liste_actions+=self.get_all_possibles_moves(board, player_number)["empty_cells"]
        else:
            liste_actions=self.get_piece_to_steal_by_player(board,player_number, data)
            if len(liste_actions)==0:
                liste_actions+=self.get_playable_pieces(board,(player_number+1)%2)
            return liste_actions
        if len(liste_actions)==0:
            liste_actions+=self.get_playable_pieces(board,player_number)
        if ai_piece_in_board < 6 :
            random.shuffle(liste_actions)
        return liste_actions
    
    def add_piece(self,board,cell,player_number):
        board[cell[0]][cell[1]]=TILES_COLOR[player_number]
    
    def remove_piece(self,board,cell):
        board[cell[0]][cell[1]]=None
    
    def jouer(self, instruction, board, player_number, data):
        board = deepcopy(board)
        color = TILES_COLOR[player_number]
        ai_captured_pieces=data[0]
        ai_pieces_in_hand=data[1]
        adv_captured_pieces=data[2]
        adv_pieces_in_hand=data[3]
        steal_on=data[4]
        player_number=player_number
        
        if len(instruction)==2:
            if(instruction[0]==instruction[1]==-1):
                if self.player_number==player_number :
                    adv_pieces_in_hand-=1
                    ai_captured_pieces+=1
                else :
                    ai_pieces_in_hand-=1
                    adv_captured_pieces+=1
                steal_on=False
                player_number=(player_number+1)%2
            elif(steal_on and not self.is_empty_cell(board,(instruction[0],instruction[1])) and board[instruction[0]][instruction[1]] != color):     
                self.remove_piece(board,(instruction[0],instruction[1]))
                if self.player_number==player_number :
                    ai_captured_pieces+=1
                else :
                    adv_captured_pieces+=1
                steal_on=False
                player_number=(player_number+1)%2
            elif self.is_empty_cell(board,(instruction[0],instruction[1])):
                self.add_piece(board, (instruction[0],instruction[1]), player_number)
                if self.player_number==player_number :
                    ai_pieces_in_hand-=1
                else :
                    adv_pieces_in_hand-=1
                player_number=(player_number+1)%2
        elif(len(instruction)==4):
            if (math.sqrt(math.pow(instruction[2]-instruction[0],2)+math.pow(instruction[3]-instruction[1],2))==1):
                self.remove_piece(board,(instruction[0],instruction[1]))
                self.add_piece(board,(instruction[2],instruction[3]),player_number)
                player_number=(player_number+1)%2
            else:        
                self.remove_piece(board,(instruction[0],instruction[1]))
                self.add_piece(board,(instruction[2],instruction[3]),player_number)
                if(instruction[0]==instruction[2]):
                    if instruction[1]-instruction[3] > 0:
                        self.remove_piece(board,(instruction[0],instruction[1]-1))
                    else:
                        self.remove_piece(board,(instruction[0],instruction[1]+1))
                    steal_on=True
                else:
                    if instruction[0]-instruction[2] >0:
                        self.remove_piece(board,(instruction[0]-1,instruction[1]))
                    else:
                        self.remove_piece(board,(instruction[0]+1,instruction[1]))
                    steal_on=True
                if self.player_number==player_number :
                    ai_captured_pieces+=1
                else :
                    adv_captured_pieces+=1
      
        return board, player_number, [ai_captured_pieces,ai_pieces_in_hand,adv_captured_pieces,adv_pieces_in_hand,steal_on]
    
    def maximum(self,board, depth, A, B, player_number, data):
        output = [None, -float("inf")]
        actions_list = self.get_possible_actions(board, player_number, data)
        if len(actions_list)==0 :
            return [None, self.evaluation_function(board, player_number, data)] # laisser pour pars
        tampon_board=[]
        tampon_player_number=int()
        tampon_data=[]
        tampon_board=deepcopy(board)
        tampon_player_number=player_number
        tampon_data=deepcopy(data)
        for action in actions_list:
            #print(action)
            current_board,player_number,data = self.jouer(action, tampon_board, tampon_player_number, tampon_data)
            val = self.mini_max(current_board, depth, A, B, player_number, data)
            check = val[1]
            if check > output[1]:
                output = [action, check]
            A = max(A, check)
            if A >= B:
                return [action, check]
            
        return output
    def minimum(self,board, depth, A, B, player_number, data):
        output = [None, float("inf")]
        actions_list = self.get_possible_actions(board, player_number, data)
        if len(actions_list)==0:
            return [None, self.evaluation_function(board, player_number, data)]
        tampon_board=[]
        tampon_player_number=int()
        tampon_data=[]
        tampon_board=deepcopy(board)
        tampon_player_number=player_number
        tampon_data=deepcopy(data)
        for action in actions_list:
            #print(action)
            current_board,player_number,data = self.jouer(action, tampon_board, tampon_player_number, tampon_data)
            val = self.mini_max(current_board, depth, A, B, player_number, data)
            check = val[1]
            if check < output[1]:
                output = [action, check]
            B = min(B, check)
            if B <= A:
                return [action, check]
            
        return output
    
    def mini_max(self, board, depth, A, B, player_number, data):
        depth += 1
        if depth == self.depth or self.is_game_over(board, data) : 
            return [None, self.evaluation_function(board, player_number, data)]
        elif player_number == self.player_number :
            return self.maximum(board, depth, A, B, player_number, data)
        else :
            return self.minimum(board, depth, A, B, player_number, data)               
    
    @timeout(seconds = 0.1)
    def play(self, depth_to_cover, board, can_steal):
        adv_piece_in_board=0
        for i in board:
            adv_piece_in_board+=i.count(TILES_COLOR[(self.player_number+1)%2])
            
        ai_piece_in_board=0
        for i in board:
            ai_piece_in_board+=i.count(TILES_COLOR[self.player_number])
            
        #informations concernant les joueurs
        ai_pieces = self.player_pieces_in_hand+ai_piece_in_board
        ai_pieces_in_hand = self.player_pieces_in_hand
        ai_captured_pieces = self.captured_pieces
          
        adv_pieces = 12-self.captured_pieces
        adv_pieces_in_hand = 12-self.captured_pieces-adv_piece_in_board
        adv_captured_pieces = 12-ai_pieces 
        steal_on = can_steal 
        player_number=self.player_number 
        
        data=[ai_captured_pieces,ai_pieces_in_hand,adv_captured_pieces,adv_pieces_in_hand,steal_on]
   
        self.depth = 2
        
        #self.current_player = self.player_number
        output = self.mini_max(board, -1, -float("inf"), float("inf"), player_number, data)
        #print("output----------> {} ".format(output))
        return output[0]
