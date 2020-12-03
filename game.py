import pygame
import sys
from board import Board
from constant import *
from piece import *
from copy import deepcopy


class Game:
    def __init__(self, win):
        self.win = win
        self._init()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = 'W'
        self.legal_moves = None
        self.check = False
        self.history = []
        self.future = []
        self.checkmate = False
        self.stalemate = False
        self.board.print_board()

    def reset(self):
        self._init()

    def get_checkmate(self):
        return self.checkmate

    def get_stalemate(self):
        return self.stalemate

    def update(self):
        self.board.draw_board(self.win)

        if self.selected:
            self.board.highlight_square(self.selected, self.win)
            self.show_legal_moves(self.legal_moves)

        if self.check:
            self.board.draw_check(self.turn, self.win)

        self.board.draw_pieces(self.win)
        pygame.display.update()

        if self.checkmate:
            print('CHECKMATE')
            print(f'{get_opposite_colour(self.turn)} WON')
            choice = input('Play again (Y/N) ? ').upper()
            if choice == 'Y':
                self._init()
            else:
                sys.exit(0)

        if self.stalemate:
            print('STALEMATE')
            choice = input('Play again (Y/N) ? ').upper()
            if choice == 'Y':
                self._init()
            else:
                sys.exit(0)



    def select(self, pos):
        '''piece already selected - move piece'''
        if self.selected:
            if pos in self.legal_moves:
                col, row = pos
                self.history.append(deepcopy(self.board))

                # castling
                if isinstance(self.selected, King) and abs(self.selected.col - col) > 1:
                    side = 'Q' if self.selected.col - col > 1 else 'K'
                    self.board.castle(side, self.turn, pos)

                # en passant
                if isinstance(self.selected, Pawn) and self.board.get_piece(pos) == 0 and self.selected.col != col:
                    self.board.en_passant(self.selected, pos)

                # normal move
                else:
                    self._move(self.selected, pos)

                self.turn = get_opposite_colour(self.turn)

                self.board.print_board()
                self.selected.increment_move_num()

                self.check = self.board.is_check(self.turn)
                all_legal_moves = self.get_all_legal_moves(self.turn)
                if all_legal_moves == []:
                    if self.check:
                        self.checkmate = True
                    else:
                        self.stalemate = True

            self.selected = None

        # no piece selected - select piece
        else:
            selected_piece = self.board.get_piece(pos)
            if selected_piece != 0:
                if selected_piece.get_colour() == self.turn:
                    self.selected = selected_piece
                    self.legal_moves = self.get_legal_moves(self.selected)
                    print(list(map(convert_to_notation, self.legal_moves)))



    def _move(self, piece, pos):
        self.board.move(piece, pos)

        # pawn promotion
        col, row = pos
        if isinstance(piece, Pawn):
            if piece.get_colour() == 'W':
                promote_row = 0
            else:
                promote_row = ROWS - 1

            if row == promote_row:
                self.promote_pawn(pos, piece.get_colour())


    def promote_pawn(self, pos, colour):
        print('PAWN PROMOTION')
        col, row = pos
        print('[Q] QUEEN, [R] ROOK, [B] BISHOP, [N] KNIGHT')
        choice = input('Pawn Promotion:').upper()

        if choice == 'Q':
            new_piece = Queen(col, row, colour)
        if choice == 'R':
            new_piece = Rook(col, row, colour)
        if choice == 'B':
            new_piece = Bishop(col, row, colour)
        if choice == 'N':
            new_piece = Knight(col, row, colour)
        self.board.board[row][col] = new_piece



    def get_legal_moves(self, piece):
        '''
        - pin pieces -> piece cannot move / can only move to some square
        - king in check -> king must move out of check / other piece must block check
        - en passant
        - castling
        - pawn promotion

        returns: list of position of legal moves
        '''
        legal_moves = []

        # en passant
        if isinstance(piece, Pawn):
            legal_moves.extend(self.get_en_passant_move(piece))

        # castling
        if isinstance(piece, King):
            legal_moves.extend(self.get_castle_move(piece))


        # pin pieces / king in check
        all_moves = piece.get_moves(self.board.get_board()) + legal_moves
        for pos in all_moves:
            new_board, new_piece = deepcopy(self.board), deepcopy(piece)
            new_board.move(new_piece, pos)
            check = new_board.is_check(self.turn)
            if not check:
                legal_moves.append(pos)

        return legal_moves


    def get_castle_move(self, piece):
        castle_move = []
        all_moves_on_board = self.board.get_all_moves(get_opposite_colour(piece.get_colour()))

        if piece.get_move_num() == 0:  # king must not have move
            # king side castling
            r_col, r_row = COLS - 1, piece.row
            rook = self.board.get_piece((r_col, r_row))

            if isinstance(rook, Rook):
                if rook.get_move_num() == 0:  # rook must not have move

                    # no piece b/w king and rook && other pieces cannot move to square b/w king and rook
                    empty = True
                    for i in range(piece.col + 1, r_col):
                        if self.board.get_piece((i, r_row)) != 0 or (i, r_row) in all_moves_on_board:
                            empty = False
                            break

                    if empty:
                        castle_pos = (r_col - 1, r_row)
                        castle_move.append(castle_pos)

            # queen side castling
            r_col, r_row = 0, piece.row
            rook = self.board.get_piece((r_col, r_row))

            if isinstance(rook, Rook):
                if rook.get_move_num() == 0:  # rook must not have move

                    # no piece b/w king and rook && other pieces cannot move to square b/w king and rook
                    empty = True
                    for i in range(r_col + 1, piece.col):
                        if self.board.get_piece((i, r_row)) != 0 or (i, r_row) in all_moves_on_board:
                            empty = False
                            break
                    if empty:
                        castle_pos = (r_col + 2, r_row)
                        castle_move.append(castle_pos)

        return castle_move
        

    def get_en_passant_move(self, piece):
        delta_row = 3
        can_en_passant = False
        en_passant_move = []

        if piece.get_colour() == 'W':
            if piece.row == delta_row:
                can_en_passant = True

        else:
            if piece.row == (ROWS - 1) - delta_row:
                can_en_passant = True

        if can_en_passant:
            # check right side
            if piece.col < COLS - 1:
                right_pos = (piece.col + 1, piece.row)
                right_piece = self.board.get_piece(right_pos)
                if isinstance(right_piece, Pawn):
                    if right_piece.get_move_num() == 1:
                        board_before = self.history[-1]
                        if board_before.get_piece(right_pos) == 0:
                            en_passant_row = piece.row + 1 if piece.get_colour() == 'B' else piece.row - 1
                            en_passant_pos = (piece.col + 1, en_passant_row)
                            en_passant_move.append(en_passant_pos)

            # check left side
            if piece.col > 0:
                left_pos = (piece.col - 1, piece.row)
                left_piece = self.board.get_piece(left_pos)
                if isinstance(left_piece, Pawn):
                    if left_piece.get_move_num() == 1:
                        board_before = self.history[-1]
                        if board_before.get_piece(left_pos) == 0:
                            en_passant_row = piece.row + 1 if piece.get_colour() == 'B' else piece.row - 1
                            en_passant_pos = (piece.col - 1, en_passant_row)
                            en_passant_move.append(en_passant_pos)

        return en_passant_move


        
    def show_legal_moves(self, legal_moves):
        '''draw circle on legal moves on window'''
        size = G_CIRCLE.get_rect().size
        for pos in self.legal_moves:
            col, row = pos
            y = (row * SQUARE_SIZE)
            x = (col * SQUARE_SIZE)
            if self.board.get_piece(pos) == 0:
                self.win.blit(G_CIRCLE, (x, y))
            else:
                self.win.blit(CAPTURE_CIRCLE, (x ,y))


    
    def undo(self):
        if len(self.history) > 0:
            self.turn = get_opposite_colour(self.turn)
            self.future.append(deepcopy(self.board))
            self.board = self.history.pop()
            print('UNDO')


    def redo(self):
        if len(self.future) > 0:
            self.turn = get_opposite_colour(self.turn)
            self.history.append(deepcopy(self.board))
            self.board = self.future.pop()
            print('REDO')


    def get_all_legal_moves(self, colour):
        all_legal_moves = []
        for row in self.board.get_board():
            for piece in row:
                if piece != 0:
                    if piece.get_colour() == colour:
                        all_legal_moves.extend(self.get_legal_moves(piece))
        return all_legal_moves