import os
import platform
global active_player
global p1_name
global p2_name

if platform.system() == "Windows":
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

board1_p1Turn = []
board1_p2Turn = []
board2_p1Turn = []
board2_p2Turn = []
active_player = 1

player1_remaining = 17
player2_remaining = 17

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


def apply_guess(coord):
    try:
        coord = coord.lower().replace(" ", "")
        row = int(coord[0])
        col = alphabet_index.get(coord[1])

        result = check_hit(row, col)

        if active_player == 1:
            if board2_p1Turn[row][col] == "X" or board2_p1Turn[row][col] == "O":
                print("You have already shot at this position!")
                apply_guess(input("Please try another position: "))
                return

            board2_p1Turn[row][col] = result
            board2_p2Turn[row][col] = result

            if result == "X":
                print_boards()
                check_win_cond()
                apply_guess(input("Hit! Enter follow-up shot: "))
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
    except:
        print("Invalid coordinates!")
        apply_guess(input("Please provide coordinates as [row][col]: "))


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


def check_win_cond():
    global p1_name
    global p2_name

    if player1_remaining == 0:
        print("%s has sunken all ships of %s and wins the game!" % (p2_name, p1_name))
        os._exit(1)

    if player2_remaining == 0:
        print("%s has sunken all ships of %s and wins the game!" % (p1_name, p2_name))
        os._exit(1)


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
    global active_player
    global p1_name
    global p2_name
    p1_name = input("Player 1 name: ")
    p2_name = input("Player 2 name: ")

    for x in range(10):
        board1_p1Turn.append(["~"] * 10)
        board1_p2Turn.append(["~"] * 10)
        board2_p1Turn.append(["~"] * 10)
        board2_p2Turn.append(["~"] * 10)

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


if __name__ == '__main__':
    main()
