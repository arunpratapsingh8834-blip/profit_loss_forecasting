import pandas as pd
import numpy as np 

# Set random seed for reproducibility

np.random.seed(42)
# Generate a date range for two years (2023-2024)
dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
# Initialize an empty list to store the generated data
data = []
# base revenue amount for satrting similution
base_revenue = 10000
#loop over each date to generate daily data 
for date in dates:
    # calculating the trend
    days_passed = (date - dates[0]).days
    trend_growth = days_passed * 5
    # add a seasonal boost during november and december
    if date.month in [11, 12]:
        seasonal_boost = 3000 #extra boost in holiday season
    else:
        seasonal_boost = 0 #no boost in other months
        # add some random noise to make the data more realistic
    noise = np.random.normal(0, 1000) #random noise with mean 0 
   # calculate revenue as base +  trend + seasonal boost + noise
    revenue = base_revenue + trend_growth + seasonal_boost + noise
    revenue = max(revenue, 2000) # ensure revenue never goes below 2000
    # calculate cost of goods sold as a percentage of revenue 
    cogs = revenue * np.random.uniform(0.4, 0.6) #cogs between 40% and 60% of revenue
    #operating expenses : random between 2000 and 5000
    operating_expenses = np.random.uniform(2000, 5000)
    # marketing expenses : random between 500 and 1500
    marketing_spend = np.random.uniform(500, 1500)
    # append each day's data as row to the list
    data.append({
         "date": date ,
         "revenue": round(revenue, 2),# revenue for the day rounded to 2 decimal places
         "cost": round(cogs, 2), #cogs for the day rounded to 2 decimal places
         "operating_expenses": round(operating_expenses, 2), #operating expenses rounded to 2 decimal places
         "marketing_expenses": round(marketing_spend, 2) #marketing expenses rounded to 2 decimal places   
        
    })
# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data, columns=[
    "date",
    "revenue", 
    "cost",
    "operating_expenses",  
    "marketing_expenses"
])
# Save the DataFrame to a CSV file
df.to_csv("company_financial_data_main2.csv", index=False)

print("Dataset generated successfully!check company_financial_data_main.csv.")  

