import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (mean_absolute_error, r2_score, mean_absolute_percentage_error,
                             mean_squared_error, accuracy_score, f1_score)
from SP import SpotifyClient
from sklearn.preprocessing import PolynomialFeatures
import seaborn as sns


def print_regression_metrics(y_true, y_pred):
    # Mean Absolute Error
    mae = mean_absolute_error(y_true, y_pred)
    # R-squared score
    r2 = r2_score(y_true, y_pred)
    # Mean Absolute Percentage Error
    mape = mean_absolute_percentage_error(y_true, y_pred)
    # Root Mean Squared Error
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    print("MAE:", mae)
    print("R²:", r2)
    print("MAPE:", mape * 100, "%")
    print("RMSE:", rmse)

class PopularityPrediction():

    def popularity_prediction(self, df):

        # Print all popularity values
        print("__________________________________________")
        print("All Popularity Values in Dataset:")
        print(df['popularity'])
        print("__________________________________________")

        # Preprocess data
        # Convert release_date to release_year and drop release_date
        df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
        df = df.drop(columns=['release_date'], errors='ignore')

        # Convert explicit to integer
        df['explicit'] = df['explicit'].astype(int)

        # One-hot encode album_type
        df = pd.get_dummies(df, columns=['album_type'], drop_first=True)


        # 5. Force all columns to numeric (if conversion fails, value becomes NaN)
        df = df.apply(pd.to_numeric, errors='coerce')

        # Display the processed DataFrame and data types
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 50)
        print("\n Processed DataFrame:")
        print(df.head())
        print("\n Data Types After Processing:")
        print(df.dtypes)

        correlation_matrix = df.corr()
        feature_correlation = correlation_matrix["popularity"].drop("popularity").sort_values(ascending=False)
        print("\nFeature Importance Based on Correlation:")
        print(feature_correlation)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=feature_correlation.values, y=feature_correlation.index, palette="coolwarm")
        plt.title("Feature Importance Based on Correlation with Popularity")
        plt.xlabel("Correlation Coefficient")
        plt.ylabel("Feature")
        plt.show()



        # Predictors (we use the one-hot encoded album_type columns automatically added)
        predictor_columns = ['popularity_of_artists', 'release_year', 'album_type_single'] \
                            + [col for col in df.columns if col.startswith('album_')]
        X = df[predictor_columns]

        # Target
        y = df['popularity']

        # Data splitting
        X_train, X_test, y_train_reg, y_test_reg = train_test_split(X, y, test_size=0.2, random_state=42)

        correlation_matrix = X_train.corr()
        sns.heatmap(correlation_matrix, cmap="coolwarm", annot=True)
        plt.title("Feature Correlation Matrix")
        plt.show()

        # Multiple Linear Regression
        print("__________________________________________")
        print("Multiple Linear Regression:")
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train_reg)
        y_pred_reg = lr_model.predict(X_test)
        print_regression_metrics(y_test_reg, y_pred_reg)

        # Plot the scatter points
        plt.scatter(y_test_reg, y_pred_reg, alpha=0.7, color='blue')
        # Add perfect prediction line
        plt.plot([min(y_test_reg), max(y_test_reg)], [min(y_test_reg), max(y_test_reg)], 'r--')
        plt.xlabel('Actual Popularity')
        plt.ylabel('Predicted Popularity')
        plt.title('Linear Regression: Actual vs Predicted Popularity')
        plt.show()

        # Polynomial Regression
        print("__________________________________________")
        print("Polynomial Regression:")
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_train_poly = poly.fit_transform(X_train)
        X_test_poly = poly.transform(X_test)
        poly_model = LinearRegression()
        poly_model.fit(X_train_poly, y_train_reg)
        y_pred_poly = poly_model.predict(X_test_poly)
        print_regression_metrics(y_test_reg, y_pred_poly)


        # Lasso Regression
        print("__________________________________________")
        print("Lasso Regression:")
        lasso_model = Lasso(alpha=0.1)
        lasso_model.fit(X_train, y_train_reg)
        y_pred_lasso = lasso_model.predict(X_test)
        print_regression_metrics(y_test_reg, y_pred_lasso)

        # Ridge Regression
        print("__________________________________________")
        print("Ridge Regression:")
        ridge_model = Ridge(alpha=1.0)
        ridge_model.fit(X_train, y_train_reg)
        y_pred_ridge = ridge_model.predict(X_test)
        print_regression_metrics(y_test_reg, y_pred_ridge)

        # Random Forest Regression
        print("__________________________________________")
        print("Random Forest Regression:")

        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train_reg)
        y_pred_rf = rf_model.predict(X_test)

        print_regression_metrics(y_test_reg, y_pred_rf)


