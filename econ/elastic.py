import numpy as np
import matplotlib.pyplot as plt

'''
Formulas and simulations
'''

def calculate_spending(wage):
    return wage / 3

def calculate_price_elasticity(price, quantity):
    price = np.array(price)
    p_diff = price[1:] - price[:-1]
    p_avg = np.average(price)

    quantity = np.array(quantity)
    q_diff = quantity[1:] - quantity[:-1]
    q_avg = np.average(quantity)

    elasticities = abs((q_diff/q_avg)/(p_diff/p_avg))

    return elasticities

def calculate_pension_elasticity(quantity, pension_amount):
    pension_amount = np.array(pension_amount)
    p_diff = pension_amount[1:] - pension_amount[:-1]
    p_avg = np.average(pension_amount)

    quantity = np.array(quantity)
    q_diff = quantity[1:] - quantity[:-1]
    q_avg = np.average(quantity)

    elasticities = (q_diff/q_avg)/(p_diff/p_avg)

    return elasticities

def simulate_price_and_pension_elasticity():
    # linspace(i_start, i_end, amt_of_samples)
    wages = np.linspace(30000, 150000, 1000)
    # only spending a third
    spending = [calculate_spending(w) for w in wages]
    
    # spending == value for amount of clothes received (in $)
    amt_of_clothes = np.linspace(15000, 3000,1000)
    price_elasticities = calculate_price_elasticity(amt_of_clothes, spending)
    
    pensions = np.linspace(8000, 25000, 1000)
    # only spends one third of it
    pension_spending = [calculate_spending(p) for p in pensions]
    
    pension_elasticities = calculate_pension_elasticity(amt_of_clothes, pension_spending)
    
    return wages, spending, price_elasticities, pension_spending, pension_elasticities

'''
Graphs and results
'''

def plot_simulations(amt_of_clothes, spending, price_elasticities, pension_spending, pension_elasticities):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(spending, amt_of_clothes)
    ax1.set_xlabel('Spending')
    ax1.set_ylabel('Amt. of clothes')
    ax1.set_title('Price Elasticity Simulation')

    ax2.plot(pension_spending, amt_of_clothes)
    ax2.set_xlabel('Pension Spending Amount')
    ax2.set_ylabel('Amt. of clothes')
    ax2.set_title('Pension Elasticity Simulation')

    plt.tight_layout()
    plt.show()

def analyze_price_elasticity(price_elasticities):
    mean_price_elasticity = np.mean(price_elasticities)
    std_price_elasticity = np.std(price_elasticities)
    
    print(f"\nPrice Elasticity Analysis:")
    print(f"Mean elasticity: {mean_price_elasticity:.2f}")
    print(f"Standard deviation: {std_price_elasticity:.2f}")

def analyze_pension_elasticity(pension_elasticities):
    mean_pension_elasticity = np.mean(pension_elasticities)
    std_pension_elasticity = np.std(pension_elasticities)
    
    print("\n\nPension Elasticity Analysis:")
    print(f"Mean elasticity: {mean_pension_elasticity:.2f}")
    print(f"Standard deviation: {std_pension_elasticity:.2f}")

# Run the simulations and analysis
simulate_price_and_pension_elasticity()
plot_simulations(*simulate_price_and_pension_elasticity())
analyze_price_elasticity(simulate_price_and_pension_elasticity()[2])
analyze_pension_elasticity(simulate_price_and_pension_elasticity()[4])

