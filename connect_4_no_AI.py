import numpy as np
import pygame
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
pygame.init()
SQUARESIZE = 100
RADIUS = int((SQUARESIZE / 2) - 5)
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT+1) * SQUARESIZE

window = pygame.display.set_mode((WIDTH,HEIGHT))


def drawboard(board):
    pygame.draw.rect(window,(0,0,255),(0,SQUARESIZE,WIDTH,HEIGHT))
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.circle(window,(0,0,0),(int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(window,(255,0,0),(int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif board[r][c] == 2:
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
turn = 0
myFont = pygame.font.SysFont("monospace",75)

drawboard(board)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window,(0,0,0),(0,0,WIDTH,SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(window,(255,0,0),(posx, int(SQUARESIZE/2)),RADIUS)
            if turn == 1:
                pygame.draw.circle(window,(255,255,0),(posx, int(SQUARESIZE/2)),RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # ask for player 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row, col, 1)

            # ask for player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row, col, 2)

            drawboard(board)
            if winning_move(board, turn + 1):
                pygame.draw.rect(window,(0,0,0),(0,0,WIDTH,SQUARESIZE))
                if turn + 1 == 1:
                    colour = (255,0,0)
                else:
                    colour = (255,255,0)
                label = myFont.render("Player " + str(turn + 1) + " Wins!!!",1,colour)
                window.blit(label,(20,10))
                pygame.display.update()
                print("End")
                game_over = True

            turn += 1
            turn = turn % 2       # look into this function

pygame.time.wait(3000)   
pygame.quit()
