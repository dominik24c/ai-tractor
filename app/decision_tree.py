#!/usr/bin/python3
import os
from typing import Union
import pydotplus
import pandas as pd
from joblib import dump, load
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz, export_text

from app.weather import Weather
from config import *


class DecisionTree:
    WEATHER = {W_SUNNY: 0, W_CLOUDY: 1, W_SNOW: 2, W_RAINY: 3}
    SEASON = {S_AUTUMN: 0, S_WINTER: 1, S_SPRING: 2, S_SUMMER: 3}
    FEATURES = ['Season', 'Weather', 'Fertilize', 'Hydrate', 'Sow', 'Harvest', 'Action']

    def __int__(self):
        self.tree = None

    def learn_tree(self) -> None:
        path = os.path.join(DATA_DIR, MODEL_TREE_FILENAME)
        if os.path.exists(path):
            self.tree = load(path)
        else:
            # read data
            training_data = pd.read_csv(os.path.join(DATA_DIR, DATA_TRAINING_FOR_DECISION_TREE))
            print(training_data.head())

            training_data = self.map_data(training_data)
            # print(training_data)

            X = training_data[self.FEATURES[:-1]]
            Y = training_data[self.FEATURES[-1]]

            self.tree = DecisionTreeClassifier()
            self.tree = self.tree.fit(X, Y)
            dump(self.tree, path)

        text = export_text(self.tree, feature_names=self.FEATURES[:-1])
        print(text)

        data = export_graphviz(self.tree, out_file=None, feature_names=self.FEATURES[:-1])
        graph = pydotplus.graph_from_dot_data(data)
        graph.write_png(os.path.join(DATA_DIR, IMG_DECISION_TREE))

    def map_data(self, data: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
        # print(data)
        data['Season'] = data['Season'].map(DecisionTree.SEASON)
        data['Weather'] = data['Weather'].map(DecisionTree.WEATHER)
        return data

    def predict(self, vector: Union[pd.Series, pd.DataFrame]) -> str:
        print(vector)
        x = self.map_data(vector)
        action = self.tree.predict(x)
        return action

    def make_decision(self, weather: Weather, v: list):
        s, w = weather.randomize_weather()
        tree = DecisionTree()
        tree.learn_tree()
        final_vector = [s, w] + v
        print(final_vector)
        df = pd.DataFrame([final_vector])
        df.columns = DecisionTree.FEATURES[:-1]
        return tree.predict(df)
