import numpy as np
import random
import pygame
import math

PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
ROW_COUNT = 6
COLUMN_COUNT = 7
pygame.init()
SQUARESIZE = 100
WINDOW_LENGH = 4
EMPTY = 0
RADIUS = int((SQUARESIZE / 2) - 5)
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT+1) * SQUARESIZE

window = pygame.display.set_mode((WIDTH,HEIGHT))


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
                                                # h=change these values to tune ai
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) ==1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5
    if window.count(opp_piece) == 3 and window.count(EMPTY) ==1:        # block
        score -= 80

    return score
    
def score_position(board, piece):
    score = 0
    # score center
    
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 6
   
    
    # score hrozontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            ai_window = row_array[c:c+WINDOW_LENGH]
            score += evaluate_window(ai_window,piece)

    # score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            ai_window = col_array[r:r+WINDOW_LENGH]
            score += evaluate_window(ai_window,piece)

    # score positive diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            ai_window = [board[r+i][c+i] for i in range(WINDOW_LENGH)]
            score += evaluate_window(ai_window,piece)

    # score negative diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            ai_window = [board[r+3-i][c+i] for i in range(WINDOW_LENGH)]
            score += evaluate_window(ai_window,piece)
    
        
    return score

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board,col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    best_score = -8000
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col
        

def drawboard(board):
    pygame.draw.rect(window,(0,0,255),(0,SQUARESIZE,WIDTH,HEIGHT))
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.circle(window,(0,0,0),(int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(window,(255,0,0),(int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(window,(255,255,0),(int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
    pygame.display.update()
    
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # check horixontal locations for winning move           ### try build more efficient winning function ###
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # check for positive sloped disgonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # check for negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


board = create_board()
game_over = False
myFont = pygame.font.SysFont("monospace",75)
turn = random.randint(PLAYER,AI)

drawboard(board)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window,(0,0,0),(0,0,WIDTH,SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(window,(255,0,0),(posx, int(SQUARESIZE/2)),RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # ask for player 1 input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row, col, PLAYER_PIECE)
                    if winning_move(board, turn + 1):
                        drawboard(board)
                        pygame.draw.rect(window,(0,0,0),(0,0,WIDTH,SQUARESIZE))
                        label = myFont.render("You Win!!!",1,(255,0,0))
                        window.blit(label,(20,10))
                        pygame.display.update()
                        game_over = True
                    drawboard(board)
                    turn += 1
                    turn = turn % 2       # look into this function

    if turn == AI and not game_over:
        #col = random.randint(0, COLUMN_COUNT-1)
        col = pick_best_move(board, AI_PIECE)
        if is_valid_location(board,col):
            pygame.time.wait(500)
            row = get_next_open_row(board,col)
            drop_piece(board,row, col, AI_PIECE)
            if winning_move(board, turn + 1):
                pygame.draw.rect(window,(0,0,0),(0,0,WIDTH,SQUARESIZE))
                label = myFont.render("Sorry, Computer Wins!!!",1,(255,255,0))
                window.blit(label,(20,10))
                pygame.display.update()
                game_over = True

            drawboard(board)
            

            turn += 1
            turn = turn % 2       # look into this function

pygame.time.wait(3000)   
pygame.quit()
