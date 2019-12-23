# -*- coding: utf-8 -*-
import random
import math
from collections import Counter
from util import timeout
from player import Player
import copy
from itertools import chain
TILES_COLOR = ["black", "green"]

class AI(Player):

    # Team modify this
    name = "GekidoLast"

    def __init__(self, player_number, board_size):
        Player.__init__(self, player_number, board_size)
        self.max_depth = 5
        self.player_color = TILES_COLOR[(self.player_number)%2].lower()


    def get_player_score(self):
        return self.captured_pieces

    def get_player_name(self):
        return self.name
    
    @timeout(seconds=0.1)
    def play(self, depth_to_cover, board, can_steal):
        board_cpy=self.clone(board)

        if can_steal:
            return self.stealable(board, self.player_number)

        #copy
        board_cpy=self.clone(board)
        #je récupère toutees les positions que je juge magique(voir la fonction pour +)
        magici=self.magicPosition(board_cpy, self.player_number)
        #trie des magici
        magici=self.sort_Tuple(magici)

        #copy
        board_cpy=self.clone(board)
        caseJouable=self.get_all_possibles_moves(board_cpy, self.player_number)["pieces"]

        #je joue simplement mes pions pour voir les gagnants
        good=list()
        for case1 in caseJouable:
            board_1=self.clone(board_cpy)

            score, ele = self.playCase(board_1, case1, self.player_number)

            if score > 0:
                good.append((case1, ele))

        
        if len(good)!=0:
            _play=good[random.randint(0, len(good)-1)]
            if self.is_place_on_board(_play[1]) and self.is_empty_cell(board, _play[1]) and _play[1] in self.get_piece_actual_moves(board, _play[0], self.player_number):
                return (_play[0][0], _play[0][1], _play[1][0],_play[1][1])


        #si rien n'est fait jusqu'à là
        before_score=self.eval(board_cpy)

        paws=self.pawsStateOnBoard(board_cpy)
        our_pieces = paws[self.player_color]
        inverse_pieces = paws[TILES_COLOR[(self.player_number+1)%2]]
        _inver=inverse_pieces+self.captured_pieces

        #alpha beta        
        score, since, to = self.ami(board_cpy, 3, -99999999999999999, 99999999999999999)

        #je vérifie si après le déplacement, l'adversaire à son tour posait un pion dans la case de "since"
        #il se retrouve dans une situation où il y a jusqu'à deux déplacements pour prendre nos pions
        _goldening=False
        if self.is_place_on_board(since) and self.is_place_on_board(to):
            _board_1=self.clone(board)
            #je pose un pion dans cette case
            _steal, _board_1=self.makeMove(_board_1, since, to)
            if _steal<=0:
                _inverse=(self.player_number+1)%2
                _board_1=self.putOnBoard(_board_1, since, TILES_COLOR[_inverse])
                _score = self.playCase(_board_1, since, _inverse)[0]

                if _score>1:
                    _goldening=True

        # si on a de pion en reserve
        # et si alpha beta ne donne rien d'interessant
        # ou on n'a plus de pion sur le board
        # ou si _goldening
        # etc...
        # on essaye de déployer un pion sur le board de façon intelligente
        _cond=(self.player_pieces_in_hand>0 and (_goldening or our_pieces==0 or len(caseJouable)==0 or (score<0 and before_score>score)))
    
        if  _cond:
            if len(magici)!=0:
                return magici[0][0]

            #parmi les positions disponible, je choisi l'idéale
            #je récupère toutes les positions vide disponible
            empty_paws=self.get_empty_cells(board_cpy)

            #pour chaque case vide, poser le pion et simuler le jeux de l'adversaire et prendre là où il gagne le moins
            if len(empty_paws)>0 and self.player_pieces_in_hand>0:
                best_score=9999999999
                best_paw=(-1,-1)
                for paw in empty_paws:
                    board_1=self.clone(board_cpy)
                    #je pose un pion dans cette case
                    board_1=self.putOnBoard(board_1, paw, self.player_color)
                        
                    #simuler le jeux de l'adversaire et prendre le minimum de tous ces meilleurs gain
                    score, since, to = self.simplePlay(board_1, (self.player_number+1)%2)
                    #print(f"score::{score} since::{since} to::{to}")
                    
                    #je prends là où il gagne le moins
                    if score<best_score:
                        best_score=score
                        best_paw=paw

                return best_paw

        if self.player_pieces_in_hand!=0 and len(magici)!=0:
            return magici[0][0]

        if (score>=before_score) or self.player_pieces_in_hand==0 or (score==0 and len(magici)==0) or (score==0 and before_score<0):
            #print(f"return score::{score} since::{since} to::{to} - {self.get_piece_actual_moves(board, since, self.player_number)}")
            if self.is_place_on_board(since) and self.is_place_on_board(to):
                return since[0], since[1], to[0], to[1]
        else:
            if len(magici)!=0:
                return magici[0][0]


        if len(magici)!=0:
                return magici[0][0]

        board_cpy=self.clone(board)
        #je déploie
        #parmi les positions disponible, je choisi l'idéale
        #je récupère toutes les positions vide disponible
        board_cpy=self.clone(board)
        empty_paws=self.get_empty_cells(board_cpy)
        #print(f"paws:{paws}")

        #pour chaque case vide, poser le pion et simuler le jeux de l'adversaire et prendre là où il gagne le moins
        if len(empty_paws)>0 and self.player_pieces_in_hand>0:
            best_score=999999999999999999
            best_paw=(-1,-1)
            for paw in empty_paws:
                board_1=self.clone(board_cpy)
                #je pose un pion dans cette case
                board_1=self.putOnBoard(board_1, paw, self.player_color)
                #simuler le jeux de l'adversaire
                score, since, to = self.simplePlay(board_1, (self.player_number+1)%2)
                #print(f"score1::{score} since::{since} to::{to}")
                #je prends là où il gagne le moins
                if score<best_score:
                    best_score=score
                    best_paw=paw
        
            return best_paw 

        temp=self.get_all_possibles_moves(board, self.player_number)["pieces"]
        #print(f"possible move:{temp}")
        playable=temp[random.randint(0, len(temp)-1)]
        #print(f"playable:{playable}")
        temp=self.get_piece_actual_moves(board, playable, self.player_number)
        #print(f"temp2:{temp}")
        playableDestination=temp[random.randint(0, len(temp)-1)]
        #print(f"playableDestination:{playableDestination}")
        return (playable[0],playable[1],playableDestination[0],playableDestination[1]) 

    # Function to sort the list by second item of tuple 
    def sort_Tuple(self, tup):  
        return(sorted(tup, key = lambda x: x[1], reverse=True)) 

    #simuler les déplacements d'un pion donné sur le board et renvoye la somme des scores des déplacement
    def playCase(self, board, case, player):
        score=0
        pawn=(-1, -1)

        real_move = self.get_piece_actual_moves(board, case, player)

        for possible_move in real_move:
            board_cpy = self.clone(board)
            steal, board_cpy=self.makeMove(board_cpy, case, possible_move)

            if steal>0:
                score+=steal
                pawn=possible_move

        return score, pawn

    #stratégie de déployement
    #permet de positionner nos pions autour de l'adversaire tout en assurant que l'adversaire ne peut pas prendre le pion lors de don tour
    def magicPosition(self, board, player):
        filtre=list()

        inverse=(player+1)%2

        #on récupère tous les pions de l'adversaire
        caseJouable = self.get_all_possibles_moves(board, inverse)["pieces"]
        #print(f"mcaseJouable : {caseJouable}")
       
        for case in caseJouable:
            real_move = self.get_piece_actual_moves(board, case, inverse)
            best_board = self.clone(board)
            best_score=-99999999999
            best_move=(-1,-1)

            a_score = self.playCase(self.clone(board), case, inverse)[0]

            #print(f"b_score1 : {case} - {a_score}")
            #pour chaque case de déplacement des pions de l'adversaire
            #je dépose mes pions dans ces cases
            #et je concerve la case pour laquelle j'ai le plus de possibilité de prendre le pion courant
            for possible_move in real_move:
                board_cpy = self.clone(board)
                
                #je dépose mon pion
                board_cpy=self.putOnBoard(board_cpy, possible_move, TILES_COLOR[player])

                b_score = max(a_score, self.playCase(self.clone(board_cpy), case, inverse)[0])

                #print(f"b_scoreN : {b_score}")

                #je joue les mouvements possible du pions
                score = self.playCase(self.clone(board_cpy), possible_move, player)[0] - b_score

                #print(f"score : {possible_move} - {score} - {best_score}")

                if score>best_score:
                    best_score=score
                    best_board=board_cpy
                    best_move=possible_move

            #print(f"best_score : {best_score}")

            #je vérifie si au préalable l'adversaire pourrait prendre mon pion avant mon tour de jeu
            #print(f"CJ : {caseJouable}")
            is_good=True
            for case1 in caseJouable:
                score = self.playCase(self.clone(best_board), case1, inverse)[0]

                if score > 0:                    
                    is_good=False
                    break
            
            #print(f"list[0] : {[ elem[0] for elem in filtre]}")
            if is_good and best_move not in [ elem[0] for elem in filtre]:
                filtre.append((best_move, best_score))

        #print(f"mfiltre : {filtre}")
        
        return filtre

            
    #filter move
    #permet d'ordonner les cases jouables de ceux qui font plus gain au moins de gain
    #afin d'améliorer la précision de Alpha Beta  
    def filterPlayable(self, board, player):
        filtre=list()
        
        caseJouable = self.get_all_possibles_moves(board, player)["pieces"]
        #print(f"case filtre:{caseJouable}")
        
        if caseJouable:
            #je trie par ce qui bouffe vite
            for case in caseJouable:
                real_move = self.get_piece_actual_moves(board, case, player)

                score=0
                for possible_move in real_move:
                    board_cpy = self.clone(board)
                
                    steal, board_cpy=self.makeMove(board_cpy, case, possible_move)
                    score+=steal
                    #print(f"filtre:{case} - {possible_move} - {steal} - {score}")

                if score>0:
                    filtre.append((case, score))

            #print(f"filtre1:{filtre}")
            filtre=(sorted(filtre, key = lambda x: x[1], reverse=True))
            #print(f"filtre2:{filtre}")
            filtre=[ elem[0] for elem in filtre]
            #print(f"filtre3:{filtre}")

            board_cpy = self.clone(board)
            va=self.player_pieces_in_hand

            cas=False
            if len(filtre)==0 and va<=0:
                cas=True
                #print(f"--filtre1:{caseJouable}")
                for case in caseJouable:
                    #print(f"filtrecase:{case}")
                    a_moves = self.get_possible_moves(case)
                    #print(f"filtrecase2:{a_moves}")
                    for a_move in a_moves:
                        if self.is_place_on_board(a_move) and not self.is_empty_cell(board_cpy, a_move):
                            if board_cpy[a_move[0]][a_move[1]]==TILES_COLOR[(player+1)%2]:
                                if case not in filtre:
                                    filtre.append(case)
                                    break

                #print(f"--filtre:{filtre}")

            _list=[ elem for elem in caseJouable if elem not in filtre]

            l=list(chain(filtre, _list))

            if cas and False:
                if len(l)>1:
                    l=self.swapList(l)

            #print(f"case end filtre:{l}")

            return l
        else:
            return filtre
            
    # Swap function 
    def swapList(self, ele): 
        
        first = ele.pop(0)    
        last = ele.pop(-1) 
        
        ele.insert(0, last)   
        ele.append(first)    
        
        return ele

    #bouffer un pion sur le board
    def makeSteal(self, board, pawn):
        if(self.player_color!=board[pawn[0]][pawn[1]]):
            board[pawn[0]][pawn[1]]=None
        return board


    def eval(self, board):
        score=self.scores_from_board(board)
        return score[0] - score[1]

    def alfaHelper(self, board, case):
        ele=0
        x, y = case

        #test1
        x_1=x+0
        y_1=y-1
        if self.is_place_on_board((x_1, y_1)) and self.is_empty_cell(board, (x_1, y_1)):
            x_2=x+0
            y_2=y-2
            if self.is_place_on_board((x_2, y_2)) and not self.is_empty_cell(board, (x_2, y_2)):
                if board[x_2][y_2]==self.player_color:
                    x_3=x+0
                    y_3=y-3
                    if self.is_place_on_board((x_3, y_3)) and self.is_empty_cell(board, (x_3, y_3)):
                        ele+=1

        #test2
        x__1=x+0
        y__1=y+1
        if self.is_place_on_board((x__1, y__1)) and self.is_empty_cell(board, (x__1, y__1)):
            x__2=x+0
            y__2=y+2
            if self.is_place_on_board((x__2, y__2)) and not self.is_empty_cell(board, (x__2, y__2)):
                if board[x__2][y__2]==self.player_color:
                    x__3=x+0
                    y__3=y+3
                    if self.is_place_on_board((x__3, y__3)) and self.is_empty_cell(board, (x__3, y__3)):
                        ele+=1
        
        #test3
        x_1=x-1
        y_1=y+0
        if self.is_place_on_board((x_1, y_1)) and self.is_empty_cell(board, (x_1, y_1)):
            x_2=x-2
            y_2=y+0
            if self.is_place_on_board((x_2, y_2)) and not self.is_empty_cell(board, (x_2, y_2)):
                if board[x_2][y_2]==self.player_color:
                    x_3=x-3
                    y_3=y+0
                    if self.is_place_on_board((x_3, y_3)) and self.is_empty_cell(board, (x_3, y_3)):
                        ele+=1

        #test4
        x_1=x+1
        y_1=y+0
        if self.is_place_on_board((x_1, y_1)) and self.is_empty_cell(board, (x_1, y_1)):
            x_2=x+2
            y_2=y+0
            if self.is_place_on_board((x_2, y_2)) and not self.is_empty_cell(board, (x_2, y_2)):
                if board[x_2][y_2]==self.player_color:
                    x_3=x+3
                    y_3=y+0
                    if self.is_place_on_board((x_3, y_3)) and self.is_empty_cell(board, (x_3, y_3)):
                        ele+=1

        return ele

    # alpha beta maximizer
    def ami(self, board, depth, a, b):
        if depth <= 0 :
            return self.eval(board), (),()
        
        alpha=a
        beta=b

        _eval=-999999999
        since,to=(-1,1),(-1,1)
        
        caseJouable = self.filterPlayable(board, self.player_number)
        for case in caseJouable:
            real_move = self.get_piece_actual_moves(board, case, self.player_number)

            best_board=self.clone(board)
            best_move=(-1,-1)
            best_score=-9999
            best_s=0

            bene=0

            for possible_move in real_move:
                board_cpy = self.clone(board)
            
                steal, board_cpy=self.makeMove(board_cpy, case, possible_move)
                bene=steal

                if(steal>0):
                    bene+=1
                    s_steal=self.stealable(board_cpy, self.player_number)

                    if s_steal[0]!=-1 and s_steal[1]!=-1:
                        board_cpy=self.makeSteal(board_cpy, s_steal)

                #check=self.alfaHelper(self.clone(best_board), possible_move)
                #steal-=check
                #print(f"check::{check} - {best_s}")

                if steal>best_score:
                    best_score=steal
                    best_board=board_cpy
                    best_move=possible_move

            
            board_cpy = self.clone(best_board)

            e_score=self.ennemie(board_cpy, depth-1, alpha, beta)[0]+bene
                
            #print(f"e_score::{e_score} - {alpha}")

            if e_score > alpha:
                alpha= e_score
                since=case
                to=best_move
            
            #print(f"alpha::{e_score} - {alpha}")

            if alpha >= beta:
                return beta, since, to
                
        return alpha, since, to


    # alpha beta manimizer
    def ennemie(self, board, depth, a, b):
        if depth <= 0 :
            return self.eval(board), (),()

        alpha=a
        beta=b
        _eval=999999999
        since,to=(-1,1),(-1,1)

        player=(self.player_number+1)%2

        caseJouable = self.filterPlayable(board,player)
        for case in caseJouable:
            real_move = self.get_piece_actual_moves(board, case, player)

            best_board=self.clone(board)
            best_score=-9999
            best_move=(-1,-1)

            bene=0
            
            for possible_move in real_move:
                board_cpy = self.clone(board)
                
                steal, board_cpy=self.makeMove(board_cpy, case, possible_move)
                bene=steal

                if(steal>0):
                    bene+=1
                    s_steal=self.stealable(board_cpy, player)

                    if s_steal[0]!=-1 and s_steal[1]!=-1:
                        board_cpy=self.makeSteal(board_cpy, s_steal)

                if steal>best_score:
                    best_score=steal
                    best_board=board_cpy
                    best_move=possible_move
                    

            board_cpy = self.clone(best_board)

            e_score=self.ami(board_cpy, depth-1, alpha, beta)[0]-bene

            if e_score < beta:
                beta= e_score
                since=case
                to=best_move

            if alpha >= beta:
                return alpha, since, to
        
        return beta, since, to


    #minimax avec profondeur 1
    def simplePlay(self, board, player):
        caseJouable = self.get_all_possibles_moves(board, player)["pieces"]

        best_gain = -999999999
        since,to=(-1,1),(-1,1)
        for case in caseJouable:
            real_move = self.get_piece_actual_moves(board, case, player)

            for possible_move in real_move:
                board_cpy = self.clone(board)
                steal, board_cpy=self.makeMove(board_cpy, case, possible_move)

                if player==self.player_number and steal > best_gain:
                    best_gain = steal
                    since=case
                    to=possible_move
                    
                elif player!=self.player_number and steal > best_gain:
                    best_gain = steal
                    since=case
                    to=possible_move

        #print(f"return board:{board}")

        return best_gain,since,to

    #poser un pion sur le  board
    def putOnBoard(self, board, cell, color):
        if self.is_place_on_board(cell) and self.is_empty_cell(board, cell):
            board[cell[0]][cell[1]] = color
        return board

    #déplacer un pion d'une case à une autre
    #et vérifie si le déplacement donne un gain
    def makeMove(self, board, since, to):
        steal=0

        color = board[since[0]][since[1]]
        board[since[0]][since[1]] = None
        board[to[0]][to[1]] = color

        distance = math.sqrt( ((to[0]-since[0])**2)+((to[1]-since[1])**2) )

        if distance==2:
            center=((since[0]+to[0])//2,(since[1]+to[1])//2)

            if self.is_place_on_board(center):
                steal=1
                board[center[0]][center[1]] = None

        return steal, board

    #grouper et compter les pions présents sur le board
    def pawsStateOnBoard(self, board):
        return Counter(color for colors in board for color in colors if color is not None)

    #renvoyer le score du jeu
    def scores_from_board(self, board):
        pieces = self.pawsStateOnBoard(board)
        our_pieces = pieces[self.player_color]

        return (self.captured_pieces, 12 - our_pieces - self.player_pieces_in_hand)

    #cloner le board
    def clone(self, element): 
        return copy.deepcopy(element)

    #stratégie de vol
    def stealable(self, board, player):
        #sera volé tout ce que constitue dss menaces pour nos pions
        # par exemple les pions adverses qui a un déplacement peuvent nous bouffer
        dangerous_pawn=self.dangerousPawn(board, player)
        if not dangerous_pawn:
            #vérifier s'il a des pions dans la reserve de l'adversaire
            #je compte alors les pions
            opponentCaseJouable = self.get_playable_pieces(board, (player+1)%2)

            if self.captured_pieces+len(opponentCaseJouable)!=12:
                return -1, -1
            else:
                return opponentCaseJouable[random.randint(0,len(opponentCaseJouable)-1)]
        
        return dangerous_pawn[random.randint(0,len(dangerous_pawn)-1)]


    #liste des pions qui peuvent nous bouffer
    def dangerousPawn(self, board, player):
        paws = list()
        #je récupère tous mes pions sur la grille
        color=TILES_COLOR[player]

        caseJouable = self.get_all_possibles_moves(board, player)["pieces"]
        for case in caseJouable:
            #pour chaque case, je récupère les déplacements théoriques
            theoricalMove=self.get_possible_moves(case)
            if theoricalMove:
                for paw in theoricalMove:
                    if self.is_place_on_board(paw) and not self.is_empty_cell(board, paw) and color!=board[paw[0]][paw[1]]:
                        steal = self.playCase(self.clone(board), paw, (player+1)%2)[0]
                        if(steal!=0 and paw not in paws):
                            paws.append(paw)
                            #break

        return paws

