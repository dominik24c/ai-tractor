## Tractor
### 1. Requirements
python version 3.9 or higher
```bash
python3 --version
```
### 2. Create virtual environments and install libs
```bash
virtualenv venv
source activate
pip3 install -r requirements.txt
```
#### 2.1 Graphviz
For ubuntu, we probably need to download graphviz library by apt-get
```bash
sudo apt-get install graphviz
```

### 3. Run application
```bash
python3 main.py
```

### 4. Arguments
Maps are saved in maps directory with json format.\
It's two dimensional array of types of fields. \
Example: 
```json
[
  ["Corn", "Sunflower","Clay"],
  ["Clay", "Soil","Clay"],
  ["Sunflower", "Soil","Corn"]
]
```
Warning!
Map must the same sizes what loaded map!\
Change sizes map in config.py
```python
# Board settings:
VERTICAL_NUM_OF_FIELDS = 3
HORIZONTAL_NUM_OF_FIELDS = 3
```

#### 4.1 Save generated map:
```bash
python3 main.py --save-map
```
Map will be saved in maps directory. 
Generated filename: map-uuid

#### 4.2 Load map
```bash
python3 main.py --load-map=name_of_map
```
Map must be in the maps directory with json extension.

#### 4.3 Auto mode
Tractor will make own decisions such as harvesting, hydrating and so on using a decision tree.
It also will be moving by a star algorithm and it will be checking fields using a neural network during harvesting crops.
```bash
python3 main.py --auto-mode
```