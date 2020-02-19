from random import random, randint


def dice(prob_six=1 / 6):
    chance = random()
    if chance > prob_six:
        return randint(1, 5)
    return 6


def depot(output, prob_six, round_count):
    if output:
        print("round", round_count, end="")
        print(": 0 -> 1 (", end="")
    firstroll = dice(prob_six)
    while firstroll != 6:
        if output:
            print(firstroll, end=", ")
        firstroll = dice(prob_six)
    if output:
        print(firstroll, end=")")
        print()


def print_rounds(round_count, start_position,
                 final_position, roll_list, roll_count):
    print("round", round_count, end="")
    print(":", start_position, "->", final_position, end="")
    print(" (", end="")
    for i in roll_list:
        roll_count += 1
        if len(roll_list) == roll_count:
            print(i, end=")")
            print()
        else:
            print(i, end=", ")


def check_six(roll, count6):
    if roll == 6:
        count6 += 1
    return count6


def game(size, prob_six=1 / 6, output=True):
    # assertion
    if size < 2:
        if output:
            print("Error: plan too small!")
        return None

    # start
    round_count = 1
    start_position = 1
    final_position = 1
    roll_count = 0
    depot(output, prob_six, round_count)

    # game
    roll_list = []
    while start_position < size:
        count6 = 0
        round_count += 1
        roll = dice(prob_six)
        count6 = check_six(roll, count6)
        add = roll
        roll_list.append(roll)
        # if 6...
        while roll == 6:
            roll = dice(prob_six)
            roll_list.append(roll)
            add += roll
            count6 = check_six(roll, count6)
            if count6 == 3:
                add = 6
                break
        if (final_position + add) <= size:
            final_position = final_position + add

        # round print
        if output:
            print_rounds(round_count, start_position,
                         final_position, roll_list, roll_count)

        # reset
        roll_count = 0
        roll_list = []
        start_position = final_position

    if output:
        print("Game finished in round", round_count, end="")
        print(".")
    return round_count


def average_game(size, games_count, prob_six=1 / 6):
    sum_game = 0
    for _ in range(games_count):
        sum_game += game(size, prob_six, output=False)
    game_average = sum_game / games_count
    return game_average


def find_optimal_probability(size, games_count=1000,
                             partition=20, show_output=False):
    best = 1 / partition
    prob_part = best
    best_length = partition * 1000
    for i in range(partition - 1):
        prob = prob_part * (i + 1)
        length = average_game(size, games_count, prob)
        if show_output:
            print("Probability of six:", "{0:.2f}".format(prob),
                  "Game length:", "{0:.2f}".format(length))
        if best_length > length:
            best_length = length
            best = prob
    return best
