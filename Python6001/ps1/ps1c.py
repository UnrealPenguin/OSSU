annual_salary = float(input("Enter your starting salary: "))

r = 0.04
current_savings = 0
semi_annual_raise = 0.07

total_cost = 1000000
portion_down_payment = 0.25
downPayment = total_cost*portion_down_payment

months = 36
monthly_salary = annual_salary/12

low = 0
high = 10000
guess_rate = (low+high)//2
iterations = 0
rate = 0

while abs(current_savings - downPayment) >= 100:

    current_savings = 0
    rate = guess_rate/10000

    for i in range(months+1):
        if i%6==0 and i<0:
            monthly_salary = monthly_salary+(monthly_salary*semi_annual_raise)
        current_savings += monthly_salary*rate+current_savings*r/12
    
    if current_savings < downPayment:
        low = guess_rate
    else: 
        high = guess_rate
    guess_rate = (low+high)//2
    
    iterations +=1
    # log(10,000) base 2 is about 13 iterations
    if iterations > 13:
        break

if iterations > 13 :
    print("It is not possible to pay the down payment in three years.")
else:
    print("Best savings rate: "+ str(rate))
    print("Steps in bisection search: " + str(iterations))
