from UI.login import Login
from PIL import Image, ImageTk
import os

rootDir = ""
if __name__ == "__main__":
    rootDir = os.path.dirname(os.path.abspath(__file__))
    app = Login(rootDir)
    app.mainloop()