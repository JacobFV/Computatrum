#COPYRIGHT (C) JACOB VALDEZ 2019 ALL RIGHTS RESERVED
#YOU MAY NOT COPY ANY PART OF THIS PROGRAM FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF JACOB VALDEZ
#PLEASE FOREWARD QUERRIES TO jacobfv@msn.com

import numpy as np
import tensorflow as tf

import sys

import pyppeteer
import asyncio
import imageio

from interfaces import Actuator, Sensor
from vision import Lookatable, Translator, Eye

class Keyboard(Actuator):

    def __init__(
        self,
        listener,
        threashold = 0.5,
        keys = ['a', 'b', 'c']
    ):
        self.keys = keys
        self.listener = listener
        self.threashold = threashold

    def d_vec_len(self, new):
        return len(self.keys)

    def execute(self, d):
        d=d.eval()
        keys_down = []
        for d_index, d_val in enumerate(d, start = 0):
            if d_val > self.threashold:
                keys_down.append(self.keys[d_index])
        self.listener.set_keys_down(set(keys_down))

    class Listener:

        def __init__(self):
            self.all_keys_down = []

        #NOTE this method may not be idempotent
        def set_keys_down(self, new_keys: set):
            self.all_keys_down = new_keys
                
    class Stateful_Listener(Listener):

        #NOTE this method may not be idempotent
        def set_keys_down(self, new_keys: set):
            prev_keys = set(self.all_keys_down)
            assert isinstance(new_keys, set)
            self.all_keys_down = prev_keys.union(new_keys)
            self.new_keys_up = prev_keys.difference(new_keys)
            self.new_keys_down = new_keys.difference(prev_keys)
            self.held_keys = prev_keys.intersection(new_keys)

class Mouse(Translator):

    def __init__(
        self,
        listener,
        buttons = ['left', 'right', 'middle'],
        click_threashold = 0.5,
        sensitivity = 1.0,
        max_speed = 5.0
    ):
        self.listener = listener
        self.buttons = buttons
        self.click_threashold = click_threashold
        super.__init__(
            unit_force = sensitivity,
            max_speed = max_speed,
            initial_x = listener.bounds_x() / 2.0,
            initial_y = listener.bounds_y() / 2.0,
            initial_vel_x = 0.0,
            initial_vel_y = 0.0,
            bounds_x = listener.bounds_x(),
            bounds_y = listener.bounds_y()
        )

    #N, E, S, W + number of buttons (prob. 3, total: 7)
    def d_vec_len(self, new):
        return 4 + len(self.buttons) 

    def execute(self, d):
        d=d.eval()
        self.move(
            dx = d[0] - d[2], #N - S
            dy = d[1] - d[3]  #E - W
        )

        buttons_down = []
        for button_index, button_name in enumerate(self.buttons, start = 0):
            if d[4 + button_index] > self.click_threashold:
                buttons_down.append(button_name)
        self.listener.set_buttons_down(set(buttons_down))

    def apply_motion(self):
        self.listener.move_to_point()

    # NOTE COMPUTERS: CALL THIS FUNCTION
    # Some uses of the mouse may require the Listener
    # to correct_position(x, y) like a computer application
    # that occasionally moves the cursor where it wants to
    # move the cursor. correct_position(x, y) makes the needed
    # changes and slows down the velocity proportional to the
    # deviation in position
    # NOTE pypeteer will not need to use this function
    def correct_position(self, x, y):
        self.vel_x = self.vel_x * min([1.0, 1.0 / abs(self.x - x)])
        self.x = x

        self.vel_y = self.vel_y * min([1.0, 1.0 / abs(self.y - y)])
        self.y = y

    class Listener:

        def __init__(self):
            self.all_buttons_down = set()

        #NOTE this method may not be idempotent
        def set_buttons_down(self, new_buttons: set):
            self.all_buttons_down = new_buttons

        #NOTE this method may not be idempotent
        def move_to_point(self, x, y):
            raise NotImplementedError

        #these methods are idempotent
        def bounds_x(self): raise NotImplementedError
        def bounds_y(self): raise NotImplementedError
        
    class Stateful_Listener(Listener):

        def __init__(self):
            self.new_buttons_down = set()
            self.new_buttons_up = set()
            self.held_buttons = set()
            self.x, self.y = 0.0, 0.0
            super.__init__()

        def move_to_point(self, x, y):
            self.x, self.y = x, y

        #NOTE this method may not be idempotent
        def set_buttons_down(self, new_buttons: set):
            prev_buttons = self.all_buttons_down
            assert isinstance(prev_buttons, set)
            assert isinstance(new_buttons, set)
            self.all_buttons_down = new_buttons
            self.new_buttons_down = new_buttons - prev_buttons
            self.new_buttons_up = prev_buttons - new_buttons
            self.held_buttons = new_buttons.intersection(prev_buttons)

class Display(Lookatable):

    def __init__(self, resolution):
        self.resolution = resolution
        self.data = np.zeros(self.resolution)

    def matrix(self) -> np.ndarray:
        return self.data


class Computer:

    def __init__(self, name: str):
        self.name = name

    def tick(self): raise NotImplementedError

class Pyppeteer_Browser(
    Keyboard.Stateful_Listener,
    Mouse.Stateful_Listener,
    Computer
):

    def __init__(
        self,
        resolution = (800, 600),
        homepage = 'https://jacobfv.github.io/',
        unique_id = str(np.random.randint(0, 100000000))
    ):
        self.unique_id = unique_id
        self.dislay = Display(resolution)
        async def setup_pyppeteer(homepage):
            self.browser: pyppeteer.browser.Browser = await pyppeteer.launch()
            self.page = await self.browser.newPage()
            self.page.setViewport({
                'width': self.dislay.data.shape[0],
                'height': self.dislay.data.shape[1]
            })
            await self.page.goto(homepage)
        asyncio.get_event_loop().run_until_complete(
            setup_pyppeteer(homepage)
        )
        super(Keyboard.Stateful_Listener, self).__init__()
        super(Mouse.Stateful_Listener, self).__init__()

    def bounds_x(self):
        return self.dislay.data.shape[0]

    def bounds_y(self):
        return self.dislay.data.shape[0]

    def screenshot_location(self):
        return f'pyppeteer_screenshot_{self.unique_id}'

    def tick(self):
        #perform pyppeteer browser logic
        async def pyppeteer_logic():
            #dispatch appropriate keydown events
            for key in self.new_keys_down:
                await self.page.keyboard.down(key)
            #dispatch appropriate keyup events
            for key in self.new_keys_up:
                await self.page.keyboard.up(key)
            #dispatch appropriate mousebutton down events
            for button in self.new_buttons_down:
                await self.page.mouse.down({'button': button})
            #dispatch appropriate mousebutton up events
            for button in self.new_buttons_up:
                await self.page.mouse.up({'button': button})
            #move cursor
            await self.page.mouse.move(
                x = self.x, 
                y = self.y,
                options = {'steps': 4}
            )
            #take screenshot
            #NOTE 'fullPage' may be capturing a squashed page
            # will need to test this to make sure long wikipedia
            # articles aren't just squashed into a 800x600 space
            # may need to add 'wheelup' and 'wheeldown' buttons
            # to mouse and handle them here to make my own scrolled
            # space
            await self.page.screenshot({
                'path': self.screenshot_location,
                'fullPage': True 
            })
            self.dislay.data = imageio.imread(self.screenshot_location)
        asyncio.get_event_loop().run_until_complete(pyppeteer_logic())

    @staticmethod
    def all_keys():
        #these are the keys that pyppeteer understands
        return """

        Escape   F1  F2  F3  F4  F5  F6  F7  F8  F9  F10  F11  F12             Delete
        Backquote 1   2    3    4   5   6    7    8    9    0  Minus Equals Backspace
        Tab     KeyQ KeyW KeyE KeyR KeyT KeyY KeyU KeyI KeyO KeyP BracketLeft BracketRight Backslash
        CapsLock KeyA KeyS KeyD KeyF KeyG KeyH KeyJ KeyK KeyL Semicolon Quote  Enter
        ShiftLeft KeyZ KeyX KeyC KeyV KeyB KeyN KeyM  Coma  Period Slash  ShiftRight
        ControlLeft AltLeft          Space       AltRight  ControlRight  ContextMenu
        
              PageUp                       ArrowUp
        Home PageDown End       ArrowLeft ArrowDown ArrowRight

        """.split()

    @staticmethod
    def all_buttons():
        return ['left', 'right', 'middle']

    @staticmethod
    def Create(
        resolution = (800, 600),
        homepage = 'https://jacobfv.github.io/'
    ):
        #make computer
        pyppeteer_browser = Pyppeteer_Browser(
            resolution = resolution,
            homepage = homepage
        )
        #make keyboard with all keys
        keyboard = Keyboard(
            listener = pyppeteer_browser,
            keys = Pyppeteer_Browser.all_keys()
        )
        #make mouse with all buttons
        mouse = Mouse(
            listener = pyppeteer_browser,
            buttons = Pyppeteer_Browser.all_buttons()
        )
        #return computer, keyboard, mouse, & computer's screen
        return pyppeteer_browser, keyboard, mouse, pyppeteer_browser.dislay

class Console_Interface(
    Keyboard.Stateful_Listener,
    Computer
):

    def __init__(self, keys: list, buffer_size = 64):
        self.keys = keys
        self.buffer_size = buffer_size
        self.buffer = ''
        self.display = Display((buffer_size, len(keys)))
        super(Keyboard.Stateful_Listener, self).__init__()

    def get_buffer(self) -> str:
        return self.buffer

    def write_to_buffer(self, text):
        #write all chars in new_keys_down to buffer
        #trimming off older chars
        self.buffer = text[-self.buffer_size:]
        #write buffer to display
        for index, char in enumerate(self.buffer, start = 0):
            self.display.data[index,:] = np.array([
                1.0 if key is char else 0.0 for key in self.keys
            ])

    def tick(self):
        self.write_to_buffer(
            self.buffer + ''.join(list(self.all_keys_down))
        )

    @staticmethod 
    def all_keys():
        #these are the keys I will use with sys.stdio
        #anything on my laptop's central keyboard is fair
        #perhaps, this may be termed the 60% keyboard keys
        return """
                ` 1 2 3 4 5 6 7 8 9 0 - =
                   q w e r t y u i o p [ ] \\
                   a s d f g h j k l ; \'
                   z x c v b n m , . /

                ~ ! @ # $ % ^ & * ( ) _ +
                                    { } |
                                    : \"
                                    < > ?
                """.split() + [' ', '\t', '\n', '\r']

    @staticmethod
    def Create(buffer_size = 64 * 64, keys = None):
        if keys is None:
            keys = Console_Interface.all_keys()
        #make computer with all_keys
        console = Console_Interface(keys = keys)
        #make keyboard with all_keys
        keyboard = Keyboard(listener = console, keys = keys)
        eye = Eye(
            lookatable = console.display,
            viewport_size_x = 2,
            viewport_size_y = len(console.keys),
            unit_force = 1.0,
            max_speed = 2.0
        )
        #return computer, keyboard, computer's display, & eye on display
        return console, keyboard, console.display, eye
    
class Blender_Workstation(
    Keyboard.Stateful_Listener,
    Mouse.Stateful_Listener,
    Computer
):
    
    def __init__(self):
        print('this must be executed on python 3.6.7')
        import bpy
        raise NotImplementedError