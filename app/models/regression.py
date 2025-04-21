from sklearn.linear_model import LinearRegression
import pandas as pd

def predict_yield(X: pd.DataFrame, y: pd.Series):
    """Modello di regressione multivariata per previsione rese."""
    model = LinearRegression()
    model.fit(X, y)
    return model
