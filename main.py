from UI.login import Login
from PIL import Image, ImageTk
import os

rootDir = ""
if __name__ == "__main__":
    rootDir = os.path.dirname(os.path.abspath(__file__))
    app = Login(rootDir)
    im = Image.open(f'{rootDir}/img/lock.png')
    photo = ImageTk.PhotoImage(im)
    app.wm_iconphoto(True, photo)
    app.mainloop()