# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 12:47:22 2020

@author: GoldS
"""

PORTION_DOWN_PAYMENT = 0.25
INVESTMENT_GAINS_RATE = 0.04
current_savings = 0

annual_salary = float(input("Enter your annual salary: ")) # 120000
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: ")) # .10
total_cost =  float(input("Enter the cost of your dream home: ")) # 1000000
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: ")) # .03

months = 0;
while current_savings < total_cost * PORTION_DOWN_PAYMENT:
    if months > 0 and months % 6 == 0:
        annual_salary *= 1 + semi_annual_raise

    current_savings *= 1 + (INVESTMENT_GAINS_RATE/12)
    current_savings += (annual_salary * portion_saved) / 12
    months += 1 
    
print(months)
