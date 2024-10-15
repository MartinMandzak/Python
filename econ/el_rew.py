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
    p_avg = (price[1:] + price[:-1]) / 2  # Average price

    quantity = np.array(quantity)
    q_diff = quantity[1:] - quantity[:-1]
    q_avg = (quantity[1:] + quantity[:-1]) / 2  # Average quantity

    elasticities = abs((q_diff / q_avg) / (p_diff / p_avg))

    return elasticities

def calculate_pension_elasticity(quantity, pension_amount):
    pension_amount = np.array(pension_amount)
    p_diff = pension_amount[1:] - pension_amount[:-1]
    p_avg = (pension_amount[1:] + pension_amount[:-1]) / 2  # Average pension amount

    quantity = np.array(quantity)
    q_diff = quantity[1:] - quantity[:-1]
    q_avg = (quantity[1:] + quantity[:-1]) / 2  # Average quantity

    elasticities = (q_diff / q_avg) / (p_diff / p_avg)
    
    return elasticities

def simulate_price_and_pension_elasticity():
    wages = np.linspace(30000, 150000, 1000)
    spending = [calculate_spending(w) for w in wages]

    # Set up dynamic price changes
    prices = np.linspace(50, 150, 1000)  # Prices ranging from $50 to $150

    # Use a hyperbolic demand curve to maintain unit elasticity
    k = 10000  # This constant can be adjusted to scale the quantity appropriately
    amt_of_clothes = k / prices  # Inversely proportional to price

    # Calculate price elasticities
    price_elasticities = calculate_price_elasticity(prices, amt_of_clothes)

    pensions = np.linspace(8000, 25000, 1000)
    pension_spending = [calculate_spending(p) for p in pensions]

    # Convert pension_spending to a NumPy array for element-wise operations
    pension_spending = np.array(pension_spending)
    
    # Amount of clothes based on pension spending
    amt_of_clothes_pension = k / pension_spending  # This keeps a consistent demand curve shape

    # Calculate pension elasticities
    pension_elasticities = calculate_pension_elasticity(amt_of_clothes_pension, pension_spending)

    return wages, spending, prices, price_elasticities, pension_spending, pension_elasticities, amt_of_clothes, amt_of_clothes_pension

'''
Graphs and results
'''

def plot_simulations(prices, spending, price_elasticities, pension_spending, pension_elasticities, amt_of_clothes, amt_of_clothes_pension):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot amount of clothes vs. prices for price elasticity
    ax1.plot(prices, amt_of_clothes)  # Amount of clothes as a function of price
    ax1.set_xlabel('Price')
    ax1.set_ylabel('Amount of Clothes')
    ax1.set_title('Amount of Clothes vs Price (Price Elasticity)')

    # Plot amount of clothes vs. pension spending for pension elasticity
    ax2.plot(pension_spending[:-1], amt_of_clothes_pension[:-1])  # Amount of clothes as a function of pension spending
    ax2.set_xlabel('Pension Spending Amount')
    ax2.set_ylabel('Amount of Clothes')
    ax2.set_title('Amount of Clothes vs Pension Spending (Pension Elasticity)')

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
wages, spending, prices, price_elasticities, pension_spending, pension_elasticities, amt_of_clothes, amt_of_clothes_pension = simulate_price_and_pension_elasticity()

# Plotting results
plot_simulations(prices, spending, price_elasticities, pension_spending, pension_elasticities, amt_of_clothes, amt_of_clothes_pension)

# Analyzing results
analyze_price_elasticity(price_elasticities)
analyze_pension_elasticity(pension_elasticities)

