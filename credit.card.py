import os
import random
import string
from datetime import datetime, timedelta

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_credit_cards_from_file(num_cards=None):
    credit_cards = []
    with open("database.txt", "r") as file:
        for line in file:
            card_info = line.strip().split("|")
            if num_cards is None or len(credit_cards) < num_cards:
                credit_cards.append({
                    "number": card_info[0],
                    "month": card_info[1],
                    "year": card_info[2],
                    "cvc": card_info[3]
                })
            else:
                break
    return credit_cards

def generate_credit_card():
    def luhn_checksum(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10

    def is_luhn_valid(card_number):
        return luhn_checksum(card_number) == 0

    def generate_valid_number():
        card_number = ''.join(random.choice(string.digits) for _ in range(15))
        card_number = '6709' + card_number
        return card_number if is_luhn_valid(card_number) else generate_valid_number()

    current_year = datetime.now().year
    exp_year = current_year + random.randint(3, 10)
    exp_month = random.randint(1, 12)
    cvc = ''.join(random.choice(string.digits) for _ in range(3))

    return {
        "number": generate_valid_number(),
        "month": f"{exp_month:02d}",
        "year": str(exp_year),
        "cvc": cvc
    }

def print_credit_card(card):
    print("------------------------------------------------")
    print(f"CVC: {card['cvc']}")
    print(f"NUMBER: {card['number']}")
    print(f"EXPIRE: {card['month']}/{str(card['year'])[-2:]}")
    print(f"NAME: Shared Card")
    print("------------------------------------------------")

def print_gui():
    clear_terminal()
    print("--------------- Nice Credit Card ---------------")
    print("1 - Get all credit cards in database")
    print("2 - Get a specific number of credit cards")
    print("3 - Generate a specific number of credit cards")
    print("4 - Exit")
    print("------------------------------------------------")

    choice = input("python@linux:~$ ")
    if choice == "1":
        credit_cards = get_credit_cards_from_file()
        for card in credit_cards:
            print_credit_card(card)
    elif choice == "2":
        num_cards = int(input("Enter the number of credit cards to get\npython@linux:~$ "))
        credit_cards = get_credit_cards_from_file(num_cards)
        for card in credit_cards:
            print_credit_card(card)
    elif choice == "3":
        num_cards = int(input("Enter the number of credit cards to generate\npython@linux:~$ "))
        new_cards = []
        for _ in range(num_cards):
            new_card = generate_credit_card()
            new_cards.append(new_card)
            with open("database.txt", "a") as file:
                file.write(f"{new_card['number']}|{new_card['month']}|{new_card['year']}|{new_card['cvc']}\n")
        for card in new_cards:
            print_credit_card(card)
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")

while True:
    print_gui()
    input("python@linux:~$ ")
