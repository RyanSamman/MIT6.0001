# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 15:46:13 2020

@author: RyanS
"""

def calculateSavings(annual_salary, portion_saved, investment_gains_rate, semi_annual_raise, months_to_goal):
        current_savings = 0
        
        for m in range(0, months_to_goal):
            if m > 0 and m % 6 == 0:
                annual_salary *= 1 + semi_annual_raise
        
            current_savings *= 1 + (investment_gains_rate/12)
            current_savings += (annual_salary * portion_saved) / 12
            
        return current_savings

# Define constants
MONTHS_TO_GOAL = 36
SEMI_ANNUAL_RAISE = 0.07
INVESTMENTS_RETURN = 0.04

PERCENTAGE_DOWN_PAYMENT = 0.25
HOUSE_COST = 1000000
TARGET_SAVINGS = PERCENTAGE_DOWN_PAYMENT * HOUSE_COST

# Get user input
annual_salary = int(input("Enter the starting salary: "))

# Search for a decimal between 0 and 100000 => Divide by 10^5 => 1.0000
DIVISION_RATE = 10000
ERROR_MARGIN = 100

# Currying
savings = lambda portion_saved: calculateSavings(annual_salary, portion_saved, INVESTMENTS_RETURN, SEMI_ANNUAL_RAISE, MONTHS_TO_GOAL)

def binarySearch(target, l, h, steps=0):
    m = l + (h - l) // 2 # Prevent overflows in other languages
    
    savingsRate = m / DIVISION_RATE
    savingsAfterTargetMonths = savings(savingsRate)
    
    if target - ERROR_MARGIN < savingsAfterTargetMonths < target + ERROR_MARGIN:
        return savingsRate, steps
    elif l == h:
        return None, None
    elif target > savingsAfterTargetMonths:
        return binarySearch(target, m + 1, h, steps + 1)
    elif target < savingsAfterTargetMonths:
        return binarySearch(target, l, m, steps + 1)
    
rate, steps = binarySearch(TARGET_SAVINGS, 0, DIVISION_RATE) # Division rate is also the max

# More General Case Binary Search, pass in a function to modify it's behavior
# def binarySearch(target, l, h, func, steps=0):
#     m = l + (h - l) // 2 # Prevent overflows in other languages
    
#     value = func(m)

#     if target == value:
#         return value, steps
#     elif l == h:
#         return None, None
#     elif target > value:
#         return binarySearch(target, m + 1, h, steps + 1)
#     elif target < value:
#         return binarySearch(target, l, m, steps + 1)
    
rate, steps = binarySearch(TARGET_SAVINGS, 0, DIVISION_RATE) # Division rate is also the max



if rate is None:
    print("It is not possible to pay down payment in three years")
else:
    print(f"Best savings rate: {rate}")
    print(f"Steps in bisection search: {steps}")