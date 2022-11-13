print("BOOT: code.py")

from app import Manager
from app.themes.strobe import StrobeTheme

manager = Manager(theme=StrobeTheme)
manager.run()
