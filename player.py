from abc import ABC, abstractmethod
TILES_COLOR = ["black", "white"]


class Player(ABC):
    name = "Player"

    def __init__(self, player_number, board_size):
        self.player_pieces = 12
        self.player_pieces_in_hand = 12
        self.captured_pieces = 0
        self.player_number = player_number
        self.board_size = board_size  # Is a tuple containing (row, col)
        self.TILES_COLOR = ["black", "white"]
        self.color = TILES_COLOR[player_number]

    def reset_player_data(self):
        self.player_pieces = 12
        self.player_pieces_in_hand = 12
        self.captured_pieces = 0

    @abstractmethod
    def play(self, depth_to_cover, board, can_steal):
        pass

    def get_name(self):
        return self.name

    def get_self_player_number(self):
        return self.player_number

    def get_score(self):
        return self.captured_pieces

    def set_score(self, score):
        self.player_pieces = score[0]
        self.player_pieces_in_hand = score[1]
        self.captured_pieces = score[2]

    def get_playable_pieces(self, board, player_number):  # Return all on board player tiles coordinates
        color = TILES_COLOR[player_number]
        row, col = self.board_size
        playable = list()
        for i in range(row):
            for j in range(col):
                if board[i][j] is not None and board[i][j].lower() == color.lower():
                    playable.append((i, j))
        return playable

    def is_place_on_board(self, cell):  # Check if the given cell exists on board
        i, j = cell
        row, col = self.board_size
        if i in range(0, row) and j in range(0, col):
            return True
        return False

    def is_empty_cell(self, board, cell):
        i, j = cell
        if self.is_place_on_board(cell) and board[i][j] is None:
            return True
        return False

    def get_empty_cells(self, board):
        empty_cells = list()
        row, col = self.board_size
        for i in range(row):
            for j in range(col):
                if self.is_empty_cell(board, (i, j)):
                    empty_cells.append((i, j))
        return empty_cells

    def get_no_empty_cell_color(self, board, cell):
        i, j = cell
        if not self.is_empty_cell(board, cell) and self.is_place_on_board(cell):
            return board[i][j]
        return None

    def get_possible_moves(self, cell):  # Return the theoretical possibles moves of a tile on a x y axis
        i, j = cell
        row, col = self.board_size
        return [(cell[0] + a[0], cell[1] + a[1]) for a in
                [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if ((0 <= cell[0] + a[0] < row) and (0 <= cell[1] + a[1] < col))]

    def get_piece_actual_moves(self, board, cell, player_number):
        moves = list()
        i, j = cell
        if self.get_possible_moves(cell) is not None:
            for move in self.get_possible_moves(cell):
                if self.is_empty_cell(board, move):
                    moves.append(move)
                elif self.get_no_empty_cell_color(board, move) != self.TILES_COLOR[player_number]:
                    k, l = move
                    if i == k and j < l and self.is_empty_cell(board, (i, j + 2)):
                        moves.append((i, j + 2))
                    elif i == k and l < j and self.is_empty_cell(board, (i, j - 2)):
                        moves.append((i, j - 2))
                    elif j == l and i < k and self.is_empty_cell(board, (i + 2, j)):
                        moves.append((i + 2, j))
                    elif j == l and k < i and self.is_empty_cell(board, (i - 2, j)):
                        moves.append((i - 2, j))
            return moves

    def get_movable_pieces_by_player(self, board, player_number):  # Returns for a player all the pieces he can move
        pieces = self.get_playable_pieces(board, player_number)
        moves = list()
        for piece in pieces:
            if len(self.get_piece_actual_moves(board, piece, player_number)) > 0:
                moves.append(piece)
        return moves

    def get_all_possibles_moves(self, board, player_number):
        moves = dict()
        moves["empty_cells"] = self.get_empty_cells(board)
        moves["pieces"] = self.get_movable_pieces_by_player(board, player_number)
        return moves

    def piece_can_move(self, board, cell, player_number):
        return len(self.get_piece_actual_moves(board, cell, player_number)) != 0 and self.get_no_empty_cell_color(board, cell) == self.TILES_COLOR[player_number]
