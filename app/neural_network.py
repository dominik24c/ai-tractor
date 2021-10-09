#!/usr/bin/python3
import os

from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras as k
import numpy as np

from app.base_field import BaseField
from config import *


class NeuralNetwork:
    def __init__(self):
        # Model config
        self.batch_size = 25
        self.img_width, self.img_height, self.img_num_channels = 25, 25, 3
        self.loss_function = sparse_categorical_crossentropy
        self.no_classes = 8
        self.no_epochs = 40
        self.optimizer = Adam()
        self.verbosity = 1

        # Determine shape of the data
        self.input_shape = (self.img_width, self.img_height, self.img_num_channels)

        # labels
        self.labels = ["cabbage", "carrot", "corn", "lettuce", "paprika", "potato", "sunflower", "tomato"]

    def init_model(self) -> None:
        if not self.model_dir_is_empty():
            # Load the model
            self.model = load_model(
                os.path.join(RESOURCE_DIR, "saved_model"),
                custom_objects=None,
                compile=True
            )
        else:
            # Create the model
            self.model = Sequential()
            self.model.add(Conv2D(16, kernel_size=(5, 5), activation='relu', input_shape=self.input_shape))
            self.model.add(Conv2D(32, kernel_size=(5, 5), activation='relu'))
            self.model.add(Conv2D(64, kernel_size=(5, 5), activation='relu'))
            self.model.add(Conv2D(128, kernel_size=(5, 5), activation='relu'))
            self.model.add(Flatten())
            self.model.add(Dense(16, activation='relu'))
            self.model.add(Dense(self.no_classes, activation='softmax'))

            self.model.compile(loss=self.loss_function,
                               optimizer=self.optimizer,
                               metrics=['accuracy'])

            # Start training
            self.model.fit(
                self.train_datagen,
                epochs=self.no_epochs,
                shuffle=False)

        # Display a model summary
        # self.model.summary()

    def load_images(self) -> None:
        # Create a generator
        self.train_datagen = ImageDataGenerator(
            rescale=1. / 255
        )
        self.train_datagen = self.train_datagen.flow_from_directory(
            TRAINING_SET_DIR,
            save_to_dir=ADAPTED_IMG_DIR,
            save_format='jpeg',
            batch_size=self.batch_size,
            target_size=(25, 25),
            class_mode='sparse')

    def predict(self, field: BaseField) -> str:
        print(field.get_img_path())
        # corn_img_path = os.path.join(RESOURCE_DIR,'corn.png')
        loaded_image = k.preprocessing.image.load_img(field.get_img_path(),
                                                      target_size=(
                                                          self.img_width, self.img_height, self.img_num_channels))

        # convert to array and resample dividing by 255
        img_array = k.preprocessing.image.img_to_array(loaded_image) / 255.

        # add sample dimension. the predictor is expecting (1, CHANNELS, IMG_WIDTH, IMG_HEIGHT)
        img_np_array = np.expand_dims(img_array, axis=0)
        # print(img_np_array)
        predictions = self.model.predict(img_np_array)
        prediction = np.argmax(predictions[0])

        label = self.labels[prediction]
        print(f'Ground truth: {type(field).__name__} - Prediction: {label}')
        return label

    def model_dir_is_empty(self) -> bool:
        if len(os.listdir(MODEL_DIR)) == 0:
            return True
        return False

    def check(self, field: BaseField) -> str:
        self.load_images()
        self.init_model()
        prediction = self.predict(field)

        # Saving model
        if self.model_dir_is_empty():
            save_model(self.model, MODEL_DIR)

        return prediction
