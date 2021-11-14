# from othello_constants import *  # Also available from othello_board
from base_game import *
import ai
import othello_board


print("Input board size")
g_board_size = int(input())
g_board_size = g_board_size//2*2
# g_board_size = 4
base_game_init(g_board_size)

print("Input maximum depth for minimax value")
g_depth = int(input())
# g_depth = 12

print("Show Minimax AI steps/paths? (Y/N)")
show_ai_steps = True if input() in ["Y", "YES", "y", "Yes"] else False
# show_ai_steps = True
print("Showing Minimax steps") if show_ai_steps else print("Not showing steps")
ai.init(g_depth, show_ai_steps)

# Print board state
g_board = [[0 for i in range(g_board_size)] for j in range(g_board_size)]
# Set middle pieces to black and white
mid = g_board_size//2
g_board[mid-1][mid-1] = BLACK
g_board[mid-1][mid] = WHITE
g_board[mid][mid-1] = WHITE
g_board[mid][mid] = BLACK

cur_color = WHITE
g_move_num = 0
agent = {WHITE: "Player", BLACK: "Minimax"}  # Naive, Player, Minimax
# agent = {WHITE: "Minimax", BLACK: "Player"}  # Naive, Player, Minimax
othello_board.init(g_board)
while True:
    g_move_num += 1
    g_valid_moves = get_valid_moves(g_board, cur_color)
    # Check if game is finished
    if len(g_valid_moves) == 0:
        if len(get_valid_moves(g_board, enemy_color(cur_color))) == 0:
            finish_game(g_board)
            break
        else:
            print('Currnet player have no more moves available')
            cur_color = enemy_color(cur_color)
            continue

    # Get choice
    if agent[cur_color] == "Naive":
        print("Naive AI Move")
        ai.start(g_move_num)
        valid_move = ai.naive(g_valid_moves)
    elif agent[cur_color] == "Minimax":
        print("Minimax AI Move")
        ai.start(g_move_num)
        print("color: ", cur_color)
        valid_move = ai.minimax(g_board, cur_color)
    else:
        print("Player Move")
        othello_board.refresh_board(g_board, g_valid_moves, cur_color)
        # valid_move = get_choice(g_valid_moves, cur_color)
        othello_board.start_listening(g_valid_moves, cur_color)
        valid_move = othello_board.get_choice()
    make_move(g_board, valid_move, cur_color)
    cur_color = enemy_color(cur_color)

