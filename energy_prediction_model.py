"""
Energy Consumption Prediction Model

This module provides a simple Linear Regression model to predict future energy
consumption based on time-based features. It's designed to be easy to understand
and beginner-friendly.

How it works:
1. Extract time features from historical data (hour, day of week, month, etc.)
2. Train a Linear Regression model using these features
3. Use the trained model to predict future energy consumption
4. The model learns patterns like "Friday afternoons use more energy"

Key Concepts:
- Features: Input variables (hour, day, month, etc.)
- Target: What we're predicting (energy consumption in kWh)
- Training: Teaching the model by showing it historical patterns
- Prediction: Using the trained model to estimate future values
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from datetime import datetime, timedelta
import json


class EnergyConsumptionPredictor:
    """
    Simple Linear Regression model to predict energy consumption.
    
    This model learns from historical energy data and predicts future
    consumption based on time patterns.
    
    Attributes:
        model (LinearRegression): The trained scikit-learn model
        feature_names (list): Names of features used (for reference)
        is_trained (bool): Whether the model has been trained
    """
    
    def __init__(self):
        """Initialize the predictor with an untrained model."""
        # ================================================================
        # Step 1: Initialize the Linear Regression model
        # ================================================================
        # LinearRegression is a simple, easy-to-understand algorithm that:
        # - Finds the best straight line through the data
        # - Uses the line to make predictions
        # - Works well for time-based patterns
        self.model = LinearRegression()
        
        # Track if model is trained
        self.is_trained = False
        
        # Store feature names for reference
        self.feature_names = [
            'hour',           # 0-23: Hour of day
            'day_of_week',    # 0-6: Monday-Sunday
            'day_of_month',   # 1-31: Day within month
            'month',          # 1-12: Month number
            'is_weekend',     # 0/1: Is it weekend?
            'is_business_hour' # 0/1: Is it 9am-5pm?
        ]
    
    def extract_time_features(self, timestamp):
        """
        Extract time-based features from a datetime object.
        
        Time features help the model understand patterns like:
        - Morning (hour = 8) uses less energy than afternoon (hour = 14)
        - Weekends (day_of_week = 5,6) might use different amounts
        - Winter (month = 1) might differ from summer (month = 7)
        
        Args:
            timestamp (datetime): The datetime to extract features from
            
        Returns:
            list: Seven features [hour, day_of_week, day_of_month, month,
                                   is_weekend, is_business_hour]
        """
        # ================================================================
        # Step 2: Extract time-based features from timestamp
        # ================================================================
        
        # Hour: 0-23 (0 = midnight, 12 = noon, 23 = 11pm)
        # Helps predict usage by time of day
        hour = timestamp.hour
        
        # Day of week: 0-6 (0 = Monday, 6 = Sunday)
        # Helps predict usage patterns (weekday vs weekend)
        day_of_week = timestamp.weekday()
        
        # Day of month: 1-31
        # Sometimes used for billing or pattern analysis
        day_of_month = timestamp.day
        
        # Month: 1-12
        # Helps predict seasonal patterns (winter vs summer)
        month = timestamp.month
        
        # Is it weekend? 1 = yes, 0 = no
        # Simplified feature: weekends = days 5,6 (Saturday, Sunday)
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Is it business hours? 1 = yes (9am-5pm), 0 = no
        # Helps predict high-usage periods
        is_business_hour = 1 if 9 <= hour < 17 else 0
        
        return [hour, day_of_week, day_of_month, month, is_weekend, is_business_hour]
    
    def prepare_data(self, data_df):
        """
        Convert raw energy data into features for the model.
        
        This takes a dataframe with timestamps and energy values,
        and converts it into a format the model can learn from.
        
        Args:
            data_df (DataFrame): Must have 'timestamp' and 'energy_consumed_kwh'
            
        Returns:
            tuple: (X_features, y_target) - Ready for training
        """
        # ================================================================
        # Step 3: Prepare data by extracting features from all records
        # ================================================================
        
        # List to store all feature rows
        features_list = []
        
        # Extract features from each record
        for idx, row in data_df.iterrows():
            # Convert to datetime if it's a string
            if isinstance(row['timestamp'], str):
                timestamp = pd.to_datetime(row['timestamp'])
            else:
                timestamp = row['timestamp']
            
            # Extract time features
            features = self.extract_time_features(timestamp)
            features_list.append(features)
        
        # Convert to numpy array for model training
        # Shape: (number_of_records, number_of_features)
        # Example: (1000, 6) = 1000 records with 6 features each
        X = np.array(features_list)
        
        # Target values: the actual energy consumption we're learning from
        y = data_df['energy_consumed_kwh'].values
        
        return X, y
    
    def train(self, data_df):
        """
        Train the Linear Regression model on historical energy data.
        
        The model learns: "When these features happen, this much energy is used"
        
        Example learning:
        - Feature set [14, 2, 15, 3, 0, 1] (2pm, Wednesday, 15th, March, not weekend, business hours)
        - Energy consumed: 45 kWh
        - The model learns: "2pm on weekday = ~45 kWh"
        
        Args:
            data_df (DataFrame): Must have columns 'timestamp' and 'energy_consumed_kwh'
            
        Returns:
            dict: Training metrics (R² score, MAE, RMSE)
        """
        # ================================================================
        # Step 4: Prepare the data
        # ================================================================
        X, y = self.prepare_data(data_df)
        
        # ================================================================
        # Step 5: Train the model
        # ================================================================
        # fit() teaches the model the relationship between features and energy
        # It finds coefficients (weights) for each feature
        # Example result: Energy = (2.5 × hour) + (3.1 × day_of_week) + ...
        self.model.fit(X, y)
        self.is_trained = True
        
        # ================================================================
        # Step 6: Calculate training metrics to evaluate performance
        # ================================================================
        
        # Make predictions on the same data
        y_pred = self.model.predict(X)
        
        # Calculate metrics
        mae = mean_absolute_error(y, y_pred)      # Average error in kWh
        rmse = np.sqrt(mean_squared_error(y, y_pred))  # Root mean squared error
        r2 = r2_score(y, y_pred)                   # How well it fits (0-1, higher is better)
        
        # Print results
        print("\n" + "="*70)
        print("MODEL TRAINING COMPLETE")
        print("="*70)
        print(f"Coefficient of Determination (R² Score): {r2:.4f}")
        print(f"  - 1.0 = Perfect predictions, 0.0 = No better than average")
        print(f"Mean Absolute Error (MAE): {mae:.2f} kWh")
        print(f"  - Average difference from actual: ±{mae:.2f} kWh")
        print(f"Root Mean Squared Error (RMSE): {rmse:.2f} kWh")
        print(f"  - Penalizes large errors more heavily")
        print("="*70)
        print(f"Model Coefficients (weights for each feature):")
        for feature_name, coefficient in zip(self.feature_names, self.model.coef_):
            print(f"  {feature_name:20s}: {coefficient:8.4f}")
        print(f"Intercept (base energy): {self.model.intercept_:.4f} kWh")
        print("="*70 + "\n")
        
        return {
            'r2_score': float(r2),
            'mae': float(mae),
            'rmse': float(rmse),
            'coefficients': dict(zip(self.feature_names, self.model.coef_)),
            'intercept': float(self.model.intercept_)
        }
    
    def predict(self, timestamp):
        """
        Predict energy consumption for a given time.
        
        Args:
            timestamp (datetime): When to predict energy consumption
            
        Returns:
            dict: Prediction details with consumption estimate
            
        Raises:
            RuntimeError: If model hasn't been trained yet
        """
        # ================================================================
        # Step 7: Validate that model is trained
        # ================================================================
        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before making predictions. "
                "Call train() with historical data first."
            )
        
        # ================================================================
        # Step 8: Extract features from the input timestamp
        # ================================================================
        features = self.extract_time_features(timestamp)
        
        # ================================================================
        # Step 9: Make prediction using trained model
        # ================================================================
        # Reshape features to 2D array (required by scikit-learn)
        X = np.array([features])
        
        # predict() returns the estimated energy consumption
        prediction = self.model.predict(X)[0]
        
        # Ensure prediction is not negative (can't have negative energy)
        prediction = max(0, prediction)
        
        return {
            'timestamp': timestamp.isoformat(),
            'predicted_energy_kwh': float(round(prediction, 2)),
            'features': {
                'hour': features[0],
                'day_of_week': features[1],
                'day_of_month': features[2],
                'month': features[3],
                'is_weekend': features[4],
                'is_business_hour': features[5]
            },
            'confidence': 'Model trained and ready for predictions'
        }
    
    def predict_range(self, start_date, end_date, frequency='H'):
        """
        Predict energy consumption for a range of dates.
        
        Args:
            start_date (datetime): Start of prediction range
            end_date (datetime): End of prediction range
            frequency (str): Frequency ('H' = hourly, 'D' = daily, etc.)
            
        Returns:
            DataFrame: Predictions for each timestamp
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before making predictions.")
        
        # Generate timestamps for the range
        timestamps = pd.date_range(start=start_date, end=end_date, freq=frequency)
        
        # Extract features for all timestamps
        features_list = []
        for ts in timestamps:
            features = self.extract_time_features(ts)
            features_list.append(features)
        
        X = np.array(features_list)
        predictions = self.model.predict(X)
        
        # Ensure no negative predictions
        predictions = np.maximum(predictions, 0)
        
        # Create results dataframe
        results_df = pd.DataFrame({
            'timestamp': timestamps,
            'predicted_energy_kwh': predictions
        })
        
        return results_df
    
    def explain_model(self):
        """
        Explain how the trained model makes predictions in plain language.
        
        Returns:
            str: Human-readable explanation of the model
        """
        if not self.is_trained:
            return "Model not trained yet. Call train() first."
        
        explanation = "\n" + "="*70 + "\n"
        explanation += "HOW THE MODEL WORKS\n"
        explanation += "="*70 + "\n\n"
        
        explanation += "The model uses this formula:\n"
        explanation += "Energy (kWh) = Base + (Hour × {:+.4f}) + (Day of Week × {:+.4f}) + ...\n\n".format(
            self.model.coef_[0], self.model.coef_[1]
        )
        
        explanation += "Interpretation:\n"
        explanation += "-" * 70 + "\n"
        
        # Interpret coefficients
        for feature_name, coef in zip(self.feature_names, self.model.coef_):
            direction = "increases" if coef > 0 else "decreases"
            impact = f"{abs(coef):.4f} kWh"
            explanation += f"• {feature_name}: Each unit {direction} energy by {impact}\n"
        
        explanation += f"\n• Base Energy (Intercept): {self.model.intercept_:.2f} kWh\n"
        explanation += "  (Energy consumed regardless of time)\n"
        
        explanation += "\n" + "="*70 + "\n"
        explanation += "EXAMPLE PREDICTION\n"
        explanation += "="*70 + "\n"
        
        # Show an example calculation
        example_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
        example = self.predict(example_time)
        
        explanation += f"Time: {example_time.strftime('%A, %I:%M %p')}\n"
        explanation += f"Predicted Energy: {example['predicted_energy_kwh']} kWh\n"
        explanation += f"Calculated as:\n"
        explanation += f"  Base: {self.model.intercept_:.2f} kWh\n"
        
        features = example['features']
        for feature_name, value in features.items():
            idx = self.feature_names.index(feature_name)
            contribution = value * self.model.coef_[idx]
            explanation += f"  + {feature_name} ({value}) × {self.model.coef_[idx]:.4f} = {contribution:.2f} kWh\n"
        
        explanation += "\n" + "="*70 + "\n"
        
        return explanation


# ============================================================================
# Example Usage
# ============================================================================

def create_sample_data(num_records=1000):
    """
    Create sample energy consumption data for demonstration.
    
    This generates realistic energy patterns:
    - Higher consumption during business hours
    - Lower consumption at night
    - Slightly higher on weekdays than weekends
    
    Args:
        num_records (int): Number of data points to generate
        
    Returns:
        DataFrame: Sample energy data with timestamps and consumption
    """
    print("\n" + "="*70)
    print("CREATING SAMPLE DATA")
    print("="*70)
    
    # Generate timestamps (last 60 days, hourly)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='H')[:num_records]
    
    # Generate realistic energy consumption
    energy_values = []
    for ts in timestamps:
        # Base consumption
        base = 20
        
        # Hour factor (higher during day, lower at night)
        hour_factor = 15 * np.sin((ts.hour - 6) * np.pi / 24)
        
        # Day of week factor (slightly higher on weekdays)
        day_factor = 5 if ts.weekday() < 5 else 2
        
        # Random variation
        noise = np.random.normal(0, 3)
        
        # Total consumption
        total = max(base + hour_factor + day_factor + noise, 5)
        energy_values.append(total)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'energy_consumed_kwh': energy_values
    })
    
    print(f"Generated {len(df)} records from {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Energy consumption range: {df['energy_consumed_kwh'].min():.2f} - {df['energy_consumed_kwh'].max():.2f} kWh")
    print("="*70 + "\n")
    
    return df


if __name__ == "__main__":
    """
    Demonstration of the energy prediction model.
    """
    print("\n" + "="*70)
    print("ENERGY CONSUMPTION PREDICTION MODEL DEMO")
    print("="*70)
    
    # Step 1: Create sample training data
    training_data = create_sample_data(1000)
    
    # Step 2: Initialize and train the model
    predictor = EnergyConsumptionPredictor()
    metrics = predictor.train(training_data)
    
    # Step 3: Make individual predictions
    print("\n" + "="*70)
    print("MAKING PREDICTIONS")
    print("="*70)
    
    # Predict for different times
    test_times = [
        datetime.now().replace(hour=8, minute=0),   # 8am
        datetime.now().replace(hour=14, minute=0),  # 2pm
        datetime.now().replace(hour=22, minute=0),  # 10pm
    ]
    
    for test_time in test_times:
        prediction = predictor.predict(test_time)
        day_name = test_time.strftime('%A')
        hour = test_time.strftime('%I:%M %p')
        energy = prediction['predicted_energy_kwh']
        print(f"{day_name} at {hour}: {energy:.2f} kWh")
    
    # Step 4: Explain the model
    print(predictor.explain_model())
    
    # Step 5: Predict for next 7 days (hourly)
    print("="*70)
    print("7-DAY HOURLY FORECAST")
    print("="*70)
    future_start = datetime.now()
    future_end = future_start + timedelta(days=7)
    forecast_df = predictor.predict_range(future_start, future_end, frequency='H')
    
    print(f"\nGenerated {len(forecast_df)} hourly predictions for next 7 days")
    print("\nSample predictions:")
    print(forecast_df.head(10).to_string(index=False))
    print("\nForecast Statistics:")
    print(f"  Average: {forecast_df['predicted_energy_kwh'].mean():.2f} kWh")
    print(f"  Min: {forecast_df['predicted_energy_kwh'].min():.2f} kWh")
    print(f"  Max: {forecast_df['predicted_energy_kwh'].max():.2f} kWh")
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70 + "\n")
