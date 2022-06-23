annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to be saved, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: ")) 


portion_down_payment = 0.25
downPayment = total_cost*portion_down_payment

r = 0.04
monthly_salary = annual_salary/12

current_savings = 0
months = 0

while current_savings < downPayment:
    investment = current_savings*r/12
    moneyDP = monthly_salary*portion_saved

    current_savings+=investment+moneyDP
    months += 1

print("Number of months till enough for down payment: "+ str(months))