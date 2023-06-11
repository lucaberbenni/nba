import os
import pandas as pd

from bs4 import BeautifulSoup

SCORE_DIR = 'data/scores'
box_scores = os.listdir(SCORE_DIR)
box_scores = [os.path.join(SCORE_DIR, f) for f in box_scores if f.endswith('.html')]
print(box_scores)