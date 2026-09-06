import numpy as np
board=np.zeros((3,3),dtype=int)
print(board)

def showBoard(board):
    keys={0:" ",1:"X",-1:"O"}
    for r in range(3):
        row=" | ".join(keys[val] for val in board[r])
        print(" "+row)
        if(r<2):
            print("---|---|---")

showBoard(board)

def checkWinner(board):
    if 3 in np.sum(board,axis=0) or 3 in np.sum(board,axis=1):
        return "X"
    if -3 in np.sum(board,axis=0) or -3 in np.sum(board,axis=1):
        return "O"
    if np.trace(board)==3 or np.trace(np.fliplr(board))==3:
        return "X"
    if np.trace(board)==-3 or np.trace(np.fliplr(board))==-3:
        return "O"
    if not 0 in board:
        return "Draw"
    return None

current = 1
print("Welcome to tic tac toe")
showBoard(board)
while True:
    try:
        row=int(input("Enter your row:(0/1/2) "))
        col=int(input("Enter your col:(0/1/2)"))
    except ValueError:
        print("Pls enter only interger value")
        continue

    if(row<0 or row>2 or col<0 or col>2):
        print("Value of row and col should be 0/1/2 only")
        continue

    if(board[row,col]!=0):
        print("pls select enother box as it is already taken")
        continue

    board[row,col]=current
    showBoard(board)
    current=-current
    result=checkWinner(board)

    if result is not None:
        if(result=="Draw"):
            print("OOPS its a draw")
        else:
            print(result+" wins")

        break
    
    

    
