# Takes the current percentage of the battery and how much someone wants to charge
# Prints invalid charge amount if exceeds 100'

GENERATOR_PRICE = 1

def charge(current_charge, target): 

    if not (current_charge <= target <= 100): 
        print("Invalid charge amount")
        return current_charge, 0

    amount = target - current_charge
    return target, amount * GENERATOR_PRICE