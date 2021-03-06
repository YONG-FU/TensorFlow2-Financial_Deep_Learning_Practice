import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf

layer = tf.keras.layers.Dense(2, activation='relu')

x = tf.constant([[1,2,3]])

with tf.GradientTape() as tape:
    #forward pass
    y = layer(x)
    loss = tf.reduce_mean(y**2)

grad = tape.gradient(loss, layer.trainable_variables)

for var, g in zip(layer.trainable_variables, grad):
    print(f'{var.name}, shape:{g.shape}')
