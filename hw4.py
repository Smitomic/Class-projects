from datetime import datetime, date
from typing import Dict, Tuple, Set, List


# ========================================
# Task 1: Bank (4 points)
# ========================================

def load_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as my_file:
        return my_file.readlines()


def error_print(task, count):
    print(f'Instruction "{task[0]}" called with an invalid '
          f'argument on line {count}.')


def create(task, count, accounts):
    if (task[1] in accounts) or int(task[2]) < 0:
        error_print(task, count)
        return False
    accounts[task[1]] = int(task[2])
    return True


def add(task, count, accounts):
    if (task[1] not in accounts) or int(task[2]) < 0:
        error_print(task, count)
        return False
    accounts[task[1]] += int(task[2])
    return True


def sub(task, count, accounts):
    if (task[1] not in accounts) or int(task[2]) < 0:
        error_print(task, count)
        return False
    accounts[task[1]] -= int(task[2])
    return True


def filter_out(task, count, accounts):
    if (int(task[1]) < 0) or ((task[2] != "MIN") and (task[2] != "MAX")):
        error_print(task, count)
        return False
    sorted_acc = sorted(accounts.items(), key=lambda accs: accs[0])
    if task[2] == "MAX":
        sorted_acc = sorted(sorted_acc, key=lambda accs: accs[1], reverse=True)
    else:
        sorted_acc = sorted(sorted_acc, key=lambda accs: accs[1])

    if int(task[1]) > len(sorted_acc):
        d_index = len(sorted_acc)
    else:
        d_index = int(task[1])

    for i in range(d_index):
        del accounts[sorted_acc[i][0]]
    return True


def aggregate(task, count, accounts):
    if (task[1] not in accounts) or (task[2] not in accounts):
        error_print(task, count)
        return False
    accounts[task[1]] += accounts[task[2]]
    del accounts[task[2]]
    return True


def crowdsource(task, count, accounts):
    if (task[1] not in accounts) or int(task[2]) < 0:
        error_print(task, count)
        return False
    sorted_acc = sorted(accounts.items(), key=lambda accs: accs[0])
    sorted_acc = sorted(sorted_acc, key=lambda accs: accs[1], reverse=True)
    sorted_acc = list(filter(lambda acc: acc[0] != task[1], sorted_acc))
    accumulated = 0
    for acc in sorted_acc:
        if acc[1] < 100:
            accounts[acc[0]] = 0
            accounts[task[1]] += acc[1]
            accumulated += acc[1]
        else:
            accounts[acc[0]] -= 100
            accounts[task[1]] += 100
            accumulated += 100
        if accumulated >= int(task[2]):
            break
    return True


def print_acc(accounts):
    sorted_acc = sorted(accounts.items(), key=lambda accs: accs[0])
    sorted_acc = sorted(sorted_acc, key=lambda accs: accs[1], reverse=True)
    for acc in sorted_acc:
        print(f"{acc[0]}: {acc[1]}")


def action(task, count, accounts):
    a = True
    if task[0] == "CREATE":
        a = create(task, count, accounts)
    elif task[0] == "ADD":
        a = add(task, count, accounts)
    elif task[0] == "SUB":
        a = sub(task, count, accounts)
    elif task[0] == "FILTER_OUT":
        a = filter_out(task, count, accounts)
    elif task[0] == "AGGREGATE":
        a = aggregate(task, count, accounts)
    elif task[0] == "CROWDSOURCE":
        a = crowdsource(task, count, accounts)
    elif task[0] == "PRINT":
        print_acc(accounts)
    return a


def interpret_file(file_name: str, accounts: Dict[str, int]) -> None:
    file = load_file(file_name)
    tasks = []
    for row in file:
        tasks.append(row.split())

    count = 0
    instructions = ["CREATE", "ADD", "SUB", "FILTER_OUT",
                    "AGGREGATE", "CROWDSOURCE", "PRINT"]
    for task in tasks:
        count += 1
        if not task:
            continue
        if task[0] not in instructions:
            print(f'Invalid instruction "{task[0]}" on line {count}.')
            return
        elif ((task[0] != "PRINT") and (len(task) > 3)) or \
                (task[0] == "PRINT" and (len(task) > 1)):
            print(f"Invalid number of arguments on line {count}.")
            return
        if not action(task, count, accounts):
            return


# ========================================
# Task 2: Chat (4 points)
# ========================================

Message = Tuple[datetime, str, str]


def to_datetime(value: str) -> datetime:
    return datetime.utcfromtimestamp(int(value))


def parse_message(line: str) -> Message:
    message = line.split(",")
    date_time = to_datetime(message[0])
    return date_time, message[1], message[2]


def latest_messages(chat: List[Message], count: int) -> List[Message]:
    sorted_messages = sorted(chat, key=lambda tup: tup[0], reverse=True)
    latest = sorted_messages[:count]
    return latest


def messages_at(chat: List[Message], day: date) -> List[Message]:
    messages = []
    for message in chat:
        if message[0].date() == day:
            messages.append(message)
    return messages


def senders(chat: List[Message]) -> Set[str]:
    senders_set = set()
    for message in chat:
        senders_set.add(message[1])
    return senders_set


def message_counts(chat: List[Message]) -> Dict[str, int]:
    dict_messages = {}
    for message in chat:
        if message[1] not in dict_messages:
            dict_messages[message[1]] = 1
        else:
            dict_messages[message[1]] += 1
    return dict_messages


def mentions(chat: List[Message], user: str) -> List[str]:
    pass


# ========================================
# Task 3: Longest Word (2 points)
# ========================================
def get_word_list(text: str) -> List[str]:
    new_text = ""
    for char in text:
        if char.isalnum() or char == " ":
            new_text = new_text + char
        else:
            char = " "
            new_text = new_text + char
    return new_text.split()


def longest_word(text: str, provided_letters: Set[str],
                 case_insensitive: bool = False) -> str:
    word_list = get_word_list(text)
    max_word = ""
    for word in word_list:
        correct = True
        for char in word:
            if case_insensitive:
                if char.upper() not in provided_letters:
                    if char.lower() not in provided_letters:
                        correct = False
                        break
            elif char not in provided_letters:
                correct = False
                break
        if correct and (len(word) >= len(max_word)):
            max_word = word
    return max_word


# ========================================
# Task 4: Parentheses Check (2 points)
# ========================================
def print_error_1(stack, text, i):
    if len(stack) == 0:
        print(f"'{text[i]}' at position {i} "
              f"does not have an opening paired bracket")
    else:
        print(f"'{text[stack[len(stack) - 1]]}' at position "
              f"{stack[len(stack) - 1]} does not match "
              f"'{text[i]}' at position {i}")


def print_error_2(text, stack):
    print(f"'{text[stack[0]]}' at position {stack[0]}"
          f" does not have a closing paired bracket")


def parentheses_check(text: str, output: bool = False) -> bool:
    left_p = ["(", "[", "{"]
    right_p = [")", "]", "}"]
    stack = []
    for i in range(len(text)):
        if text[i] in left_p:
            stack.append(i)
        elif text[i] in right_p:
            pos = right_p.index(text[i])
            if (len(stack) > 0) and \
                    (left_p[pos]) == text[stack[len(stack) - 1]]:
                stack.pop()
            else:
                if output:
                    print_error_1(stack, text, i)
                return False
    if len(stack) == 0:
        return True
    if output:
        print_error_2(text, stack)
    return False
