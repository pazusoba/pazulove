"""
Predict the max combo in 8 steps
"""

# %%
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np

# %%
# Define the model
model = keras.Sequential(name="pazulove")
model.add(keras.Input(shape=(30,)))  # 6 x 5 boards
model.add(layers.Dense(120, activation="relu", name="layer1"))
# model.add(layers.Dense(10, activation="relu", name="layer2"))
# 0 - 10 are all possible outputs
# for now, we only have 3 - 8 so 6 values
model.add(layers.Dense(9, activation="softmax", name="predictions"))
model.summary()

# %%
# Load data from csv
csv_name = "data8_normal.csv"
full_data = pd.read_csv("../../data/{}".format(csv_name))
partial_data = full_data.sample(frac=0.02)
print("Using {} data".format(partial_data.shape))

# %%
# take the first 80% as training data
train_data = partial_data.iloc[:int(len(partial_data) * 0.8)]
test_data = partial_data.iloc[int(len(partial_data) * 0.8):]

train_x = train_data.drop(columns=["combo"])
train_y = train_data["combo"]

test_x = test_data.drop(columns=["combo"])
test_y = test_data["combo"]

# %%
# normalize the input data
# TODO: better normalise data here
train_x = train_x.astype("float32")
train_x = train_x / 5.0
test_x = test_x.astype("float32")
test_x = test_x / 5.0

# update output to float
train_y = train_y.astype("float32")
test_y = test_y.astype("float32")

# build the model
model.compile(
    optimizer=keras.optimizers.RMSprop(lr=0.0001),
    loss=keras.losses.SparseCategoricalCrossentropy(),
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)

# %%
print("Fit model on training data")
history = model.fit(
    train_x,
    train_y,
    epochs=500,
    validation_data=(test_x, test_y),
)

# %%
print("Evaluate on test data")
results = model.evaluate(test_x, test_y)
print("test loss, test acc:", results)

predictions = model.predict(test_x[:10])
predictions = np.argmax(predictions, axis=1)
# argmax find the max in that array and axis=1 is horizontal index (index in that array)
print("predictions:", predictions)
print(test_y[:10])

# %%
print("Test overall performance")
all_x = full_data.drop(columns=["combo"])
all_y = full_data["combo"]
results = model.evaluate(all_x, all_y)
print("test loss, test acc:", results)

# %%
