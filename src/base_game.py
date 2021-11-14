# Othellos spel-logik
from othello_constants import *
# Konstanter för riktningar
UP = (-1, 0)
UP_RIGHT = (-1, 1)
RIGHT = (0, 1)
DOWN_RIGHT = (1, 1)
DOWN = (1, 0)
DOWN_LEFT = (1, -1)
LEFT = (0, -1)
UP_LEFT = (-1, -1)

g_board_size = None
g_board_choices = None
g_alphabet_list = None


def base_game_init(board_size):
    '''
    Initiera spelet.
    '''
    global g_board_size, g_alphabet_list, g_board_choices
    g_board_size = board_size
    g_alphabet_list = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    g_board_choices = [["%c%d " % (g_alphabet_list[i], j) for i in range(g_board_size)] for j in range(g_board_size)]


def evaluator(board, color):
    '''
    Kollar hur många poäng den angivna spelaren har.
    '''
    cur_score = 0
    for row in board:
        for cell in row:
            if cell == color:
                cur_score += 1
    return cur_score


def finish_game(board):
    '''
    Avslutar spelet.
    '''
    print('Inga fler drag finns. Spelet är över.')
    black_count = 0
    white_count = 0
    for row in board:
        for cell in row:
            if cell == BLACK:
                black_count += 1
            elif cell == WHITE:
                white_count += 1

    if black_count > white_count:
        print("Svart vann")
    elif white_count > black_count:
        print("Vit vann")
    else:
        print("Oavgjort")


def print_choices(board, valid_moves):
    '''
    Printar alternativen.
    '''
    move_coords = [valid_move["coordinate"] for valid_move in valid_moves]
    for i, rows in enumerate(board):
        for j, cell in enumerate(rows):
            if (i, j) in move_coords:
                print(g_board_choices[i][j], end='')
            elif cell == WHITE:
                print('WW ', end='')
            elif cell == BLACK:
                print('BB ', end='')
            elif cell == 0:
                print('-- ', end='')
            else:
                print(cell, end='')
        print()


def get_choice(valid_moves, color):
    '''
    Returnerar den angivna spelarens drag.
    '''
    move_coords = [valid_move["coordinate"] for valid_move in valid_moves]

    choice = input()
    j = ord(choice[0]) - ord('a')
    i = ord(choice[1]) - ord('0')
    print(i, j)
    if (i, j) in move_coords:
        return valid_moves[move_coords.index((i, j))]
    else:
        print("Inte ett giltigt drag")
        return get_choice(valid_moves, color)


def enemy_color(color):
    '''
    Returnerar motståndaren för den angivna spelaren.
    '''
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def get_valid_moves(board, color):
    '''
    Returnerar alla lagliga drag.
    '''
    res_moves = []
    for iRow, row in enumerate(board):
        for iCol, cell in enumerate(row):
            if cell != 0:
                continue
            move = check_valid_move(board, color, (iRow, iCol))
            if move is not None:
                res_moves.append(move)
    return res_moves


def make_move(board, valid_move, color):
    '''
    Gör ett drag
    '''
    def flip_direction(i, j, dir_tuple, player_color):
        '''
        Vänder pjäserna enligt spelets regler
        '''
        diffI, diffJ = dir_tuple
        # Placera start pjäserna.
        board[i][j] = player_color
        i, j = move_over(i, j, diffI, diffJ)
        # Vänder tills en pjäs av andra färgen hittas.
        while is_in_range(i, j):
            if board[i][j] == player_color:
                break
            board[i][j] = player_color
            i, j = move_over(i, j, diffI, diffJ)

    directions = valid_move['direction']
    (tmpI, tmpJ) = valid_move['coordinate']
    for direction in directions:
        flip_direction(tmpI, tmpJ, direction, color)


def check_valid_move(board, color, coordinate):
    '''
    Kollor om den angivna koordinaten är ett lagligt drag för den angivna färgen eller inte.
    '''
    result = {"coordinate": coordinate, "amount": 0, "direction": []}

    # Returnerar 0 om draget är olagligt.
    # else; returnerar mängden fiende pjäser som vänds över vid draget
    def check_line(i, j, direction):
        diffI, diffJ = direction
        i, j = move_over(i, j, diffI, diffJ)
        if is_in_range(i, j) and board[i][j] == enemy_color(color):
            i, j = move_over(i, j, diffI, diffJ)  # move 1 step
            count = 1
            same_color_found = False
            # Hitta pjäs av samma färg
            while is_in_range(i, j):
                if board[i][j] == color:
                    same_color_found = True
                    break
                elif board[i][j] != enemy_color(color):
                    break
                i, j = move_over(i, j, diffI, diffJ)
                count += 1
            # loop klar
            if same_color_found:
                # Om det fanns en pj's av samma färg returnera count
                return count
            else:
                # Om det inte fanns en pjäs av samma färg, returnera 0
                return 0
        else:
            # Om grann-pjäsen inte är en fiende pjäs är draget inte lagligt
            return 0

    iStart, jStart = coordinate
    check_line_results = [
        check_line(iStart, jStart, UP),
        check_line(iStart, jStart, UP_RIGHT),
        check_line(iStart, jStart, RIGHT),
        check_line(iStart, jStart, DOWN_RIGHT),
        check_line(iStart, jStart, DOWN),
        check_line(iStart, jStart, DOWN_LEFT),
        check_line(iStart, jStart, LEFT),
        check_line(iStart, jStart, UP_LEFT)
    ]
    # Kollar efter drag åt alla håll
    if check_line_results[0] > 0:
        result["amount"] += check_line_results[0]
        result["direction"].append(UP)
    if check_line_results[1] > 0:
        result["amount"] += check_line_results[1]
        result["direction"].append(UP_RIGHT)
    if check_line_results[2] > 0:
        result["amount"] += check_line_results[2]
        result["direction"].append(RIGHT)
    if check_line_results[3] > 0:
        result["amount"] += check_line_results[3]
        result["direction"].append(DOWN_RIGHT)
    if check_line_results[4] > 0:
        result["amount"] += check_line_results[4]
        result["direction"].append(DOWN)
    if check_line_results[5] > 0:
        result["amount"] += check_line_results[5]
        result["direction"].append(DOWN_LEFT)
    if check_line_results[6] > 0:
        result["amount"] += check_line_results[6]
        result["direction"].append(LEFT)
    if check_line_results[7] > 0:
        result["amount"] += check_line_results[7]
        result["direction"].append(UP_LEFT)

    if result["amount"] == 0:
        return None
    return result


def is_in_range(i, j):
    '''
    Är koordinaten in range
    '''
    return g_board_size > i >= 0 and g_board_size > j >= 0


def move_over(mv_i, mv_j, diffI, diffJ):
    mv_i += diffI
    mv_j += diffJ
    return mv_i, mv_j


def print_board_helper(board, color):
    valid_moves = get_valid_moves(board, color)
    moves = [valid_move["coordinate"] for valid_move in valid_moves]
    print_choices(board, moves)
