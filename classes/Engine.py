"""
The Engine is the heart of the application. It handles inputs, renders screens
and panels, delegates id3 tag actions to outside modules, etc.
"""

from util import Point

from classes.Panel import DummyPanel

class Engine:
    def __init__(self, config, win):
        self.quit = False
        self.config = config
        self.win = win
        (self.height, self.width) = self.win.getmaxyx()
        self.constructPanels()

    def constructPanels(self):
        dimensions = self.getWindowDimensions()
        test_panel = DummyPanel(dimensions, "Test Panel")

        self.panels = [ test_panel ]
        self.currentPanelIndex = 0

    def getWindowDimensions(self):
        ul = Point(0, 0)
        lr = Point(self.height, self.width)
        dimensions = (ul, lr)

        return dimensions

    def run(self):
        while(not self.quit):
            self.renderAll()
            key = self.getInput()
            self.handleInput(key)

    def renderAll(self):
        for panel in self.panels:
            panel.render()

    def getInput(self):
        current_panel = self.getCurrentPanel()
        key = current_panel.win.getch()
        return key

    def getCurrentPanel(self):
        return self.panels[self.currentPanelIndex]

    def handleInput(self, key):
        if key == ord('q'):
            self.quit = True
