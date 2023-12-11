import shutil
import os
import pandas as pd
import numpy as np
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM


def getStockTickers(data):
    return data["Name"].unique()


def getStockData(data, stock_ticker):
    stock_data = data[data["Name"] == stock_ticker]

    return stock_data


def getTargetData(data, target):
    target_data = data[target]
    target_data = np.array(target_data).reshape(-1, 1)

    return target_data


def standardizeData(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    return scaled_data, scaler


def createDataPartitions(scaled_data, original_data, split_ratio):
    trainset_length = int(len(scaled_data) * split_ratio)
    train_data = scaled_data[:trainset_length]

    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60 : i])
        y_train.append(train_data[i : i + 1])

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    test_data = scaled_data[trainset_length - 60 :]

    x_test = []
    y_test = original_data[trainset_length:]

    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60 : i])

    x_test = np.array(x_test)

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    return x_train, y_train, x_test, y_test


def buildModel(x_train):
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    return model


def getPredictions(model, scaler, x_test, y_test):
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))

    return predictions, rmse


def zipModels(source_folder, destination_folder):
    shutil.make_archive(destination_folder, "zip", source_folder)
    print("Zipping completed!")


class RMSECallback(tf.keras.callbacks.Callback):
    def __init__(self, model_filename, scaler, x_test, y_test):
        super(RMSECallback, self).__init__()

        self.model_filename = model_filename
        self.best_rmse = float("inf")
        self.scaler = scaler
        self.x_test = x_test
        self.y_test = y_test


def on_epoch_end(self, epoch, logs=None):
    predictions, rmse = getPredictions(
        self.model, self.scaler, self.x_test, self.y_test
    )

    print(f"RMSE on test data: {rmse:.2f}\n")

    if rmse < 5:
        print("Reached RMSE < 5. Stopping training.\n")
        self.model.stop_training = True

    if rmse < self.best_rmse:
        print(f"Saving model with RMSE: {rmse:.2f}\n")

        self.best_rmse = rmse
        self.model.save(f"/content/prediction_models/{self.model_filename}.h5")


def main():
    data = pd.read_csv("/content/all_stocks_5yr.csv")
    data.set_index("date", inplace=True)
    data.dropna(inplace=True)

    stock_tickers = getStockTickers(data)

    for stock_ticker in stock_tickers:
        stock_data = getStockData(data, stock_ticker)

        if len(stock_data) < 60:
            continue

        target_data = getTargetData(stock_data, "close")

        scaled_data, scaler = standardizeData(target_data)

        x_train, y_train, x_test, y_test = createDataPartitions(
            scaled_data, target_data, 0.95
        )

        model = buildModel(x_train)

        model.compile(optimizer="adam", loss="mean_squared_error")

        print(f"\nTraining on {stock_ticker} data...\n")

        model.fit(
            x_train,
            y_train,
            epochs=20,
            batch_size=1,
            callbacks=[
                RMSECallback(
                    model_filename=f"lstm_{stock_ticker}",
                    scaler=scaler,
                    x_test=x_test,
                    y_test=y_test,
                )
            ],
        )

    zipModels(
        source_folder="/content/prediction_models",
        destination_folder="/content/zipped_models",
    )


if __name__ == "__main__":
    main()
