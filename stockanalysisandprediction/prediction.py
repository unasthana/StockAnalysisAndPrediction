import tempfile

import pandas as pd
import tensorflow as tf
from django.http import JsonResponse
from pymongo import MongoClient
from gridfs import GridFS
import os
from rest_framework.decorators import api_view
from stockanalysisandprediction.management.commands.train_prediction_model import (
    getTargetData,
    standardizeData,
    createDataPartitions,
    getPredictions,
)
from stockanalysisandprediction.models import Stock

client = MongoClient(
    "mongodb+srv://viveknayak:I8gipVxwYPxoTemh@stockanalysisandpredict.eckfrb9.mongodb.net/"
)
db = client["model_files"]
fs = GridFS(db)


def load_model(ticker):
    file = fs.find_one({"metadata.ticker": ticker}, sort=[("uploadDate", -1)])
    _, temp_path = tempfile.mkstemp(suffix=".h5")

    with open(temp_path, "wb") as f:
        f.write(file.read())

    model = tf.keras.models.load_model(temp_path)
    os.remove(temp_path)
    return model


@api_view(["GET"])
def makePrediction(request, stock_ticker):
    # Get Stock Data particular to the corresponding stock ticker.
    stock_data = Stock.objects.filter(name=stock_ticker).values()
    stock_data = pd.DataFrame(list(stock_data)).set_index("date")
    # Get Target Data. In our case, we are predicting the Close Price of the Stock.
    target_data = getTargetData(stock_data, "close")

    # Standardize the data for quicker convergence.
    scaled_data, scaler = standardizeData(target_data)

    # Create data sequences for training and testing. I am doing a 0.95 train/test split.
    x_train, y_train, x_test, y_test = createDataPartitions(
        scaled_data, target_data, 0.95
    )

    model = load_model(stock_ticker)
    result_df, rmse = getPredictions(model, scaler, x_test, y_test)

    trainset_length = int(len(stock_data) * 0.95)
    train_data = stock_data[["close"]][:trainset_length]
    test_data = stock_data[["close"]][trainset_length:]
    test_data["predicted"] = result_df
    test_data.index = test_data.index.astype(str)
    train_data.index = train_data.index.astype(str)
    return JsonResponse(
        {"train": train_data.to_dict(), "test": test_data.to_dict()}, safe=False
    )
