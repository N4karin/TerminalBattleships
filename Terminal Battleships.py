import os
import platform

# Declaring these variables globally so all methods can access it.
global active_player
global p1_name
global p2_name

# Defining clear() function using lambdas after requesting OS
if platform.system() == "Windows":
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')


# Defining both boards from each players perspective (4 in total)
board1_p1Turn = []
board1_p2Turn = []
board2_p1Turn = []
board2_p2Turn = []

# Variable holding which player's turn it is (1: player 1, 2: player 2)
active_player = 1

# Counter holding info on how many tiles of S are left, decreases after taking a hit
player1_remaining = 17
player2_remaining = 17

# Dictionary to convert letter into their corresponding column numbers
alphabet_index = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
        "i": 8,
        "j": 9,
}


# Function displaying left and right boards, the boards displayed depend on whose turn it is.
# Boards are printed row by row to allow displaying them side by side instead of above/below.

def print_boards():
    clear()
    if active_player == 1:
        left = board1_p1Turn
        right = board2_p1Turn
    else:
        left = board2_p2Turn
        right = board1_p2Turn

    print("   ---- YOUR BOARD ---- |  ---- ENEMY BOARD ----  ")
    print("   A B C D E F G H I J  |     A B C D E F G H I J")
    for row in range(10):
        print("%d  %s  |  %d  %s" % (row, " ".join(left[row]), row, " ".join(right[row])))


# Function processing a guess made by the active player (determined by global variable activePlayer)

def apply_guess(coord):
    try:
        # sanitize input and convert it into ints for further processing.
        # Thanks to that, the player is free to decide how they input their coordinates as long as the
        # order of the coordinates adheres to [row][col], regardless of whitespaces
        coord = coord.lower().replace(" ", "")
        row = int(coord[0])
        col = alphabet_index.get(coord[1])

        # check whether guess is a hit or not, result will be "X" for hit or "O" miss
        result = check_hit(row, col)

        # carry out if player 1 is at turn
        if active_player == 1:
            # Players should only be able to guess coordinates not already guessed
            if board2_p1Turn[row][col] == "X" or board2_p1Turn[row][col] == "O":
                print("You have already shot at this position!")
                apply_guess(input("Please try another position: "))
                return

            board2_p1Turn[row][col] = result
            board2_p2Turn[row][col] = result

            # procedure for a hit
            if result == "X":
                print_boards()
                check_win_cond()
                # recursive function call on hit
                apply_guess(input("Hit! Enter follow-up shot: "))

        # carry out if player 2 is at turn
        else:
            if board1_p2Turn[row][col] == "X" or board1_p1Turn[row][col] == "O":
                print("You have already shot at this position!")
                apply_guess(input("Please try another position: "))
                return

            board1_p1Turn[row][col] = result
            board1_p2Turn[row][col] = result

            if result == "X":
                print_boards()
                check_win_cond()
                apply_guess(input("Hit! Enter follow-up shot: "))
    # in case a player mixes up row and col or enters some other invalid input
    except:
        print("Invalid coordinates!")
        apply_guess(input("Please provide coordinates as [row][col]: "))


# checks whether a guessed coordinate hits a ship in the attacked board.
# returns a value corresponding to a hit or a miss.

def check_hit(row, col):
    global player1_remaining
    global player2_remaining
    if active_player == 1:
        if board2_p2Turn[row][col] == "S":
            player2_remaining -= 1
            return "X"
        else:
            return "O"
    else:
        if board1_p1Turn[row][col] == "S":
            player1_remaining -= 1
            return "X"
        else:
            return "O"


# Checks, whether one player has no ship tiles remaining. If that's the case, a winner
# is announced whereupon the program will close without clearing the console of the latest game state.

def check_win_cond():
    global p1_name
    global p2_name

    if player1_remaining == 0:
        print("%s has sunken all ships of %s and wins the game!" % (p2_name, p1_name))
        # We use os._exit(1) instead of exit() to prevent raising an exception because the function calling
        # check_win_cond() is handling all exceptions as if they were a false input.
        os._exit(1)

    if player2_remaining == 0:
        print("%s has sunken all ships of %s and wins the game!" % (p1_name, p2_name))
        os._exit(1)


# Function to place a ship at coord with length in tiles and direction (e for east and s for south).

def place_ship(coord, length):
    try:
        coord = coord.lower().replace(" ", "")

        if active_player == 1:
            target_board = board1_p1Turn
        else:
            target_board = board2_p2Turn

        row = int(coord[0])
        col = alphabet_index.get(coord[1])
        direction = coord[2]

        # Checking, whether the ship placed at the position would overlap with another ship
        for x in range(length):
            if direction == "e":
                if target_board[row][col + x] == "S":
                    print("Your ship placement would collide with an already existing ship!")
                    place_ship(input("Please choose another position for your ship: "), length)
                    return
            if direction == "s":
                if target_board[row + x][col] == "S":
                    print("Your ship placement would collide with an already existing ship!")
                    place_ship(input("Please choose another position for your ship: "), length)
                    return

        for x in range(length):
            if direction == "e":
                target_board[row][col + x] = "S"
            else:
                target_board[row + x][col] = "S"
    except:
        print("Invalid coordinates or ship is not completely in the board!")
        place_ship(input("Please provide coordinates as [row][col][e/s]: "), length)


def main():
    # accessing global variables
    global active_player
    global p1_name
    global p2_name

    # set player names
    p1_name = input("Player 1 name: ")
    p2_name = input("Player 2 name: ")

    # fill boards with plain water
    for x in range(10):
        board1_p1Turn.append(["~"] * 10)
        board1_p2Turn.append(["~"] * 10)
        board2_p1Turn.append(["~"] * 10)
        board2_p2Turn.append(["~"] * 10)

    # player 1 ship placement
    active_player = 1
    print_boards()
    place_ship(input("%s - Place your carrier (5 tiles) [row][col][e/s]: " % p1_name), 5)
    print_boards()
    place_ship(input("%s - Place your battleship (4 tiles): " % p1_name), 4)
    print_boards()
    place_ship(input("%s - Place your destroyer (3 tiles): " % p1_name), 3)
    print_boards()
    place_ship(input("%s - Place your submarine (3 tiles): " % p1_name), 3)
    print_boards()
    place_ship(input("%s - Place your patrol boat (2 tiles): " % p1_name), 2)
    print_boards()

    # player 2 ship placement
    input("This is the board of %s, press enter to begin setting up board of %s" % (p1_name, p2_name))
    active_player = 2
    print_boards()
    place_ship(input("%s - Place your carrier (5 tiles) [row][col][e/s]: " % p2_name), 5)
    print_boards()
    place_ship(input("%s - Place your battleship (4 tiles): " % p2_name), 4)
    print_boards()
    place_ship(input("%s - Place your destroyer (3 tiles): " % p2_name), 3)
    print_boards()
    place_ship(input("%s - Place your submarine (3 tiles): " % p2_name), 3)
    print_boards()
    place_ship(input("%s - Place your patrol boat (2 tiles): " % p2_name), 2)
    print_boards()
    input("This is the board of %s, press enter to begin first turn of %s" % (p2_name, p1_name))

    # Main Game Loop
    while True:
        active_player = 1
        print_boards()
        guess = input("%s guessing: " % p1_name)
        apply_guess(guess)
        print_boards()
        input("Press enter to end your turn")
        clear()
        input("Press enter if only %s is present" % p2_name)

        active_player = 2
        print_boards()
        guess = input("%s guessing: " % p2_name)
        apply_guess(guess)
        print_boards()
        input("Press enter to end your turn")
        clear()
        input("Press enter if only %s is present" % p1_name)


# making sure main method is called on start

if __name__ == '__main__':
    main()
