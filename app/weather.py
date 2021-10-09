#!/usr/bin/python3
import random
from config import *


class Weather:
    def __init__(self):
        self.months = (S_WINTER, S_WINTER, S_SPRING, S_SPRING, S_SPRING, S_SUMMER,
                       S_SUMMER, S_SUMMER, S_AUTUMN, S_AUTUMN, S_AUTUMN, S_WINTER)
        self.current_month = 0

    def randomize_weather(self) -> tuple[str, str]:
        season = self.months[self.current_month]

        if season == S_WINTER:
            weather = random.choices([W_SNOW, W_CLOUDY])
        elif season == S_SUMMER:
            weights = [0.5, 0.3, 0.2]
            weather = random.choices([W_SUNNY, W_CLOUDY, W_RAINY], weights)
        elif season == S_SPRING:
            weights = [0.3, 0.5, 0.2]
            weather = random.choices([W_SUNNY, W_CLOUDY, W_RAINY], weights)
        else:
            weights = [0.2, 0.3, 0.4]
            weather = random.choices([W_SUNNY, W_CLOUDY, W_RAINY], weights)

        self.current_month = (self.current_month + 1) % len(self.months)
        return season, weather[0]
