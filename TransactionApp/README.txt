	data_entry.py — Input Handling
get_date(prompt, allow_default): Validates user date input (dd-mm-yyyy); uses today’s date if allowed and left blank.

get_amount(): Asks for a positive float value.

get_category(): Accepts 'I' or 'E', returns "Income" or "Expense".

get_description(): Optional text input for transaction description.


	main.py - Core Functionality
CSV Class
Handles all CSV-related tasks:

initialize_csv(): Creates finance_data.csv with headers if missing.

add_entry(...): Appends a new transaction row (date, amount, category, description).

get_transaction(start, end):

Reads and filters transactions within the date range.

Displays transactions and calculates:

Total income

Total expense

Net savings

plot_transactions(df)
Takes filtered transactions.

Plots Income vs. Expense over time (daily), using matplotlib.

main() Loop
A CLI menu with 3 options:

Add new transaction

View transactions (within date range + optional plot)

Exit