import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# Function to load the dataset
def load_data():
    data = st.file_uploader("Upload Metro Interstate Traffic Volume CSV", type=["csv"])
    if data is not None:
        df = pd.read_csv(data)
        return df
    else:
        st.warning("Please upload the dataset.")
        return None


# Main function to run the Streamlit app
def main():
    st.title("Crowd Management of Routes")

    # Load and display the dataset
    df = load_data()
    if df is not None:
        st.subheader("Dataset Overview")
        st.write(df.head())

        # Data preprocessing
        df['date_time'] = pd.to_datetime(df['date_time'])
        df['hour'] = df['date_time'].dt.hour
        df['day'] = df['date_time'].dt.day
        df['month'] = df['date_time'].dt.month
        df['day_of_week'] = df['date_time'].dt.dayofweek

        X = df[['hour', 'day', 'month', 'day_of_week']]
        y = df['traffic_volume']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Scaling
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Model training
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predictions
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        st.subheader("Prediction Results")
        st.write(f"Mean Absolute Error: {mae:.2f}")

        # Classify crowd status
        threshold = 100
        crowd_status = ["Crowded" if pred >= threshold else "Not Crowded" for pred in y_pred]
        st.write(f"Crowd Classification based on threshold {threshold}:")

        result_df = pd.DataFrame({
            "Predicted Traffic Volume": y_pred,
            "Crowd Status": crowd_status
        })
        st.write(result_df)

        # Visualizing traffic volume distribution
        st.subheader("Traffic Volume Distribution")
        plt.figure(figsize=(10, 5))
        sns.histplot(df['traffic_volume'], kde=True)
        plt.title('Traffic Volume Distribution')
        st.pyplot(plt)


if __name__ == "__main__":
    main()
