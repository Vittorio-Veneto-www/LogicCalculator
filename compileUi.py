from PyQt5 import uic
from os.path import dirname, join
current_dir = dirname(__file__)

with open(join(current_dir, './gui.py'), 'w', encoding='utf-8') as f:
    uic.compileUi(join(current_dir, './gui.ui'), f)