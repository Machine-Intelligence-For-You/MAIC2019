# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 20:57:54 2019

@author: PROBOOK
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 21:15:06 2019

@author: PROBOOK
"""

# -*- coding: utf-8 -*-
import random
from util import timeout
from player import Player
#from board import Board
from pprint import pprint
from copy import deepcopy
TILES_COLOR = ["black", "green"]
inf = float("inf")


A = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),\
     (1,0),                        (1,5),\
     (2,0),                        (2,5),\
     (3,0),                        (3,5),\
     (4,0),(4,1),(4,2),(4,3),(4,4),(4,5)]


class AI(Player):

    # Team modify this
    name = "SLH"
    
    def __init__(self, player_number, board_size, in_hand = 12, captured = 0):
        Player.__init__(self, player_number, board_size)
        self.captured_pieces = captured
        self.player_pieces_in_hand = in_hand
        self.depth = 2
        

    def get_player_score(self):
        return self.captured_pieces

    def get_player_name(self):
        return self.name
    
    @timeout(seconds=0.1)
    def play(self, depth_to_cover, board, can_steal):
        
        print("Player", self.player_number, "j'ai encore", self.player_pieces_in_hand)
        x, y = self.count_pieces(board)
        game = {\
            "board": board,\
            "on_board": x,\
            "in_hand": self.player_pieces_in_hand,\
            "captured": self.captured_pieces,\
            "in_ad_hand": 12 - y - self.captured_pieces\
        }
        return self.minimax(game, self.player_number, can_steal)[0]
        """if can_steal:
            ennemyPieces=[]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] is not None and TILES_COLOR[(self.player_number+1)%2].lower()==board[i][j].lower():
                        ennemyPieces.append((i,j))
            if not ennemyPieces:
                return -1, -1
            return ennemyPieces[random.randint(0,len(ennemyPieces)-1)]"""
    
    

  

    def apply_choice(self, game, action, player_num):
        board = game["board"]
        win = False
        if len(action) == 4:
            i,j,k,l = action
            board[k][l] = board[i][j]
            board[i][j] = None
            if abs(k-i) > 1:
                win = True
                board[min(k,i) + 1][j] = None
                if player_num == self.player_number:
                    game["captured"] += 1
                else:
                    game["on_board"] -= 1
            elif abs(j-l) > 1:
                win = True
                board[i][min(j,l) + 1] = None
                if player_num == self.player_number:
                    game["captured"] += 1
                else:
                    game["on_board"] -= 1
        else:
            i,j = action
            if i == -1:
                if player_num == self.player_number:
                    game["captured"] += 1
                    game["in_ad_hand"] -= 1
                else:
                    game["in_hand"] -= 1
            elif board[i][j] != None and board[i][j].lower() == TILES_COLOR[1 - player_num].lower():
                board[i][j] = None
                if player_num == self.player_number:
                    game["captured"] += 1
                else:
                    game["on_board"] -= 1
            else:
                board[i][j] = TILES_COLOR[player_num].lower()
                if player_num == self.player_number:
                    game["on_board"] += 1
                    game["in_hand"] -= 1
                else:
                    game["in_ad_hand"] -= 1
        return game, win
    
    
    def copyGame(self, game):
        g = dict()
        g["board"] = game["board"].copy()
        for k in game:
            if k != "board":
                g[k] = game[k]
        
        return g
    
    def count_pieces(self, board):
        player, ad = 0,0
        for line in board:
            for cell in line:
                if cell == None:
                    continue
                elif cell.lower() == self.color.lower():
                    player += 1
                else:
                    ad += 1
        return player, ad
    
    def actions(self, game, player):
        board = game["board"]
        d = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        rows, cols = len(board), len(board[0])
        for i, line in enumerate(board):
            for j, cell in enumerate(line):
                if cell != None and cell.lower() == TILES_COLOR[player].lower():
                    for k,l in d:
                        if 0 <= i+k < rows and 0 <= j+l < cols:
                            if board[i+k][j+l] is None:
                                yield i,j,i+k,j+l
                            elif board[i+k][j+l].lower() == TILES_COLOR[1-player].lower() and\
                                 0 <= i+2*k < rows and 0 <= j+2*l < cols and\
                                 board[i+2*k][j+2*l] is None:
                                yield i,j,i+2*k,j+2*l
        if player == self.player_number and game["in_hand"] > 0:
            for act in self.get_empty_cells(game["board"]):
                yield act
        elif player != self.player_number and game["in_ad_hand"] > 0:
            for act in self.get_empty_cells(game["board"]):
                yield act
    
    def steals(self, game, player):
        for i, line in enumerate(game["board"]):
            for j, cell in enumerate(line):
                if cell!=None and cell.lower() == TILES_COLOR[1-player].lower():
                    yield i,j
        if game["in_ad_hand"] > 0:
            yield -1,-1

    def menace(self, board, evaluator):
        player = self.player_number
        def sides(i, j):
            d = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for x, y in d:
                if 0 <= i+x < heigth and 0 <= j+y < width:
                    yield x, y
        mines = 0
        ad = 0
        heigth = len(board)
        width = len(board[0])
        for i, line in enumerate(board):
            for j, cell in enumerate(line):
                if cell == TILES_COLOR[player]:
                    #print(i,j)
                    for k, l in sides(i, j):
                        if board[i+k][j+l] == None:
                            continue
                        if not (0 <= i+2*k < heigth and 0 <= j+2*l < width):
                            continue
                        if board[i+2*k][j+2*l] != None:
                            continue
                        if board[i+k][j+l] != cell:
                            if 0 <= i-k < heigth and 0 <= j-l < width:
                                if board[i-k][j-l] == None and evaluator != player:
                                    mines += 1
                                elif board[i-k][j-l] != None:
                                    mines += 1
                            else:
                                mines += 1
                elif cell == TILES_COLOR[1-player]:
                    for k, l in sides(i, j):
                        if board[i+k][j+l] == None:
                            continue
                        if not (0 <= i+2*k < heigth and 0 <= j+2*l < width):
                            continue
                        if board[i+2*k][j+2*l] != None:
                            continue
                        if board[i+k][j+l] != cell:
                            if 0 <= i-k < heigth and 0 <= j-l < width:
                                if board[i-k][j-l] == None and evaluator == player:
                                    ad += 1
                                if board[i-k][j-l] != None:
                                    ad += 1
                            else:
                                ad += 1
                                
        return mines - ad + (0 if mines!=ad else (0.1 if mines>0 and evaluator != player else -0.1))
    
    def evaluate(self, game, evaluator):
        
        n = self.menace(game["board"], evaluator)
        rest = game["in_hand"] 
        #total = 
        #print(game["on_board"], game["in_hand"], game["captured"], total)
        return game["on_board"] + game["in_hand"] + game["captured"] + (n/10) + (0 if rest>=4 else (rest/100))

    def minimax(self, game, player, can_steal, depth = 2, alpha = inf):
        
        gain = -inf
        bests = []
        f = max
        if player != self.player_number:
            gain = inf
            f = min
        
        if can_steal:
            for act in self.steals(game, player):
                myGame, won = self.apply_choice(deepcopy(game), act, player)
                if depth == 1:
                    g = self.evaluate(myGame, player)
                else:
                    g = self.minimax(myGame, 1 - player, False, depth - 1, gain)[1]
                if g == gain:
                    bests.append(act)
                elif f(g, gain) == g:
                    gain = g;
                    bests = [act]
                if f == max and alpha < gain:
                    return None, gain
                elif f == min and alpha > gain:
                    return None, gain
        else:
            for act in self.actions(game, player):
                
                myGame, won = self.apply_choice(deepcopy(game), act, player)
                
                if won:
                    g = self.minimax(myGame, player, True, depth, gain)[1]
                elif depth == 1:
                    g = self.evaluate(myGame, player)
                else:
                    g = self.minimax(myGame,1 - player,False,depth - 1, gain)[1]
                #pprint((myGame,g))      
                if depth == 2:
                    print(g, act)
                if g == gain:
                    bests.append(act)
                elif f(g, gain) == g:
                    gain = g
                    bests = [act]
                    
                if f == max and alpha < gain:
                    return None, inf
                elif f == min and alpha > gain:
                    return None, -inf
            
            
        if len(bests) > 0:
            action = bests[random.randint(0, len(bests) - 1)] if len(bests) > 0 else None
        else:
            action = None
        """if depth == self.depth:
            print("#####################")
            print(bests)
            print("#####################")"""
        #pprint(game)
        #input()
        
        #print("#-----------------------------------------")
        return action, gain


if __name__ == "__main__":
    player = AI(player_number = 0, board_size = (5,6), in_hand = 3, captured = 0)
    player.depth = 2
    b = [["green","green","black", "black", None, None],
         [ None, "green", None, None , None, None],
         [ "green" ,None , None, None, None, None],
         [ None, None, None, None, None, None],
         [ None, None, None, None, None, None]]
    """b = [[None, "black", None, "green", "green", "black"],
         [None, "green", None,    None, "green", "black"],
         [None,    None, None,    None,    None, "black"],
         [None,    None, None, "green", "black", "black"],
         [None, "green", None,    None, "green", "black"]]"""
    x, y = player.count_pieces(b)
    print(x,y)
    game = {\
        "board": b,\
        "on_board": x,\
        "in_hand": player.player_pieces_in_hand,\
        "captured": player.captured_pieces,\
        "in_ad_hand": 12 - y - player.captured_pieces\
    }
    print("Game", game)
    #print(player.menace(b))
    print(player.minimax(game, 0, False, depth = player.depth))
