class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    def __str__(self):
        output = ''
        output += self.name.center(30, '*') + '\n'

        total = self.get_balance()
        for item in self.ledger:
            output += item['description'].ljust(23)[:23]
            output += "{:>7.2f}".format(item['amount'])
            output += "\n"

        output += "Total: " + "{0:.2f}".format(total)

        return output
             
    def deposit(self, amount, description=''):
        # Always Positive Value
        self.ledger.append({"amount": abs(amount), "description": description})
    
    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            # Always Negative Value
            self.ledger.append({"amount": -abs(amount), "description": description})
            return True
        else:
            return False
        
    def transfer(self, amount, other_category):
        transfer_to = 'Transfer to ' + other_category.name
        transfer_from = 'Transfer from ' + self.name

        if self.check_funds(amount):
            self.withdraw(amount, transfer_to)
            other_category.deposit(amount, transfer_from)
            return True
        else:
            return False

         
    def get_balance(self):
        current_balance = 0
        for item in self.ledger:
            current_balance += item['amount']
        return current_balance

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True

def create_spend_chart(categories):
    output = "Percentage spent by category\n"

    total_budget = 0
    expenses = []
    category_names = []
    len_names = 0

    for category in categories:
        expense = sum([-item['amount'] for item in category.ledger if item['amount'] < 0])
        total_budget += expense

        if len(category.name) > len_names:
            len_names = len(category.name)

        expenses.append(expense)
        category_names.append(category.name)
    
    expenses = [(expense / total_budget) * 100 for expense in expenses]
    category_names = [name.ljust(len_names, " ") for name in category_names]

    for step in range(100,-1,-10):
        output += str(step).rjust(3, ' ') + '|'
        for expense in expenses:
            output += ' o ' if expense >= step else '   '
        output += ' \n'

    output += '    ' + '---' * len(category_names) + '-\n'

    for space in range(len_names):
        output += "    "
        for name in category_names:
            output += " " + name[space] + " "
        output += " \n"

    return output.strip("\n")
