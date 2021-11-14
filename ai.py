# Naive och Minimax AI för othello
import copy
from base_game import enemy_color, get_valid_moves, make_move, evaluator
import ai_gui

g_depth = None
g_move_num = None
g_show_steps = False


def init(depth, show_steps):
    '''
    Initiera AI
    '''
    global g_depth, g_show_steps
    g_depth = depth
    g_show_steps = show_steps


def start(move_num):
    global g_move_num
    g_move_num = move_num


def naive(valid_moves):
    '''
    Returnerar det första möjliga draget
    '''
    return valid_moves[0]


def minimax(board, cur_minimax_color):
    '''
    Minimax-algoritm
    '''
    ai_gui.close_window()
    max_depth = g_depth + g_move_num

    def _minimax(cur_board, cur_color, cur_depth, isMax, alpha, beta, parent_has_no_moves=False):
        if g_show_steps:
            ai_gui.add_minimax_board(cur_board, cur_depth - g_move_num, isMax, False)
        if max_depth == cur_depth:
            score = evaluator(cur_board, cur_minimax_color)
            if g_show_steps:
                ai_gui.add_score(score, cur_depth - g_move_num + 1, isMax)
            return score, None

        valid_moves = get_valid_moves(cur_board, cur_color)
        if len(valid_moves) == 0:
            if parent_has_no_moves:
                score = evaluator(cur_board, cur_minimax_color)
                if g_show_steps:
                    ai_gui.add_score(score, cur_depth - g_move_num + 1, isMax)
            else:
                score, move = _minimax(
                    copy.deepcopy(cur_board), enemy_color(cur_color), cur_depth + 1, not isMax,
                    alpha, beta, True)
            if g_show_steps:
                ai_gui.add_score(score, cur_depth - g_move_num + 1, isMax)
            return score, None

        if isMax:
            alpha_move = valid_moves[0]
            for i, move in enumerate(valid_moves):
                board_copy = copy.deepcopy(cur_board)
                make_move(board_copy, move, cur_color)

                cur_score, cur_move = _minimax(board_copy, enemy_color(cur_color), cur_depth + 1, False, alpha, beta)
                if cur_score > alpha:
                    alpha = cur_score
                    alpha_move = move
                if beta <= alpha:
                    if g_show_steps and len(valid_moves) - 1 > i:
                        board_copy2 = copy.deepcopy(cur_board)
                        make_move(board_copy2, valid_moves[i + 1], cur_color)
                        if g_show_steps:
                            ai_gui.add_minimax_board(board_copy2, cur_depth - g_move_num + 1, not isMax, True)
                    break
            if g_show_steps:
                ai_gui.add_score(alpha, cur_depth - g_move_num + 1, isMax)
            return alpha, alpha_move
        else:
            beta_move = valid_moves[0]
            for i, move in enumerate(valid_moves):
                board_copy = copy.deepcopy(cur_board)
                make_move(board_copy, move, cur_color)

                cur_score, cur_move = _minimax(board_copy, enemy_color(cur_color), cur_depth + 1, True, alpha, beta)
                if beta > cur_score:
                    beta = cur_score
                    beta_move = move
                if beta <= alpha:
                    # Gå till nästa nod
                    if g_show_steps and len(valid_moves) - 1 > i:
                        board_copy2 = copy.deepcopy(cur_board)
                        make_move(board_copy2, valid_moves[i + 1], cur_color)
                        if g_show_steps:
                            ai_gui.add_minimax_board(board_copy2, cur_depth - g_move_num + 1, not isMax, True)
                    break
            if g_show_steps:
                ai_gui.add_score(beta, cur_depth - g_move_num + 1, isMax)
            return beta, beta_move

    if g_show_steps:
        ai_gui.init(cur_minimax_color)

    best_score, best_move = _minimax(copy.deepcopy(board), cur_minimax_color, g_move_num, True, float("-inf"),
                                     float("inf"))
    if g_show_steps:
        ai_gui.finish_board()
    return best_move
