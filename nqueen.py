#!/usr/bin/env python3
import sys

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( r if isinstance(r, int) else 0 for r in board[row])

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] if isinstance(row[col], int) else 0 for row in board] )

# Count total # of pieces on board
def count_pieces(board):
    return sum([ r if isinstance(r, int) else 0 for row in board for r in row ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([" ".join([required_type if col==1 else  "_" if col==0 else col for col in row]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

#Checking if the position is empty
def not_already_occupied(board,r,c):
    return board[r][c]!="X" and board[r][c]!=required_type;

# Checking if the diagonals are empty
def no_elements_in_diagonals(board,r,c):
    return diagonal_left_d(board,r,c) & diagonal_left_top(board,r,c) & diagonal_right_d(board,r,c)& diagonal_right_top(board,r,c);

def diagonal_left_top(board,r,c):
     tot=0
     while r >= 0  and c >= 0:
           tot=tot+(board[r][c] if isinstance(board[r][c], int) else 0)
           r=r-1;
           c=c-1;
     return tot==0;

def diagonal_right_top(board, r, c):
    tot = 0
    while r >= 0 and c < N:
        tot = tot + (board[r][c] if isinstance(board[r][c], int) else 0)
        r=r-1;
        c=c+1;
    return tot == 0;

def diagonal_left_d(board, r, c):
    tot = 0
    while r < N and c >= 0:
        tot = tot + (board[r][c] if isinstance(board[r][c], int) else 0)
        r=r+1;
        c=c-1;
    return tot == 0;

def diagonal_right_d(board, r, c):
    tot = 0
    while  r < N and c < N:
        tot = tot + ( board[r][c] if isinstance(board[r][c], int) else 0)
        r=r+1;
        c=c+1;
    return tot == 0;

# Get list of successors of given board state
def successors(board):
    succs = []
    row = count_pieces(board)
    for col in range(0, N):
        temp_piece = add_piece(board, row, col)
        if board[row][col]!=1 and count_on_col(board,col)<1 and not_already_occupied(board,row,col) \
            and (no_elements_in_diagonals(board,row,col) if required_type=='Q' else True) :
                succs.append(temp_piece)
    return succs;

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks and n-queens!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

#Knight Solution
def solve_knight(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors_knight( fringe.pop() ):
            if is_goal_knight(s):
                return(s)
            fringe.append(s)
    return False

#Goal for the knight
def is_goal_knight(board):
    if count_pieces(board)!=N:
        return False
    for r in range(0,N):
        for c in range(0,N):
            if board[r][c]==1:
                if not knight_not_exist(board, r, c) :
                    return False
    return True

#Successors for the knight
def successors_knight(board):
    succs = []
    #row = count_pieces(board)
    for row in range(0,N):
        for col in range(0, N):
            if board[row][col]!=1 and knight_not_exist(board,row,col) and count_pieces(board)<=N and in_range(row,col) and not_already_occupied(board,row,col):
                    succs.append(add_piece(board, row, col))
    return succs;

#Check if no other knight present, that would take down the knight about to be placed
def knight_not_exist(board,r,c):
    if in_range(r-2,c+1):
        if board[r-2][c+1]==1:
            return False;
    if in_range(r - 1, c + 2):
        if board[r - 1][c + 2] == 1:
            return False;
    if in_range(r + 1, c + 2):
        if board[r + 1][c + 2] == 1:
            return False;
    if in_range(r + 2, c + 1):
        if board[r + 2][c + 1] == 1:
            return False;
    if in_range(r + 2, c - 1):
        if board[r + 2][c - 1] == 1:
            return False;
    if in_range(r + 1, c - 2):
        if board[r + 1][c - 2] == 1:
            return False;
    if in_range(r - 1, c - 2):
        if board[r - 1][c - 2] == 1:
            return False;
    if in_range(r - 2, c - 1):
        if board[r - 2][c - 1] == 1:
            return False;
    return True
#check for indexes are in bounds
def in_range(r,c):
    if (r>=0 and r<N) and (c>=0 and c<N):
        return True

# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[2])
# number of block positions
unavailable=int(sys.argv[3])
#Check for rrok or queen
required_type="R" if sys.argv[1]=="nrook" else "Q";
initial_board = [[0 for x in range(N)] for y in range(N)]
for i in range(0,unavailable*2,2):
      initial_board[int(sys.argv[i+4])-1][int(sys.argv[i+5])-1]="X";
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
if sys.argv[1]=="nknight":
    required_type="K"
    solution = solve_knight(initial_board)
    print(printable_board(solution) if solution else "Sorry, no solution found. :(")
else:
    solution = solve(initial_board)
    print(printable_board(solution) if solution else "Sorry, no solution found. :(")
