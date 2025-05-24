import pandas as pd
import csv
from datetime import datetime
from data_entry import get_category, get_date, get_description, get_amount
import matplotlib.pyplot  as plt


class CSV:                                          # clasa CSV
    CSV_FILE = "finance_data.csv"                   # fisier pentru CSV
    COLUMNS = ["date","amount","category","description"] # coloanele din csv
    FORMAT = "%d-%m-%Y"

    @classmethod                                    # decorator de clasa - va avea acces la clasa (metode sau variabile) in sine, dar nu la o instanta a acesteia. 
    def initialize_csv(cls):                        # citim sau cream (daca nu exista) fisierul
        try:                                        # incercam     
            pd.read_csv(cls.CSV_FILE)               # sa citim fisierul csv
        except FileNotFoundError:                   # daca nu exista
            df = pd.DataFrame(columns = cls.COLUMNS)    # cream fisierul, specificand coloanele pe care vrem sa le aiba csvul 
            # data frame => obiect din pandas care permite accesul la diferite randuri si coloane dintr-un fisier csv

            df.to_csv(cls.CSV_FILE, index = False)  # exportam data frameul intr-un csv. Nu vom sorta prin indexare
    

    @classmethod
    def add_entry(cls, date, amount, category, description):        # adaugam date in cls
        new_entry = {                               # nou dictionar de date pt a scrie direct in coloanele dorite
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:    # a - append la sfarsit de fisier | newline - se suprascrie cu "", pt a nu adauga o linie noua la deschidere fisier
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)    #  .dictwriter - luam un dictionar si il scriem in csv
            writer.writerow(new_entry)              # introducem noul dictionar
        print("content adaugat")    


    @classmethod
    def get_transaction(cls, start_date, end_date): # definim o tranzactie cu clasa, datele de start si sfarsit ale tranzactiei
        df = pd.read_csv(cls.CSV_FILE)              # citim in fisierul csv
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)    # convertim datele din coloana de date la un obiect date pentru a le putea filtra dupa tranzactii diferite
        start_date = datetime.strptime(start_date, CSV.FORMAT)  # trecem stringul in formatul corespunzator
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)    # daca data de pe randul curent este mai mare decat data start si mai mica decat end
        # MASK - ceva ce putem aplica diferitelor randuri dintr-un df pt a vedea daca trebuie sa le selectam sau nu
        # '&' sau 'and' - folosit specific in lucru cu masti sau df pandas
        
        filtered_df = df.loc[mask]                  # returneaza un df filtrat care contine doar randurile unde ce e la masca e true

        if filtered_df.empty:
            print("no transactions found in the given data range")
        else:
            print(f"transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                    )                               # functie lambda anonima care va lua obiecte datetime, le va formata la strftime cu formatul specificat
                )
            # formatters - formatam coloane specifice. numele de coloana ca si cheie, si functia pe care vrem sa o aplicam fiecarui element din acea coloana

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            # ia toate randurile din df unde category este egal cu income. din acele randuri, ne uitam specific la valorile din coloana amount, pe care le insumam 

            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net savings ${(total_income - total_expense):.2f}")

        return filtered_df



def add():                                          # functie care va apela functiile get din data_entry in ordinea in care vrem sa colectam datele
    CSV.initialize_csv()
    date = get_date("Enter date for the transaction (dd-mm-yyyy) or enter today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


# CSV.initialize_csv()                                # initializam csvul
# CSV.add_entry("20-07-2024", "125.65", "Income", "Salary") # am adaugat date in coloanele csv

CSV.get_transaction("01-01-2023","30-07-2025")


def plot_transactions(df):                          # se primesc tranzactiile pe care le vrem plotate
    df.set_index('date', inplace=True)              # prin index localizam si sortam diferite randuri pt creare plot

    # cream 2 dataframeuri, unu pentru income si unu pentru expense
    # randurile care sunt income
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")                              # 'D' daily frequency - ia datele filtrate cu tranzactiile, si vom avea un rand pentru toate zilele ramase
        .sum()                                      # sum() - insumeaza toate valorile - agrega randurile care au aceeasi data la un unic amount
        .reindex(df.index, fill_value=0)            # reindex - umplem orice valoare care lipseste cu 0
        )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")                              # 'D' daily frequency - ia datele filtrate cu tranzactiile, si vom avea un rand pentru toate zilele ramase
        .sum()                                      # sum() - insumeaza toate valorile - agrega randurile care au aceeasi data la un unic amount
        .reindex(df.index, fill_value=0)            # reindex - umplem orice valoare care lipseste cu 0
        )    
    
    plt.figure(figsize=(10,5))                      # canvas pentru grafic, cu size de 10 si 5
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")  # folosim asa x pentru index si y pentru valorile amount
    plt.plot(expense_df.index, expense_df["amount"], label="Expnese", color="r") 
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and expenses over time")
    plt.legend()                                    # legenda pt labels si culori
    plt.grid(True)                                  # linii grid
    plt.show()                                      # ia tot plotul creat si il afiseaza pe ecran



def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a data range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy)")
            end_date =  get_date("Enter the end date (dd-mm-yyyy)")
            df = CSV.get_transaction(start_date, end_date)
            if input("Do you want to see a plot? (y/n)").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

if __name__ == "__main__":                                  # daca rulam din acest fisier, atunci se va rula linia asta
    main()                                                  # daca se importa fisierul, linia nu va rula pentru ca __name__ nu va fi main
