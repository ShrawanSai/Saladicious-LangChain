import joblib
from sklearn.multioutput import MultiOutputRegressor
import pandas as pd

model = joblib.load('backend/regression_model.pkl')

def predict_usage(number_of_serving_communities, sample_given, date):
    # Feature engineering for the input date
    date = pd.to_datetime(date)
    year = date.year
    month = date.month
    day = date.day
    day_of_week = date.dayofweek

    # Prepare the input features
    input_features = pd.DataFrame({
        'Number_of_Serving_Communities': [number_of_serving_communities],
        'Sample_Given': [sample_given],
        'Year': [year],
        'Month': [month],
        'Day': [day],
        'DayOfWeek': [day_of_week]
    })

    # Predict the usage
    prediction = model.predict(input_features)

    # Return the predicted values as a dictionary
    return {
        'Lettuce_Usage': round(prediction[0][0]),
        'Chicken_Usage': round(prediction[0][1]),
        'Tomato_Usage': round(prediction[0][2]),
        'Cheese_Usage': round(prediction[0][3]),
        'Onion_Usage': round(prediction[0][4])
    }

if __name__ == '__main__':
    # Test the function
    predicted_usage = predict_usage(number_of_serving_communities=15, sample_given=1, date='2023-02-28')
    print(predicted_usage)
