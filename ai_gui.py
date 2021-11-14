# Visa minimax steg
from tkinter import *
from othello_constants import *
from base_game import evaluator

g_root = None
g_canvas = None

g_ai_color = None
g_show_steps = False
g_board_size = 0
g_tile_size = 20

minimax_coords = {}


def init(ai_color):
    '''
    Initiera GUI som visar minimax-trädet
    '''
    global g_root, g_canvas, g_ai_color
    g_ai_color = ai_color
    g_root = Tk()
    w, h = g_root.winfo_screenwidth(), g_root.winfo_screenheight()
    g_root.geometry("%dx%d+0+0" % (w, h))

    # Initiera canvas
    g_root.title("Minimax AI Steps")
    frame = Frame(g_root, width=20, height=20)
    frame.pack(expand=True, fill=BOTH)
    g_canvas = Canvas(frame, bg='#FFFFFF', width=600, height=600)
    hbar = Scrollbar(frame, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=g_canvas.xview)
    vbar = Scrollbar(frame, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=g_canvas.yview)
    g_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    g_canvas.pack(side=LEFT, expand=True, fill=BOTH)


last_board_x_coords = {0: 0}
xOffset = g_tile_size
yOffset = g_tile_size


def add_minimax_board(board, level, isMax, is_pruned):
    '''
    Lägg till ett bräde i trädet
    '''
    global g_board_size, xOffset, yOffset
    xOffset = (g_board_size + 2) * g_tile_size
    yOffset = (g_board_size + 2) * g_tile_size
    level += 1
    if level == 1:
        g_board_size = len(board)
        minimax_coords[level] = 0
        draw_board(board, level, 0, 0, isMax, is_pruned)
    # Om index är out of range
    elif len(minimax_coords) < level:
        minimax_coords[level] = minimax_coords[level-1]
        draw_board(board, level, minimax_coords[level], yOffset*(level-1), isMax, is_pruned)
    else:
        minimax_coords[level] = minimax_coords[level] + xOffset
        for i in range(level, 1, -1):
            minimax_coords[i-1] = minimax_coords[i]
        if is_pruned:
            # Om is_pruned så har det nya brädet samma koordinater som det nuvarande brädet.
            for i in range(level, len(minimax_coords)+1):
                minimax_coords[i+1] = minimax_coords[i]
        else:
            # Om inte is_pruned så har det nya brädet samma koordinator som det nuvarande brädet minus 1.
            for i in range(level, len(minimax_coords)+1):
                minimax_coords[i+1] = minimax_coords[i] - xOffset
        draw_board(board, level, minimax_coords[level], yOffset*(level-1), isMax, is_pruned)


def draw_board(board, level, start_x, start_y, isMax, is_pruned):
    '''
    Rita nytt bräde
    '''
    last_board_x_coords[level] = start_x
    # Börja rita brädet
    board_color = 'DARKGREEN' if is_pruned is False else 'DARKRED'
    g_canvas.create_rectangle(
        start_x, start_y,
        start_x + g_tile_size * g_board_size, start_y + g_tile_size * g_board_size,
        width=1, fill=board_color)
    for i in range(1, g_board_size):  # Rita vertikala linjer
        g_canvas.create_line(
            start_x + g_tile_size * i, start_y,
            start_x + g_tile_size * i, start_y + g_tile_size * g_board_size,
            width=1, fill='BLACK')
    for i in range(1, g_board_size):  # Rita horizontella linjer
        g_canvas.create_line(
            start_x, start_y + g_tile_size * i,
            start_x + g_tile_size * g_board_size, start_y + g_tile_size * i,
            width=1, fill='BLACK')

    # Börja rita othello-pjäserna
    for i in range(g_board_size):
        for j in range(g_board_size):
            sx = (j + 0.5) * g_tile_size + start_x
            sy = (i + 0.5) * g_tile_size + start_y
            if board[i][j] == BLACK:
                g_canvas.create_oval(
                    sx - g_tile_size/3, sy - g_tile_size/3,
                    sx + g_tile_size/3, sy + g_tile_size/3,
                    fill='BLACK')
            elif board[i][j] == WHITE:
                g_canvas.create_oval(
                    sx - g_tile_size/3, sy - g_tile_size/3,
                    sx + g_tile_size/3, sy + g_tile_size/3,
                    fill='WHITE')

    # Börja rita minimax-linjer
    g_canvas.create_line(
        last_board_x_coords[level-1] + g_tile_size * g_board_size // 2,
        start_y - (yOffset - g_board_size*g_tile_size),  # Y-koordinaten ovanför  brädets slut
        last_board_x_coords[level] + g_tile_size * g_board_size // 2,
        start_y,
        width=1, fill='darkblue')


def add_score(score, level, isMax):
    '''
    Rita poäng-texten för nuvarande bräde
    '''
    color = "black" if isMax else "red"
    g_canvas.create_text(
        last_board_x_coords[level],
        yOffset*(level-1)+g_board_size*g_tile_size,
        fill=color, font="Times 12", anchor=NW,
        text="Score: "+str(score))


def finish_board():
    global minimax_coords
    g_canvas.config(scrollregion=g_canvas.bbox("all"))
    minimax_coords = {}

def close_window():
    '''
    Stänger ner ai_gui fönstret om det existerar.
    '''
    if (g_root != None):
        try:
            g_root.destroy()
        except:
            pass
