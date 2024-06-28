from .settings import *
import os
from os.path import isfile
import numpy as np
import tensorflow as tf

class HandwrittenRecognition:
    def __init__(self):        
        self.modelPath = MODEL_PATH

        mnist = tf.keras.datasets.mnist
        (imageTrain, labelTrain), (imageTest, labelTest) = mnist.load_data()

        self.imageTest = tf.keras.utils.normalize(imageTest, axis=1)
        self.imageTrain = tf.keras.utils.normalize(imageTrain, axis=1)
        self.labelTrain = labelTrain
        self.labelTest = labelTest

    def train(self):
        try:
            model = tf.keras.models.Sequential()
            model.add(tf.keras.layers.Flatten(input_shape=(INPUT_SIZE, INPUT_SIZE)))
            for _ in range(HIDDEN_LAYERS):
                model.add(tf.keras.layers.Dense(NODES_IN_HIDDEN_LAYERS, activation='relu'))
            model.add(tf.keras.layers.Dense(10, activation='softmax'))

            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

            model.fit(self.imageTrain, self.labelTrain, epochs=EPOCHS)

            model.save(self.modelPath)
            return True
        except:
            return False

    def test(self):
        if not isfile(self.modelPath):
            raise Exception('Run the train first')

        model = tf.keras.models.load_model(self.modelPath)

        loss, accuracy = model.evaluate(self.imageTest, self.labelTest)
        return accuracy

    def run(self, grid):
        if not isfile(self.modelPath):
            raise Exception('Run the train first')

        model = tf.keras.models.load_model(self.modelPath)

        sanitizedGrid = []
        for r, row in enumerate(grid):
            sanitizedGrid.append([])
            for _, col in enumerate(row):
                sanitizedGrid[r].append(255 if col == WHITE else 0)
        
        sanitizedGrid = np.array([sanitizedGrid])

        try:
            prediction = model.predict(sanitizedGrid)
            return np.argmax(prediction), prediction
        except Exception as e:
            raise Exception(str(e))
