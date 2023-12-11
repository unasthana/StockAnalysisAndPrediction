import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from stockanalysisandprediction.management.commands.train_prediction_model.py import (
    getStockData,
    getTargetData,
    standardizeData,
    createDataPartitions,
    getPredictions,
    getStocktTickers
)


def makePrediction(data, stock_ticker):
    # Get Stock Data particular to the corresponding stock ticker.
    stock_data = getStockData(data, "AAL")

    # Get Target Data. In our case, we are predicting the Close Price of the Stock.
    target_data = getTargetData(stock_data, "close")

    # Standardize the data for quicker convergence.
    scaled_data, scaler = standardizeData(target_data)

    # Create data sequences for training and testing. I am doing a 0.95 train/test split.
    x_train, y_train, x_test, y_test = createDataPartitions(
        scaled_data, target_data, 0.95
    )

    model = tf.keras.models.load_model(f"/content/lstm_{stock_ticker}.h5")
    result_df, rmse = getPredictions(model, scaler, x_test, y_test)

    trainset_length = int(len(stock_data) * 0.95)
    train_data = stock_data[["close"]][:trainset_length]
    test_data = stock_data[["close"]][trainset_length:]
    test_data["predicted"] = result_df

    return train_data, test_data


def makeCluster(data, time = '1_week'):

  stock_tickers = getStockTickers(data)
  combined_df = pd.DataFrame()

  for stock_ticker in stock_tickers:

      stock_data = getStockData(data, stock_ticker)

      if len(stock_data) < 252:
          continue  

      stock_data['Daily_Returns'] = stock_data['close'].pct_change()
      stock_data['Risk'] = stock_data['Daily_Returns'].rolling(window=22).std()

      time_values = {"all_time": len(stock_data), "1_week": 5, "2_weeks": 10,
                    "1_month": 22, "1_quarter": 66, "6_months": 132,
                    "1_year": 253}

      if time.startswith('custom'):
          time_value = int(time[7:])
          time = 'custom'
          time_values["custom"] = time_value

      stock_data = stock_data.tail(time_values[time])

      combined_df = pd.concat([combined_df, stock_data[['Name', 'Daily_Returns', 'Risk']]])

  combined_df.fillna(method='bfill', inplace=True)

  # Extract relevant features for clustering
  features = combined_df[['Daily_Returns', 'Risk']]

  # Standardize the features to have zero mean and unit variance
  scaler = StandardScaler()
  features_standardized = scaler.fit_transform(features)

  # K-Means Clustering
  num_clusters = 5
  kmeans = KMeans(n_clusters=num_clusters, random_state=42)
  combined_df['cluster'] = kmeans.fit_predict(features_standardized)

  combined_df.index = pd.to_datetime(combined_df.index)

  cluster_df = combined_df.groupby('Name').last()

  cluster_df = cluster_df[['cluster']]
  cluster_df = cluster_df.reset_index()

  return cluster_df
