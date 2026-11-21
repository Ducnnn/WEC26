from charge import charge 

# Attempts to progressively decrease the amount of charge needed
def battery(hour, current): 
    current = 0
    if 1 <= hour <= 18: 
        current, cost = charge(current, 100)
    elif(18 < hour <= 22): 
        current, cost = charge(current, 50)
    else:
        cost = 0
    return current, cost