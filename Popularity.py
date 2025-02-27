import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_absolute_percentage_error, mean_squared_error
from SP import SpotifyClient


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    """Train a model and print its performance metrics."""
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"______{name}______")
    print(f"MAE: {mae:.4f}")
    print(f"R²: {r2:.4f}")
    print(f"MAPE: {mape * 100:.2f}%")
    print(f"RMSE: {rmse:.4f}")

    return model, y_pred


def main():
    # Dictionary of tracks and artists
    TRACKS = {
        "Blinding Lights": "The Weeknd",
        "Shape of You": "Ed Sheeran",
        "Dance Monkey": "Tones and I",
        # Shortened list for simplicity - actual implementation would use full list
        "Life Is Good": "Future feat. Drake"
    }

    # Fetch data
    client = SpotifyClient()
    df = client.get_track_properties(TRACKS)

    # Data preprocessing
    # Convert release_date to year
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    df = df.drop(columns=['release_date'], errors='ignore')

    # Convert explicit to integer
    df['explicit'] = df['explicit'].astype(int)

    # One-hot encode categorical variables
    df = pd.get_dummies(df, columns=['album_type'], drop_first=True)

    # Convert all columns to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # Display basic dataset info
    print("\nDataset preview:")
    print(df.head())

    # Show correlations with popularity
    correlation_with_popularity = df.corr()["popularity"].drop("popularity").sort_values(ascending=False)
    print("\nFeature correlation with popularity:")
    print(correlation_with_popularity)

    # Visualize correlations
    plt.figure(figsize=(10, 6))
    sns.barplot(x=correlation_with_popularity.values, y=correlation_with_popularity.index, palette="coolwarm")
    plt.title("Feature Correlation with Popularity")
    plt.xlabel("Correlation Coefficient")
    plt.tight_layout()
    plt.show()

    # Prepare data for modeling
    predictor_columns = [
                            'popularity_of_artists',
                            'release_year',
                            'explicit'
                        ] + [col for col in df.columns if col.startswith('album_type_')]

    X = df[predictor_columns]
    y = df['popularity']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train and evaluate models
    models = {
        "Linear Regression": LinearRegression(),
        "Lasso Regression": Lasso(alpha=0.1),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
    }

    results = {}
    for name, model in models.items():
        trained_model, predictions = evaluate_model(name, model, X_train, X_test, y_train, y_test)
        results[name] = (trained_model, predictions)

    # Visualize predictions vs actual for best model
    best_model_name = "Random Forest"  # Typically the best performer for this type of data
    _, best_preds = results[best_model_name]

    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, best_preds, alpha=0.7)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel('Actual Popularity')
    plt.ylabel('Predicted Popularity')
    plt.title(f'{best_model_name} Predictions vs Actual')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()