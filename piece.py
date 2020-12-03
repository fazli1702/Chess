import pygame
from constant import *

class Piece:
    def __init__(self, col, row, colour):
        self.row = row 
        self.col = col
        self.colour = colour
        self.selected = False
        self.move_num = 0

    def get_pos(self):
        return (self.col, self.row)

    def get_pos_notation(self):
        return convert_to_notation(self.get_pos())

    def get_coordinate(self):
        '''returns top left corner coordinate'''
        x = self.col * SQUARE_SIZE
        y = self.row * SQUARE_SIZE
        return (x, y)

    def get_colour(self):
        return self.colour

    def get_selected(self):
        return self.selected

    def get_move_num(self):
        return self.move_num

    def set_pos(self, pos):
        col, row = pos
        self.row = row
        self.col = col

    def set_selected(self, n):
        self.selected = n

    def move(self, new_pos):
        col, row = new_pos
        self.col = col
        self.row = row

    def increment_move_num(self):
        self.move_num += 1


class Pawn(Piece):
    def __init__(self, col, row, colour):
        super().__init__(col, row, colour)
    
    def __repr__(self):
        return self.colour + 'P'

    def show(self, win):
        '''display image on screen'''
        if self.colour == 'W':
            img = W_PAWN
        else:
            img = B_PAWN
        win.blit(img, self.get_coordinate())

    def get_moves(self, board):
        '''return list of standard moves that piece can make'''
        moves = []

        # can move 2 steps at start
        if self.move_num == 0:
            for i in range(1, 3):
                col, row = self.get_pos()
                if self.colour == 'W':
                    row -= i
                else:
                    row += i

                if board[row][col] == 0:
                    moves.append((col, row))
                else:
                    break

        # can only move 1 step
        else:
            col, row = self.get_pos()
            if self.colour == 'W':
                row -= 1
            else:
                row += 1
            
            if board[row][col] == 0:
                moves.append((col, row))


        # can capture sideways - check if piece exist
        if self.colour == 'W':
            row = self.row - 1
        else:
            row = self.row + 1

        # check left side
        if self.col < 7:
            col = self.col + 1
            curr_piece = board[row][col]
            if curr_piece != 0:
                if curr_piece.colour != self.colour:
                    moves.append((col, row))

        # check right side
        if self.col > 0:
            col = self.col - 1
            curr_piece = board[row][col]
            if curr_piece != 0:
                if curr_piece.colour != self.colour:
                    moves.append((col, row))

        return moves



class Knight(Piece):
    def __init__(self, col, row, colour):
        super().__init__(col, row, colour)
    
    def __repr__(self):
        return self.colour + 'N'

    def show(self, win):
        if self.colour == 'W':
            img = W_KNIGHT
        else:
            img = B_KNIGHT
        win.blit(img, self.get_coordinate())

    def get_moves(self, board):
        moves = []
        steps = [(-2, -1), (-2, +1), (+2, -1), (+2, +1), (-1, -2), (-1, +2), (+1, -2), (+1, +2)]
        for step in steps:
            col, row = self.get_pos()
            col += step[1]
            row += step[0]

            if 0 <= col < COLS and 0 <=row < ROWS:
                curr_piece = board[row][col]

                if curr_piece == 0:
                    moves.append((col, row))

                elif curr_piece.colour != self.colour:
                    moves.append((col, row))

        return moves



class Bishop(Piece):
    def __init__(self, col, row, colour):
        super().__init__(col, row, colour)
    
    def __repr__(self):
        return self.colour + 'B'

    def show(self, win):
        if self.colour == 'W':
            img = W_BISHOP
        else:
            img = B_BISHOP
        win.blit(img, self.get_coordinate())

    def get_moves(self, board):
        moves = []
        steps = [(+1, +1), (-1, -1), (+1, -1), (-1, +1)]
        for step in steps:
            col, row = self.get_pos()
            stop = False
            while not stop:
                col += step[1]
                row += step[0]

                if 0 <= col < COLS and 0 <= row < ROWS:
                    curr_piece = board[row][col]

                    if curr_piece == 0:
                        moves.append((col, row))

                    elif curr_piece.colour != self.colour:
                        moves.append((col, row))
                        stop = True

                    else:
                        stop = True
                else:
                    stop = True

        return moves


class Rook(Piece):
    def __init__(self, col, row, colour):
        super().__init__(col, row, colour)
    
    def __repr__(self):
        return self.colour + 'R'

    def show(self, win):
        if self.colour == 'W':
            img = W_ROOK
        else:
            img = B_ROOK
        win.blit(img, self.get_coordinate())

    def get_moves(self, board):
        moves = []
        steps = [(+1, 0), (0, +1), (-1, 0), (0, -1)]
        for step in steps:
            col, row = self.get_pos()
            stop = False
            while not stop:
                col += step[1]
                row += step[0]

                if 0 <= col < COLS and 0 <= row < ROWS:
                    curr_piece = board[row][col]

                    if curr_piece == 0:
                        moves.append((col, row))

                    elif curr_piece.colour != self.colour:
                        moves.append((col, row))
                        stop = True

                    else:
                        stop = True
                else:
                    stop = True

        return moves



class Queen(Piece):
    def __init__(self, col, row, colour):
        super().__init__(col, row, colour)
    
    def __repr__(self):
        return self.colour + 'Q'

    def show(self, win):
        if self.colour == 'W':
            img = W_QUEEN
        else:
            img = B_QUEEN
        win.blit(img, self.get_coordinate())

    def get_moves(self, board):
        moves = []
        steps = [(+1, 0), (0, +1), (-1, 0), (0, -1),      # horizontal and vertical steps
                (+1, +1), (-1, -1), (+1, -1), (-1, +1)]  # diagonal steps  
        for step in steps:
            col, row = self.get_pos()
            stop = False
            while not stop:
                col += step[1]
                row += step[0]

                if 0 <= col < COLS and 0 <= row < ROWS:
                    curr_piece = board[row][col]

                    if curr_piece == 0:
                        moves.append((col, row))

                    elif curr_piece.colour != self.colour:
                        moves.append((col, row))
                        stop = True

                    else:
                        stop = True
                else:
                    stop = True

        return moves



class King(Piece):
    def __init__(self, col, row, colour):
        super().__init__(col, row, colour)
    
    def __repr__(self):
        return self.colour + 'K'

    def show(self, win):
        if self.colour == 'W':
            img = W_KING
        else:
            img = B_KING
        win.blit(img, self.get_coordinate())

    def draw_check(self, win):
        win.blit(R_CIRCLE, self.get_coordinate())

    def get_moves(self, board):
        moves = []
        steps = [(+1, 0), (0, +1), (-1, 0), (0, -1),      # horizontal and vertical steps
                (+1, +1), (-1, -1), (+1, -1), (-1, +1)]  # diagonal steps  
        for step in steps:
            col, row = self.get_pos()
            col += step[1]
            row += step[0]

            if 0 <= col < COLS and 0 <= row < ROWS:
                curr_piece = board[row][col]

                if curr_piece == 0:
                    moves.append((col, row))

                elif curr_piece.colour != self.colour:
                    moves.append((col, row))

        return moves