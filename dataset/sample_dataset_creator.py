import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample data
dates = pd.date_range(start="2023-01-01", periods=30, freq='D')
number_of_serving_communities = [1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,5,5,5,6,6,6,7]
sample_given = [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1]
lettuce_usage = [10,10,15,15,20,20,25,25,30,30,35,35,40,40,45,45,50,50,55,55,60,60,65,65,70,70,75,75,80,80]
chicken_usage = [20,20,25,25,30,30,35,35,40,40,45,45,50,50,55,55,60,60,65,65,70,70,75,75,80,80,85,85,90,90]
tomato_usage = [3,3,6,6,9,9,12,12,15,15,18,18,21,21,24,24,27,27,30,30,33,33,36,36,39,39,42,42,45,45]
cheese_usage = [0.5,0.5,1,1,1.5,1.5,2,2,2.5,2.5,3,3,3.5,3.5,4,4,4.5,4.5,5,5,5.5,5.5,6,6,6.5,6.5,7,7,7.5,7.5]
onion_usage = [5,5,10,10,15,15,20,20,25,25,30,30,35,35,40,40,45,45,50,50,55,55,60,60,65,65,70,70,75,75]

# Create a DataFrame
data = {
    "Date": dates,
    "Number_of_Serving_Communities": number_of_serving_communities,
    "Sample_Given": sample_given,
    "Lettuce_Usage": lettuce_usage,
    "Chicken_Usage": chicken_usage,
    "Tomato_Usage": tomato_usage,
    "Cheese_Usage": cheese_usage,
    "Carrot_Usage": onion_usage
}

df_stock_forecast = pd.DataFrame(data)

# Save the DataFrame to a CSV file
file_path_stock_forecast = "ingredient_stock_forecast_sample.csv"
df_stock_forecast.to_csv(file_path_stock_forecast, index=False)

print(f"Sample dataset saved to {file_path_stock_forecast}")
