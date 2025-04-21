import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def predict_drought(data: pd.Series, forecast_days: int = 7):
    """Previsione siccità con modello ARIMA."""
    model = ARIMA(data, order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_days)
    return forecast
