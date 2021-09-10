"""
Predict the max combo in 8 steps
"""

# %%
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd

# %%
# Define the model
model = keras.Sequential(name="pazulove")
model.add(keras.Input(shape=(30,)))  # 6 x 5 boards
model.add(layers.Dense(10, activation="relu", name="layer1"))
model.add(layers.Dense(10, activation="relu", name="layer2"))
# 0 - 11
model.add(layers.Dense(11, activation="softmax", name="predictions"))
model.summary()

# %%
# Load data from csv
csv_name = "data8_normal.csv"
full_data = pd.read_csv("../../data/{}".format(csv_name))
partial_data = full_data.sample(frac=0.1)

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

# update output to float
train_y = train_y.astype("float32")
test_y = test_y.astype("float32")

# build the model
model.compile(
    optimizer=keras.optimizers.RMSprop(),
    loss=keras.losses.SparseCategoricalCrossentropy(),
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)

# %%
print("Fit model on training data")
history = model.fit(
    train_x,
    train_y,
    # batch_size=64,
    epochs=200,
    # validation_data=(x_val, y_val),
)

# %%
print("Evaluate on test data")
results = model.evaluate(test_x, test_y, batch_size=128)
print("test loss, test acc:", results)

print("Get predictions for 3 samples")
predictions = model.predict(test_x[:3])
print("predictions:", predictions)
print(test_y[:3])

# %%
