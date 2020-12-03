# TODO

* [x] Create basic Piece, Board, Game class

* [x] Move pieces
    - [x] Basic movement
        - Select piece & move to selected square

    - [x] Show moves
        - basic move
        - other pieces will block move


* [x] Check
    - occurs when opposite colour piece can capture the king
    - highlight king in red


* [x] Legal moves
    - incorporate all the moves in move pieces
    - need to have undo method

    - [x] Pin pieces
        - move piece to possible moves and see if king in check, if king not in check -> legal move

    - [x] King in check
        - [x] move piece to possible moves and see if king in check, if king not in check -> legal move
        - [x] king move away from check

    - [x] King cannot move to check position (put itself in check)

    - [x] En passant
        - opposite colour pawn must be in the same row as attacking pawn
        - opposite colour pawn must have only moved to that square in the last move
        - capture similar to normal pawn capture except move to empty space instead of piece

    - [x] Castling
        - both king and rook must not have move (move_num = 0)
        - no piece in between king and rook
        - opposite colour piece must not be able to move to empty space between king and rook

    - [x] Pawn promotion
        - when pawn reaches the last rank / row (relative to colour of pawn), pawn can promote (Knight, Bishop, Rook, Queen)


* [x] Checkmate
    - King in check
    - No legal moves on board
    - Player who check king wins the game


* [x] Stalemate
    - No legal move for current player
    - Draw


* [x] GUI (display message on screen)
    - checkmate / stalemate
