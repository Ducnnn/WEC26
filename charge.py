
# Takes the current percentage of the battery and how much someone wants to charge
# Prints invalid charge amount if 
def charge(current_charge, charge_amount): 
    generator_price = 1; 

    max_charge = 100 - current_charge

    if (charge_amount <= max_charge):
        current_charge += charge_amount
        cost += charge_amount * generator_price
    else: 
        print("Invalid Charge Amount")
        