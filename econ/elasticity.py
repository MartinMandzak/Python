import numpy as np
import matplotlib.pyplot as plt

def price_elasticity_simulation():
    prices = np.linspace(50, 150, 100)
    quantities = np.random.uniform(500, 2000, 100)
    
    elasticities = (prices / quantities).reshape(-1, 1)
    
    return prices, quantities, elasticities

def pension_elasticity_simulation():
    ages = np.linspace(25, 75, 100)
    pensions = np.random.uniform(800, 2500, 100)
    
    elasticities = (ages / pensions).reshape(-1, 1)
    
    return ages, pensions, elasticities

def plot_elasticity_simulations():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    prices, quantities, elasticities = price_elasticity_simulation()
    
    ax1.scatter(prices, quantities)
    ax1.set_xlabel('Price')
    ax1.set_ylabel('Quantity')
    ax1.set_title('Price Elasticity Simulation')

    ages, pensions, elasticities = pension_elasticity_simulation()
    
    ax2.scatter(ages, pensions)
    ax2.set_xlabel('Age')
    ax2.set_ylabel('Pension Amount')
    ax2.set_title('Pension Elasticity Simulation')

    plt.tight_layout()
    plt.show()

def analyze_elasticity_simulations():
    prices, quantities, elasticities = price_elasticity_simulation()
    ages, pensions, elasticities = pension_elasticity_simulation()

    print("Price Elasticity Simulation:")
    print(f"Mean elasticity: {np.mean(elasticities):.2f}")
    print(f"Standard deviation: {np.std(elasticities):.2f}")

    print("\n\nPension Elasticity Simulation:")
    print(f"Mean elasticity: {np.mean(elasticities):.2f}")
    print(f"Standard deviation: {np.std(elasticities):.2f}")

# Run the simulations and analysis
plot_elasticity_simulations()
analyze_elasticity_simulations()

