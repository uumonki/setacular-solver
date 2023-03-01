from selenium import webdriver
from selenium.webdriver.common.by import By
from itertools import combinations
import time

def find_count(tile): # find the count
    shapes_classes = tile.get_attribute("class").split(" ")
    if "three" in shapes_classes:
        count = 3
    elif "two" in shapes_classes:
        count = 2
    else:
        count = 1
    return count

def find_shape(tile): # find the shape: circle, rect, or path
    if len(tile.find_elements(By.TAG_NAME, "circle")) > 0:
        shape = 1
    elif len(tile.find_elements(By.TAG_NAME, "rect")) > 0:
        shape = 2
    else:
        shape = 3
    return shape

def find_color(tile): # find the color
    indicator = tile.find_element(By.XPATH, "./following-sibling::div")
    indicator_classes = indicator.get_attribute("class").split(" ")
    if "red" in indicator_classes:
        color = 1
    elif "blue" in indicator_classes:
        color = 2
    else:
        color = 3
    return color

def find_fill(tile): # find the fill
    shape_classes = tile.find_element(By.CLASS_NAME, "shape").get_attribute("class").split(" ")
    if "full" in shape_classes:
        fill = 3
    elif "half" in shape_classes:
        fill = 2
    else:
        fill = 1
    return fill

def is_set(patterns): # check if the set is valid
    for i in range(4):
        s = set([patterns[0][i], patterns[1][i], patterns[2][i]])
        if len(s) == 1 or len(s) == 3:
            continue
        else:
            return False
    return True

def solve(patterns): # solve the set
    # patterns is a list of tuples (count, shape, color, fill)
    # return a list of the indices of the set
    # all tuple elements must either all be the same or all be different
    # if there is no set, return an empty list
    for c in combinations(patterns, 3):
        # this is inefficient but 9C3 is only 84
        if is_set(c):
            return [patterns.index(i) for i in c]
    return []

b = webdriver.Chrome("./chromedriver")
url = input("Enter the URL: ")

# https://set.loud.red/multiplayer/tyanhj
b.get(url)
began = False
while not began: # wait for page to load
    try:
        alert = b.switch_to.alert
        alert.send_keys(input("Enter your name: "))
        alert.accept()
    except:
        try:
            b.find_element(By.CLASS_NAME, "grid")
            began = True
        except:
            time.sleep(0.1)

grids = b.find_elements(By.CLASS_NAME, "grid")
while grids != []: # while the game is still going
    grid = grids[0]
    tiles = grid.find_elements(By.CLASS_NAME, "shapes")
    patterns = [] # list of tuples (count, shape, color, fill)
    for tile in tiles:
        count = find_count(tile)
        shape = find_shape(tile)
        color = find_color(tile)
        fill = find_fill(tile)
        patterns.append((count, shape, color, fill))
    solution = solve(patterns)
    for i in solution:
        tiles[i].click()
        time.sleep(0.1)
    time.sleep(2)
    grids = b.find_elements(By.CLASS_NAME, "grid")





        
