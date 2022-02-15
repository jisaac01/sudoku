
import math

def solved(working_board):
    for space in working_board:
        if space == '': return False
    return True

def row_num(n):
    return math.floor(n / 9)

def col_num(n):
    return n % 9

# remove empty values
def squish(arry):
    return [space for space in arry if space != '']

def get_row(n, board):
    #print("row " + str(row_num(n)))
    raw_row = board[row_num(n) * 9: row_num(n) * 9 + 9]
    return squish(raw_row)

def get_column(n, board):
    #print("column " + str(col_num(n)))
    raw_column = []
    for i in range(len(board)):
        if i % 9 == col_num(n): raw_column.append(board[i])
    return squish(raw_column)

def get_square(n, board):
    col = math.floor(n / 3) % 3
    row = math.floor(n / 27)
    start_index = (row * 27) + (col * 3)
    #print(f"square for {n} row {row} col {col} start_index {start_index}")
    row_1 = board[start_index : start_index + 3]
    # print(row_1)
    row_2 = board[start_index + 9 : start_index + 9 + 3]
    # print(row_2)
    row_3 = board[start_index + 18 : start_index + 18 + 3]
    # print(row_3)
    return squish(row_1 + row_2 + row_3)

def print_board(board):
    # if debug == False:
    #     print("= = =   = = =   = = =")
    #     for i in range(len(board)):
    #         print(".", end=' ') if board[i] == '' else print(board[i],end=' ')
    #         if (i+1) % 3 == 0: print("|", end=' ')
    #         if (i+1) % 9 == 0: print("")
    #         if (i+1) % 27 == 0: print("- - -   - - -   - - -")
    # else: 
    for i in range(len(board)):
        print(".", end='') if board[i] == '' else print(board[i],end='')
        if (i+1) % 9 == 0: print(" ", end=' ')
    print('')

# open the file
f = open("hard.txt", "r")
original_board = f.read()
print(len(original_board))

# read the contents into a list 
working_board = []
for space in original_board:
    if space == '\n': continue
    if space == '.': space = ''
    working_board.append(space)

print_board(original_board)
print_board(working_board)

debug = False
forward = True
current_square = 0;
all_values = {'1','2','3','4','5','6','7','8','9'}
working_values = {}

while not solved(working_board):
    if debug == True:
        print("<------------------------------------------------------------------------\n")
        print(working_board[current_square])
        print(original_board[current_square])
        print("current_square " + str(current_square))
        print(get_row(current_square, working_board))
        print(get_column(current_square, working_board))
        print(get_square(current_square, working_board))

    if working_board[current_square] == original_board[current_square]:
        current_square = current_square+1 if forward else current_square-1
        continue

    if current_square not in working_values:
        if debug == True: print("Initializing")
        working_values[current_square] = {
          "visited" : 1,
          "possible_values" : set(),
          "used_values" : set(),
          "tried_values" : set()
        }
    else:
        working_values[current_square]["visited"] += 1 
        working_values[current_square]["tried_values"].add(working_board[current_square])
        working_board[current_square] = ''

    used_values = set(get_row(current_square, working_board) +
        get_column(current_square, working_board) +
        get_square(current_square, working_board))
    possible_values = all_values - used_values - working_values[current_square]["tried_values"]

    working_values[current_square]["possible_values"] = possible_values
    working_values[current_square]["used_values"] = used_values

    if debug == True:
        print(f"used_values: {used_values}")
        print(f"possible_values: {possible_values}")
        print(f"tried_values: {working_values[current_square]['tried_values']}")
        print(f"visited: {working_values[current_square]['visited']}")

        if working_values[current_square]["visited"] > 9:
            print("We've entered the twilight zone")

    if len(possible_values) == 0:
        working_values[current_square]['tried_values'] = set()
        forward = False
 
        if current_square == 0:
            print("No more possible solutions")
            break

        current_square = current_square - 1
        
        print_board(working_board)

        continue
    else:
        forward = True
        working_board[current_square] = possible_values.pop()
        if debug == True:
            print(f"setting square {current_square} to {working_board[current_square]}")
            print("------------------------------------------------------------------------>\n")

        current_square = current_square + 1
        continue


print_board(original_board)
print_board(working_board)
