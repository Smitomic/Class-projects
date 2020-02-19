from random import choice
from typing import Tuple, List, Optional


def new_playground(size: int) -> List[List[str]]:
    row = []
    for _ in range(size):
        collumn = []
        for _ in range(size):
            collumn.append(" ")
        row.append(collumn)
    return row


def init_playground(playground: List[List[str]]) -> List[List[str]]:
    half = (len(playground) // 2) - 1
    playground[half][half] = "X"
    playground[half][half + 1] = "O"
    playground[half + 1][half] = "O"
    playground[half + 1][half + 1] = "X"
    return playground


def get(playground: List[List[str]], row: int, col: int) -> str:
    return playground[row][col]


def set_symbol(playground: List[List[str]], row: int,
               col: int, symbol: str) -> None:
    playground[row][col] = symbol


def draw(playground: List[List[str]]) -> None:
    length = len(playground)
    for i in range(length):
        print("   +", end="")
        print("---+" * length)
        print("", chr(ord('A')+i), "|", end="")
        for j in range(length):
            print(" ", end="")
            print(playground[i][j], "|", end="")
        print()
    print("   +", end="")
    print("---+" * length)
    print("   ", end="")
    for k in range(length):
        if k < 10:
            print(" ", k, end=" ")
        else:
            print(" ", k, end="")
    print()


def inside_of_board(row: int, col: int, playground: List[List[str]]) -> bool:
    size = len(playground) - 1
    return 0 <= row <= size and 0 <= col <= size


def get_enemy_symbol(symbol: str) -> str:
    if symbol == "X":
        return "O"
    else:
        return "X"


def generate_flips_list(x: int, y: int, symbol: str, xs: int, ys: int,
                        row: int, col: int, flips: List[List[int]],
                        playground: List[List[str]]) -> None:
    if playground[x][y] == symbol:
        while True:
            x -= xs
            y -= ys
            if x == row and y == col:
                break
            flips.append([x, y])


def check_move_and_get_flips(playground: List[List[str]], row: int, col: int,
                             symbol: str) -> Optional[List[List[int]]]:
    enemy = get_enemy_symbol(symbol)
    flips: List[List[int]] = []
    if not inside_of_board(row, col, playground)\
            or playground[row][col] != " ":
        return None
    for xs, ys in [[-1, -1], [0, -1], [-1, 0], [0, 1],
                   [1, 0], [1, 1], [1, -1], [-1, 1]]:
        x, y = row, col
        x += xs
        y += ys
        while inside_of_board(x, y, playground) and playground[x][y] == enemy:
            x += xs
            y += ys
        if not inside_of_board(x, y, playground):
            continue
        generate_flips_list(x, y, symbol, xs, ys,
                            row, col, flips, playground)
    if len(flips) == 0:
        return None
    return flips


def play(playground: List[List[str]], row: int, col: int,
         symbol: str) -> Optional[int]:
    flips = check_move_and_get_flips(playground, row, col, symbol)
    count_flips = 0
    if flips is None:
        return None
    playground[row][col] = symbol
    for i in range(len(flips)):
        x, y = flips[i][0], flips[i][1]
        playground[x][y] = symbol
        count_flips += 1
    return count_flips


def available_moves(playground: List[List[str]], symbol: str) \
        -> List[List[int]]:
    move_list = []
    size = len(playground)
    for i in range(size):
        for j in range(size):
            if check_move_and_get_flips(playground, i, j, symbol) is not None:
                move_list.append([i, j])
    return move_list


def strategy(playground: List[List[str]], symbol: str) \
        -> Optional[Tuple[int, int]]:
    size = len(available_moves(playground, symbol))
    if size == 0:
        return None
    move = choice(available_moves(playground, symbol))
    return move[0], move[1]


def count_symbol(playground: List[List[str]], symbol: str) -> int:
    counts = 0
    size = len(playground)
    for i in range(size):
        for j in range(size):
            if playground[i][j] == symbol:
                counts += 1
    return counts


def count(playground: List[List[str]]) -> Tuple[int, int]:
    x = count_symbol(playground, "X")
    o = count_symbol(playground, "O")
    return x, o


def fill_board(playground: List[List[str]], symbol: str) -> None:
    size = len(playground)
    for i in range(size):
        for j in range(size):
            if playground[i][j] == " ":
                playground[i][j] = symbol


def final_score(playground: List[List[str]], psymbol: str,
                cpsymbol: str, turn: str) -> None:
    scorep = count_symbol(playground, psymbol)
    scorecp = count_symbol(playground, cpsymbol)
    scorerest = count_symbol(playground, " ")
    if turn == "Comp":
        scorep += scorerest
        final_symbol = psymbol
        print("Finalne skore:", scorep, ":", scorecp)
    else:
        scorecp += scorerest
        final_symbol = cpsymbol
        print("Finalne skore:", scorep, ":", scorecp)
    fill_board(playground, final_symbol)
    draw(playground)
    if scorep > scorecp:
        print("Vyhra!")
    elif scorep < scorecp:
        print("Prehra :(")
    else:
        print("Remiza!")


def print_score(playground: List[List[str]], psymbol: str) -> None:
    scoreo = count(playground)[1]
    scorex = count(playground)[0]
    if psymbol == "O":
        print("Tvoje skore:", scoreo, " Skore oponenta: ", scorex)
    else:
        print("Tvoje skore:", scorex, " Skore oponenta: ", scoreo)


def who_first() -> int:
    while True:
        check = input("Ak chces ist prvy/a, zadaj 1, inak zadaj 2: ")
        if check == "1" or check == "2":
            first = int(check)
            break
        print("Nespravny vstup.")
    return first


def game(size: int) -> None:
    playground = init_playground(new_playground(size))
    print("Vitaj v hre Reversi!")
    draw(playground)
    print("Vyber, kto pojde prvy.")
    first = who_first()

    if first == 1:
        psymbol = "O"
        cpsymbol = "X"
        turn = "Player"
        print("Tvoje kamene su O.")
    else:
        psymbol = "X"
        cpsymbol = "O"
        turn = "Comp"
        print("Tvoje kamene su X.")

    while True:
        if turn == "Player":
            if not available_moves(playground, psymbol):
                print("Nemas ziadne mozne tahy.")
                break
            print("Si na tahu.")
            x = ord(input("Zadaj riadok podla oznacenia: ")) - ord("A")
            y = int(input("Zadaj stlpec podla oznacenia: "))
            if play(playground, x, y, psymbol) is None:
                print("Nespravny vstup. Bol zadany nespravny tah,"
                      " alebo bol zadany tah mimo hracej plochy.")
            else:
                play(playground, x, y, psymbol)
                draw(playground)
                print_score(playground, psymbol)
                if available_moves(playground, cpsymbol) == 0:
                    break
                else:
                    turn = "Comp"

        elif turn == "Comp":
            move = strategy(playground, cpsymbol)
            if move is None:
                print("Oponent uz nema ziadne mozne tahy.")
                break
            else:
                play(playground, move[0], move[1], cpsymbol)
            draw(playground)
            print_score(playground, psymbol)
            turn = "Player"

    final_score(playground, psymbol, cpsymbol, turn)
game(8)