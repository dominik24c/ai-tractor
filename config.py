#!/usr/bin/python3

import os

__all__ = (
    'WIDTH', 'HEIGHT', 'FIELD_SIZE', 'TIME_OF_MOVING',
    'VERTICAL_NUM_OF_FIELDS', 'HORIZONTAL_NUM_OF_FIELDS',
    'FPS', 'CAPTION', 'RESOURCE_DIR', 'MAP_DIR', 'TRACTOR', 'PNG',
    'SAND', 'CLAY', 'GRASS', 'CORN', 'SUNFLOWER',
    'FIELD_TYPES', 'TIME_OF_GROWING', 'AMOUNT_OF_CROPS',
    'M_GO_FORWARD', 'M_ROTATE_LEFT', 'M_ROTATE_RIGHT',
    'S_AUTUMN', 'S_SPRING', 'S_SUMMER', 'S_WINTER', 'TYPES_OF_SEASON',
    'W_SUNNY', 'W_CLOUDY', 'W_SNOW', 'W_RAINY', 'TYPES_OF_WEATHER',
    'A_SOW', 'A_HARVEST', 'A_HYDRATE', 'A_FERTILIZE', 'A_DO_NOTHING',
    'TYPES_OF_ACTION', 'D_NORTH', 'D_EAST', 'D_SOUTH', 'D_WEST',
    'VALUE_OF_CROPS', 'VALUE_OF_PLANT', 'VALUE_OF_SAND', 'VALUE_OF_CLAY',
    'MAP_FILE_NAME', 'JSON', 'SAVE_MAP', 'LOAD_MAP', 'AUTO_MODE',
    'TRAINING_SET_DIR', 'TEST_SET_DIR', 'ADAPTED_IMG_DIR', 'MODEL_DIR',
    'DATA_DIR','IMG_DECISION_TREE','MODEL_TREE_FILENAME','DATA_TRAINING_FOR_DECISION_TREE'
)

# Board settings:
VERTICAL_NUM_OF_FIELDS = 9
HORIZONTAL_NUM_OF_FIELDS = 12
FIELD_SIZE = 60
WIDTH = HORIZONTAL_NUM_OF_FIELDS * FIELD_SIZE
HEIGHT = VERTICAL_NUM_OF_FIELDS * FIELD_SIZE

# Other settings
FPS = 10
CAPTION = 'Tractor'

# Paths
BASE_DIR = os.path.dirname(__file__)
RESOURCE_DIR = os.path.join(BASE_DIR, 'resources')
MAP_DIR = os.path.join(BASE_DIR, 'maps')
DATA_DIR = os.path.join(BASE_DIR, 'data')
MAP_FILE_NAME = 'map'
TRAINING_SET_DIR = os.path.join(RESOURCE_DIR, 'smaller_train')
TEST_SET_DIR = os.path.join(RESOURCE_DIR, 'smaller_test')
ADAPTED_IMG_DIR = os.path.join(RESOURCE_DIR, "adapted_images")
MODEL_DIR = os.path.join(RESOURCE_DIR, 'saved_model')

MODEL_TREE_FILENAME = 'tree_model.joblib'
IMG_DECISION_TREE = 'decision_tree.png'
DATA_TRAINING_FOR_DECISION_TREE = 'data_training.csv'

# Picture format
PNG = "png"

# File format
JSON = 'json'

# Tractor settings
TRACTOR = 'tractor'

# Types of Fields
SAND = 'sand'
CLAY = 'clay'
GRASS = 'grass'
CORN = 'corn'
SUNFLOWER = 'sunflower'

FIELD_TYPES = (SAND, CLAY, GRASS, CORN, SUNFLOWER)

# Directions
D_NORTH = 0.0
D_EAST = 270.0
D_SOUTH = 180.0
D_WEST = 90.0

# Goal Test
AMOUNT_OF_CROPS = 5

# Movements:
M_GO_FORWARD = "go forward"
M_ROTATE_LEFT = "rotate left"
M_ROTATE_RIGHT = "rotate right"

# Actions:
A_SOW = "sow"
A_HARVEST = "harvest"
A_HYDRATE = "hydrate"
A_FERTILIZE = "fertilize"
A_DO_NOTHING = "do nothing"
TYPES_OF_ACTION = [A_SOW, A_HARVEST, A_HYDRATE, A_FERTILIZE, A_DO_NOTHING]

# Costs fields:
VALUE_OF_CROPS = 0.2
VALUE_OF_PLANT = 0.3
VALUE_OF_SAND = 0.4
VALUE_OF_CLAY = 0.5

# Weather
W_SUNNY = 'Sunny'
W_CLOUDY = 'Cloudy'
W_SNOW = 'Snow'
W_RAINY = 'Rainy'
TYPES_OF_WEATHER = [W_SUNNY, W_CLOUDY, W_SNOW, W_RAINY]

# Seasons
S_AUTUMN = 'Autumn'
S_WINTER = 'Winter'
S_SPRING = 'Spring'
S_SUMMER = 'Summer'

TYPES_OF_SEASON = [S_AUTUMN, S_WINTER, S_SPRING, S_SUMMER]

# Times
TIME_OF_GROWING = 2
TIME_OF_MOVING = 2

# Args
SAVE_MAP = '--save-map'
LOAD_MAP = '--load-map'
AUTO_MODE = '--auto-mode'
