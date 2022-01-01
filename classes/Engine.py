"""
The Engine is the heart of the application. It handles inputs, renders screens
and panels, delegates id3 tag actions to outside modules, etc.
"""

import eyed3
from os import chdir, getcwd, listdir
from os.path import isdir, join

import paneldriver
import panelmaker
from util import Point

from classes.Panel import DummyPanel

class Engine:
    def __init__(self, config, win):
        self.quit = False
        self.config = config
        self.win = win
        (self.height, self.width) = self.win.getmaxyx()
        self.currentPanelIndex = 0
        self.constructPanels()
        eyed3.log.setLevel("ERROR")

    def constructPanels(self):
        dimensions = self.getWindowDimensions()
        self.panels = [
                        panelmaker.make_panel("Previous Directory", dimensions),
                        panelmaker.make_panel("Current Directory", dimensions),
                        panelmaker.make_panel("Tags", dimensions)
                      ]
        self.setCurrentPanel(1)

        self.populateDirectoryPanels()

    def getWindowDimensions(self):
        ul = Point(0, 0)
        lr = Point(self.height, self.width)
        dimensions = (ul, lr)

        return dimensions

    def populateDirectoryPanels(self):
        current_dir = self.listDirectory('.')
        self.panels[1].setItems(current_dir)

        if getcwd() == '/':
            previous_dir = []
        else:
            previous_dir = self.listDirectory('..')
        self.panels[0].setItems(previous_dir)

    def listDirectory(self, dir_path):
        # We only care about mp3 files and directories
        files = [ f for f in listdir(dir_path) if '.mp3' in f or isdir(join(dir_path, f)) ]

        return files

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

    def setCurrentPanel(self, newIndex):
        if newIndex not in range(0, len(self.panels)):
            return
        self.getCurrentPanel().unfocus()
        self.currentPanelIndex = newIndex
        self.getCurrentPanel().focus()

    def handleInput(self, key):
        if key == ord('q'):
            # Exit fantasia
            self.quit = True
        elif key == ord('j'):
            # Move current panel's highlight down 1
            panel = self.getCurrentPanel()
            paneldriver.move_down(panel, 1)
        elif key == ord('k'):
            # Move current panel's highlight up 1
            panel = self.getCurrentPanel()
            paneldriver.move_up(panel, 1)
        elif key == ord('h'):
            if self.currentPanelIndex == 2:
                # If on the tags panel, focus the directory
                self.setCurrentPanel(1)
            elif self.currentPanelIndex == 1:
                # If on the directory panel, go up one level
                chdir('..')
                self.populateDirectoryPanels()
        elif key == ord('l'):
            if self.currentPanelIndex == 1:
                panel = self.getCurrentPanel()
                item = paneldriver.get_selected_item(panel)
                if '.mp3' in item:
                    # If selected item is an mp3 file, display tags
                    tags = self.getTagsFromFile(item)
                    self.panels[2].setItems(tags)
                    self.setCurrentPanel(2)
                elif isdir(join('.', item)):
                    # If selected item is a directory, cd into it
                    chdir(join('.', item))
                    self.populateDirectoryPanels()

    def getTagsFromFile(self, file):
        audiofile = eyed3.load(file)

        tags = [
                f"       TITLE: {audiofile.tag.title}",
                f"      ARTIST: {audiofile.tag.artist}",
                f"       ALBUM: {audiofile.tag.album}",
                f"ALBUM ARTIST: {audiofile.tag.album_artist}",
                f"        YEAR: {audiofile.tag.best_release_date}",
                f"   TRACK NUM: {audiofile.tag.track_num[0]}",
                f"       GENRE: {audiofile.tag.genre}",
                f"    DISC NUM: {audiofile.tag.disc_num[0]}"
               ]

        return tags
