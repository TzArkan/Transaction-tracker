from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income",
              "E": "Expense"}


def get_date(prompt, allow_default=False):                       # prompt primit - pentru ceea ce vrem sa ii cerem userului, pt diferite motive
    # allow_default - daca cineva nu introduce valoare, se ia data curenta
    date_str = input(prompt)                                    # folosim promptu
    if allow_default and not date_str:                          # daca doar se da enter fara introducere valoare
            return datetime.today().strftime(date_format)         # obiect datetime convertit string format time pt primirea datelor
    try:
            valid_date = datetime.strptime(date_str, date_format) # luam stringul de date,folosim formatul si il convertim in datetime object
            return valid_date.strftime(date_format)               # odata obtinut obiectul, il convertim in format str de care avem nevoie
    except ValueError:                                          # daca data introdusa nu respecta formatul de data
            print("Invalid date format. Enter the date in dd-mm-yyyy")
            return get_date(prompt, allow_default)

def get_amount():
    try:
            amount = float(input("Enter amount: "))             # incercam sa convertim la nr intreg inputul userului
            if amount <= 0:                                     # o valoare > 0
               raise ValueError("amount must a non-negative, non-zero value.")
            return amount
    except ValueError as e:
           print(e)
           return get_amount()


def get_category():
    category = input("Enter category ('I' for Income | 'E' for Expense): ").upper()   # introduce categoria
    if category in CATEGORIES:                                  # daca categoria introdusa e in categoriile definite
          return CATEGORIES[category]                           # returnam categoria aceea
    
    print("Invalid category. Please enter 'I' for Income and 'E' for Expense")
    return get_category()


def get_description():
    return input("Enter a description (optional):\n")




