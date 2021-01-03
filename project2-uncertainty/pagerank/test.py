import os
import random
import re
import sys
from pagerank import *
DAMPING = 0.85
SAMPLES = 10000
corpus = crawl('corpus0')
print(transition_model(corpus,'1.html',DAMPING))