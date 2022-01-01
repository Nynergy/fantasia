"""
This is where we keep all our Panel classes/subclasses.
"""

import curses
import unicodedata

import draw
from util import Point, get_color_pair

"""
A Panel is a container for an arbitrary set of information. Since this will
serve as the "abstract" baseclass, it has no idea how to render itself, though
it does have some basic draw functions that subclasses will call on if they
don't implement their own.
"""

class Panel:
    def __init__(self, panel_dimensions, title=""):
        self.constructPanelWindow(panel_dimensions)
        self.title = title

    def constructPanelWindow(self, panel_dimensions):
        (ul, lr) = panel_dimensions
        self.y = ul.y
        self.x = ul.x
        self.width = lr.x - ul.x
        self.height = lr.y - ul.y
        self.win = curses.newwin(self.height, self.width, self.y, self.x)

    def clearScreen(self):
        # Fill each cell with the empty character
        for i in range(self.height - 1):
            for j in range(self.width):
                p = Point(i, j)
                draw.char(p, " ", self.win)

    def drawTitleLine(self):
        ul = Point(0, 0)
        lr = Point(0, self.width - 1)
        self.drawTeeLine(ul, lr)

    def drawBottomLine(self):
        ul = Point(self.height - 2, 0)
        lr = Point(self.height - 2, self.width - 1)
        self.drawTeeLine(ul, lr)

    def drawTeeLine(self, left, right):
        # Horizontal line with tees on the ends
        self.win.attron(curses.A_ALTCHARSET)
        draw.h_line(left, right, curses.ACS_HLINE, self.win)
        draw.char(left, curses.ACS_LTEE, self.win)
        draw.char(right, curses.ACS_RTEE, self.win)
        self.win.attroff(curses.A_ALTCHARSET)

    def drawTitle(self):
        title_x = (self.width // 2) - (len(self.title) // 2)

        # First blank the area around the title
        ul = Point(0, title_x - 1)
        lr = Point(0, title_x + len(self.title))
        draw.h_line(ul, lr, " ", self.win)

        # Then draw the title string itself
        self.win.attron(curses.A_BOLD)
        draw.string(Point(0, title_x), self.title, self.win)
        self.win.attroff(curses.A_BOLD)

    def resize(self, new_dimensions):
        self.constructPanelWindow(new_dimensions)

"""
A DummyPanel is a test panel that just renders a basic Panel with no data.
"""

class DummyPanel(Panel):
    def __init__(self, panel_dimensions, title=""):
        super().__init__(panel_dimensions, title)

    def render(self):
        self.clearScreen()
        self.drawTitleLine()
        self.drawTitle()
        self.drawBottomLine()
        self.win.refresh()

"""
A ListPanel is a panel that specifically contains some list of information, and
will display/interact with that list via the user's commands.
"""

class ListPanel(Panel):
    def __init__(self, panel_dimensions, title=""):
        super().__init__(panel_dimensions, title)
        self.items = []
        self.f_item = 0
        self.l_item = min(len(self.items), self.height - 1)
        self.curr_item = 0
        self.focused = False

    def render(self):
        self.clearScreen()
        self.drawTitleLine()
        self.drawTitle()
        self.drawItems()
        self.clearSides()
        self.drawIndicators()
        self.drawBottomLine()
        self.win.refresh()

    def drawItems(self):
        # Translate any non-strings into strings
        strings = []
        for item in self.items:
            if not isinstance(item, str):
                strings.append(repr(item))
            else:
                strings.append(item)

        # Draw items within moving frame
        attr = 0
        counter = 0
        bound = min(self.l_item, len(self.items))
        for i in range(self.f_item, bound):
            # Specify applicable attributes
            if(counter + self.f_item == self.curr_item):
                attr = (attr | curses.A_REVERSE)
                if self.focused:
                    attr = (attr | get_color_pair("Accent"))
            item = strings[i][:self.width - 2] # Truncate strings longer than panel width
            fill_spaces = (self.width - calc_string_width(item)) - 2
            itemline = str(item) + (" " * fill_spaces)
            item_point = Point(counter + 1, 1)
            self.win.attron(attr)
            draw.string(item_point, itemline, self.win)
            self.win.attroff(attr)
            counter += 1
            attr = 0

    def drawIndicators(self):
        if(self.f_item > 0):
            self.drawUpperIndicators()

        if(self.l_item < len(self.items)):
            self.drawLowerIndicators()

    def drawUpperIndicators(self):
        left = Point(1, 0)
        right = Point(1, self.width - 1)

        self.win.attron(curses.A_ALTCHARSET)
        draw.char(left, curses.ACS_UARROW, self.win)
        draw.char(right, curses.ACS_UARROW, self.win)
        self.win.attroff(curses.A_ALTCHARSET)

    def drawLowerIndicators(self):
        left = Point(self.height - 3, 0)
        right = Point(self.height - 3, self.width - 1)

        self.win.attron(curses.A_ALTCHARSET)
        draw.char(left, curses.ACS_DARROW, self.win)
        draw.char(right, curses.ACS_DARROW, self.win)
        self.win.attroff(curses.A_ALTCHARSET)

    def clearSides(self):
        # Clear any mis-rendered item artifacts off the sides of the panel
        left_ul = Point(1, 0)
        left_lr = Point(self.height - 3, 0)
        draw.v_line(left_ul, left_lr, ' ', self.win)

        right_ul = Point(1, self.width - 1)
        right_lr = Point(self.height - 3, self.width - 1)
        draw.v_line(right_ul, right_lr, ' ', self.win)

    def getCurrentItemIndex(self):
        return self.curr_item

    def getCurrentItem(self):
        return self.items[self.curr_item]

    def setItems(self, new_items):
        self.items = new_items
        self.resetMovingFrame()

    def addItem(self, item):
        self.items.append(item)
        self.resetMovingFrame()

    def clearItems(self):
        self.items = []
        self.resetMovingFrame()

    def resize(self, new_dimensions):
        self.constructPanelWindow(new_dimensions)
        self.resetMovingFrame()

    def resetMovingFrame(self):
        self.curr_item = min(self.curr_item, self.height - 3, max(0, len(self.items) - 1))
        if len(self.items) < self.height - 1:
            self.f_item = 0
        self.l_item = min(len(self.items), self.f_item + (self.height - 3))

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False

def calc_string_width(text):
    fake_length = len(text.replace(u'’', u"'").encode('utf-8'))
    num_wide = sum(unicodedata.east_asian_width(c) in 'WF' for c in text)
    return fake_length - num_wide
