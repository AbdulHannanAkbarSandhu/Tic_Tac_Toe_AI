import copy  # Import the copy module to create deep copies of the board
import math  # Import the math module for infinity constants

# Constants representing players and empty cells
X = "X"  # Player X
O = "O"  # Player O
EMPTY = None  # Empty cell

def initial_state():
  
    # Returns the starting state of the board.
    
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
   
   
    
    # Count the number of X's and O's on the board
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    # The player with fewer moves is the next to play
    return O if count_x > count_o else X

def actions(board):
   
    # Return a set of coordinates for all empty cells
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    
    if action not in actions(board):
        raise Exception("Invalid action")  # Raise an error if the action is invalid
    new_board = copy.deepcopy(board)  # Create a deep copy of the board
    new_board[action[0]][action[1]] = player(board)  # Apply the action to the new board
    return new_board

def winner(board):
   
    # Check rows for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
    # Check columns for a winner
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    # Check diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None  # No winner

def terminal(board):
    
    if winner(board) is not None:  # Check for a winner
        return True
    if all(cell is not EMPTY for row in board for cell in row):  # Check for a full board
        return True
    return False

def utility(board):
   
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def max_value(board):
    
    if terminal(board):  # Check if the game is over
        return utility(board)
    v = -math.inf  # Initialize to negative infinity
    for action in actions(board):  # Evaluate all possible actions
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
   
    if terminal(board):  # Check if the game is over
        return utility(board)
    v = math.inf  # Initialize to positive infinity
    for action in actions(board):  # Evaluate all possible actions
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    
    if terminal(board):  # Check if the game is over
        return None
    current_player = player(board)  # Determine the current player
    # Find the best move for the current player
    if current_player == X:
        value, move = max((min_value(result(board, action)), action) for action in actions(board))
    else:
        value, move = min((max_value(result(board, action)), action) for action in actions(board))
    return move