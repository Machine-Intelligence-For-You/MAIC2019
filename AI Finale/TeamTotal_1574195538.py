# -*- coding: utf-8 -*-
import random
import os
from util import timeout
from player import Player
TILES_COLOR = ["Black", "green"]


class AI(Player):

    # Team modify this
    name = "Total"

    def __init__(self, player_number, board_size):
        Player.__init__(self, player_number, board_size)

    def get_player_score(self):
        return self.captured_pieces

    def get_player_name(self):
        return self.name
    
    @timeout(seconds=0.1)
    def play(self, depth_to_cover, board, can_steal):

        self.passe1=self.passe2=()

        def soldatdupasse(a,b,c="",d=""):

            if  c=="":
                retourner=(a,b)
            else:
                retourner=(a,b,c,d)

            if retourner==self.passe2:

                if self.player_pieces_in_hand>0:
                    playable=[]
                    bonnetroupe=[]
                    troupetueur=[]
                    i=-1
                    for line in board:
                        i+=1
                        j=-1
                        for case in line:
                            j+=1
                            if case is None:
                                playable.append((i,j))
                    
                    for i in range(len(playable)):
                        if estUnCoupAgreable(playable[i][0],playable[i][1],board,self.player_number)[0]:
                            bonnetroupe.append(playable[i])
                        if estUnCoupAgreable(playable[i][0],playable[i][1],board,self.player_number)[1]:
                            troupetueur.append(playable[i])

                    if troupetueur:
                        soldat=troupetueur[random.randint(0, len(troupetueur)-1)]
                        retourner = soldat
                    if bonnetroupe:
                        soldat=bonnetroupe[random.randint(0, len(bonnetroupe)-1)]
                        retourner = soldat
            
            self.passe2=self.passe1
            self.passe1=retourner
            return retourner



        def is_a_possible_action(self, instruction, can_steal, player_number):# leur fonction a un bug ca donne la possibilité de tuer une troupe
            if not can_steal:
                if not len(instruction) in [2, 4]:
                    return False
                for a in instruction:
                    if not isinstance(a, int):
                        return False
                if len(instruction) == 2:
                    if not self.is_empty_cell(board,instruction):
                        return False
                elif len(instruction) == 4:
                    if (instruction[2], instruction[3]) not in self.get_piece_actual_moves(board,(instruction[0], instruction[1]), player_number):
                        return False
            else:
                if not len(instruction) == 2:
                    return False
                for a in instruction:
                    if not isinstance(a, int):
                        return False
                if not self.get_no_empty_cell_color(board,instruction) == TILES_COLOR[(player_number +  1)%2]:
                    return False
                elif instruction[0] == instruction[1] == -1:
                    return True
            return True

        def aideDispoPour(X,Y):
            color=TILES_COLOR[self.player_number].lower()
            aideur=[]
            if X>0 and board[X-1][Y] is not None and board[X-1][Y].lower()==color:
                aideur.append((X-1,Y))
            if X<len(board)-1 and board[X+1][Y] is not None and board[X+1][Y].lower()==color:
                aideur.append((X+1,Y))
            if Y>0 and board[X][Y-1] is not None and board[X][Y-1].lower()==color:
                aideur.append((X,Y-1))
            if Y<len(board[0])-1 and board[X][Y+1] is not None and board[X][Y+1].lower()==color:
                aideur.append((X,Y+1))
            if aideur:
                return aideur
            return False

        def estUnCoupAgreable(a,b,c,d,e="chou",f="lol",can_steal=False):
            futureboard=[['none', 'none', 'none', 'none', 'none', 'none'], ['none', 'none', 'none', 'none', 'none', 'none'], ['none', 'none', 'none', 'none', 'none', 'none'], ['none', 'none', 'none', 'none', 'none', 'none'], ['none', 'none', 'none', 'none', 'none', 'none']]
            if f!="lol":
                sourceX=a
                sourceY=b
                destinationX=c
                destinationY=d
                board=e
                player_number=f
            else:
                destinationX=a
                destinationY=b
                board=c
                player_number=d
            if not can_steal:    
                for i in range(len(futureboard)):
                    for j in range(len(futureboard[0])):
                        futureboard[i][j]=board[i][j]
                if f!="lol":
                   futureboard[sourceX][sourceY]=None
                futureboard[destinationX][destinationY]=TILES_COLOR[player_number].lower()

                temp=self.get_all_possibles_moves(futureboard, (self.player_number+1)%2)["pieces"]
                for i in range(len(temp)):
                    assassin=temp[i]
                    if peutTuer(futureboard, assassin, (self.player_number+1)%2) is not None:
                        return False,False

                temp=self.get_all_possibles_moves(futureboard, self.player_number)["pieces"]
                for i in range(len(temp)):
                    tueur=temp[i]
                    if peutTuer(futureboard, tueur, self.player_number) is not None:
                        return True,True,peutTuer(futureboard, tueur, self.player_number)
               
                return True,False
            else:
                for i in range(len(futureboard)):
                    for j in range(len(futureboard[0])):
                        futureboard[i][j]=board[i][j]
                futureboard[destinationX][destinationY]=None
                temp=self.get_all_possibles_moves(futureboard, self.player_number)["pieces"]
                for i in range(len(temp)):
                    tueur=temp[i]
                    if peutTuer(futureboard, tueur, self.player_number) is not None:
                        return True
                return False          


        def mouvementspossibleactuel(cell):  # leur fonction a un bug
            moves = list()
            i, j = cell
            color = TILES_COLOR[self.player_number].lower()
            if self.get_possible_moves(cell) is not None:
                for move in self.get_possible_moves(cell):
                    if self.is_empty_cell(board,move):
                        moves.append(move)
                    elif self.get_no_empty_cell_color(board,move).lower() != color:
                        k, l = move
                        if i == k and j < l and self.is_empty_cell(board,(i, j + 2)):
                            moves.append((i, j + 2))
                        elif i == k and l < j and self.is_empty_cell(board,(i, j - 2)):
                            moves.append((i, j - 2))
                        elif j == l and i < k and self.is_empty_cell(board,(i + 2, j)):
                            moves.append((i + 2, j))
                        elif j == l and k < i and self.is_empty_cell(board,(i - 2, j)):
                            moves.append((i - 2, j))
                return moves
            return None

        def peutTuer(board, cell, player_number):
            moves = list()
            i, j = cell
            if self.get_possible_moves(cell) is not None:
                for move in self.get_possible_moves(cell):
                    k, l = move
                    if board[k][l] is not None and TILES_COLOR[(player_number+1)%2].lower()==board[k][l].lower():
                        if i == k and j < l and self.is_empty_cell(board, (i, j + 2)):
                            moves.append((i, j + 2))
                        elif i == k and l < j and self.is_empty_cell(board, (i, j - 2)):
                            moves.append((i, j - 2))
                        elif j == l and i < k and self.is_empty_cell(board, (i + 2, j)):
                            moves.append((i + 2, j))
                        elif j == l and k < i and self.is_empty_cell(board, (i - 2, j)):
                            moves.append((i - 2, j))   
                if moves:
                    return moves

        
        if can_steal:
            temp=self.get_all_possibles_moves(board, (self.player_number+1)%2)["pieces"]
            for i in range(len(temp)):
                assassin=temp[i]
                if peutTuer(board, assassin, (self.player_number+1)%2) is not None:
                    return assassin

            ennemyPieces=[]
            ennemichevaldetroi=[]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] is not None and TILES_COLOR[(self.player_number+1)%2].lower()==board[i][j].lower():
                        ennemyPieces.append((i,j))
                        if estUnCoupAgreable(i,j,board,self.player_number,can_steal=True):
                            ennemichevaldetroi.append((i,j))
            if not ennemichevaldetroi:
                return -1,-1
            return ennemichevaldetroi[random.randint(0,len(ennemichevaldetroi)-1)]
        
        
        nombreenemi=0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] is not None and TILES_COLOR[(self.player_number+1)%2].lower()==board[i][j].lower():
                    nombreenemi+=1

        #J'essai d'abord de tuer un enemi si j'en ai la possibilité et  qu'ils sont plus que 1, plus que 1 pour éviter un bug que j'ai constaté dans le jeu.

        temp=self.get_all_possibles_moves(board, self.player_number)["pieces"]
        for i in range(len(temp)):
            playable=temp[i]
            if peutTuer(board, playable, self.player_number) is not None:
                destinationMeurtre=peutTuer(board, playable, self.player_number)[0]
                return (playable[0],playable[1],destinationMeurtre[0],destinationMeurtre[1])
            
        #J'essai maintenant d'ajouter une troupe pour protéger un autre qui va probablement se faire tuer si j'ai plus de 4 troupes en main, pour éviter de tout metre sur le terrain inutiliement.
        if self.player_pieces_in_hand>2:
            temp2=self.get_all_possibles_moves(board, (self.player_number+1)%2)["pieces"]
            for i in range(len(temp2)):
                assassin=temp2[i]
                if peutTuer(board, assassin, (self.player_number+1)%2) is not None:
                    coup=peutTuer(board, assassin, (self.player_number+1)%2)
                    for j in range(len(coup)):
                        if estUnCoupAgreable(coup[j][0],coup[j][1],board,self.player_number)[0]:
                            return coup[j]

        #J'essai maintenant de déplacer une toupe pour qu'elle aille deriere celle qui se fera tuer.
        temp2=self.get_all_possibles_moves(board, (self.player_number+1)%2)["pieces"]
        for i in range(len(temp2)):
            assassin=temp2[i]
            if peutTuer(board, assassin, (self.player_number+1)%2) is not None:
                coup=peutTuer(board, assassin, (self.player_number+1)%2)
                for j in range(len(coup)):
                    if aideDispoPour(coup[j][0],coup[j][1]):
                        aideur=aideDispoPour(coup[j][0],coup[j][1])
                        for k in range(len(aideur)):
                            aide=aideur[k]
                            aidedupasse=soldatdupasse(aide[0],aide[1],coup[j][0],coup[j][1])
                            if len(aidedupasse)>2:
                                if estUnCoupAgreable(aidedupasse[0],aidedupasse[1],aidedupasse[2],aidedupasse[3],board,self.player_number)[0]:
                                    if is_a_possible_action(self,(aidedupasse[0],aidedupasse[1],aidedupasse[2],aidedupasse[3]),can_steal,self.player_number):
                                        return aidedupasse[0],aidedupasse[1],aidedupasse[2],aidedupasse[3]
                            else:
                                if estUnCoupAgreable(aidedupasse[0],aidedupasse[1],board,self.player_number)[0]:
                                    if is_a_possible_action(self,(aidedupasse[0],aidedupasse[1]),can_steal,self.player_number):
                                        return aidedupasse[0],aidedupasse[1]

        #J'essai maintenant d'ajouter une troupe pour protéger un autre qui va probablement se faire tuer si j'ai des troupes en main parcequ'il na pas pu etre protégé.
        if self.player_pieces_in_hand>0:
            temp2=self.get_all_possibles_moves(board, (self.player_number+1)%2)["pieces"]
            for i in range(len(temp2)):
                assassin=temp2[i]
                if peutTuer(board, assassin, (self.player_number+1)%2) is not None:
                    coup=peutTuer(board, assassin, (self.player_number+1)%2)
                    for j in range(len(coup)):
                        if estUnCoupAgreable(coup[j][0],coup[j][1],board,self.player_number)[0]:
                            return coup[j]

        


        wantTomove=0
        if self.player_pieces_in_hand>2:
            wantTomove=0
            if(len(self.get_all_possibles_moves(board, self.player_number)["empty_cells"])==len(board)*len(board[0])):
                wantTomove=0
            if(len(self.get_movable_pieces_by_player(board, self.player_number))==0):
                wantTomove=0
        else:
            wantTomove=1

        if wantTomove==0:
            playable=[]
            bonnetroupe=[]
            troupetueur=[]
            i=-1
            for line in board:
                i+=1
                j=-1
                for case in line:
                    j+=1
                    if case is None:
                        playable.append((i,j))
            
            for i in range(len(playable)):
                if estUnCoupAgreable(playable[i][0],playable[i][1],board,self.player_number)[0]:
                    bonnetroupe.append(playable[i])
                if estUnCoupAgreable(playable[i][0],playable[i][1],board,self.player_number)[1]:
                    troupetueur.append(playable[i])

            if troupetueur:
                soldat=troupetueur[random.randint(0, len(troupetueur)-1)]
                return soldat
            if bonnetroupe:
                soldat=bonnetroupe[random.randint(0, len(bonnetroupe)-1)]
                return soldat


        else:
            temp=self.get_all_possibles_moves(board, self.player_number)["pieces"]
            bonnetroupe=[]
            troupetueur=[]
            
            for i in range(len(temp)):
                playable=temp[i]
                temp2=mouvementspossibleactuel(playable)
                for j in range(len(temp2)):
                        playableDestination=temp2[j]
                        if estUnCoupAgreable(playable[0],playable[1],playableDestination[0],playableDestination[1],board,self.player_number)[0]:
                            bonnetroupe.append((playable[0],playable[1],playableDestination[0],playableDestination[1]))
                        if estUnCoupAgreable(playable[0],playable[1],playableDestination[0],playableDestination[1],board,self.player_number)[1]:
                            troupetueur.append((playable[0],playable[1],playableDestination[0],playableDestination[1]))
            if troupetueur:
                soldat=troupetueur[random.randint(0, len(troupetueur)-1)]
                return soldatdupasse(soldat[0],soldat[1],soldat[2],soldat[3])
            if bonnetroupe:
                soldat=bonnetroupe[random.randint(0, len(bonnetroupe)-1)]
                return soldatdupasse(soldat[0],soldat[1],soldat[2],soldat[3])

        if self.player_pieces_in_hand>0:
            playable=[]
            bonnetroupe=[]
            troupetueur=[]
            
            i=-1
            for line in board:
                i+=1
                j=-1
                for case in line:
                    j+=1
                    if case is None:
                        playable.append((i,j))
            
            for i in range(len(playable)):
                if estUnCoupAgreable(playable[i][0],playable[i][1],board,self.player_number)[0]:
                    bonnetroupe.append(playable[i])
                if estUnCoupAgreable(playable[i][0],playable[i][1],board,self.player_number)[1]:
                    troupetueur.append(playable[i])

            if troupetueur:
                soldat=troupetueur[random.randint(0, len(troupetueur)-1)]
                return soldat
            if bonnetroupe:
                soldat=bonnetroupe[random.randint(0, len(bonnetroupe)-1)]
                return soldat
            
            return playable[0]


        temp=self.get_all_possibles_moves(board, self.player_number)["pieces"]
        troupe=[]
        for i in range(len(temp)):
            playable=temp[i]
            temp2=mouvementspossibleactuel(playable)
            for j in range(len(temp2)):
                    playableDestination=temp2[j]
                    troupe.append((playable[0],playable[1],playableDestination[0],playableDestination[1]))
        soldat=troupe[random.randint(0, len(troupe)-1)]
        return soldat
