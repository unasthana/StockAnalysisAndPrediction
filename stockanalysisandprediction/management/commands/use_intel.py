import tensorflow as tf

from stockanalysisandprediction.management.commands.train_prediction_model.py import (
    getStockData,
    getTargetData,
    standardizeData,
    createDataPartitions,
    getPredictions,
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
