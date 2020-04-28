import sys
import random
import asyncio
import imageio
import pyppeteer
import numpy as np
from enum import Enum
from eye import Translator
from interface import Sense, Actuator


class Mouse(Translator):

    #class Buttons(Enum):
        #Left = 0
        #Right = 1
        #Middle = 2

    #class Listener:
        #def mouse_button(self, button, state): pass
        #def mouse_move(self, delta): pass
        #def wheel_rot(self, rot): pass

    def __init__(self, click_threshold=0.75, wheel_sensitivity=1.0, **kwargs):
        super.__init__(**kwargs)
        self.click_threshold = click_threshold
        self.wheel_sensitivity = wheel_sensitivity
        self._zero_internal_state()

    def do(self, action):
        self._zero_internal_state()
        self.deltify(action[:4])
        if action[4] > self.click_threashold: self.lmb = true
        if action[5] > self.click_threashold: self.rmb = true
        if action[6] > self.click_threashold: self.mmb = true
        self.drot = self.wheel_sensitivity * (action[7] - action[8])

    def apply_delta(self, delta):
        self.dloc = delta

    def get_delta(self):
        return self.dloc

    def get_drot(self):
        return self.drot

    def get_buttons(self):
        return {'left': self.lmb, 'right': self.rmb, 'middle': self.mmb}
        
    def _zero_internal_state(self):
        self.lmb, self.rmb, self.mmb = 3 * [False]
        self.dloc = [0,0]
        self.drot = 0

    def action_vec_length(self): return 9
        #NESW, lmb, rmb, mmb, wheel up, wheel down


class Keyboard(Actuator):
    #class Listener:
        #active_keys: set of chars for pressed keys
        #def set_active_keys(self, active_keys): pass
            
    def __init__(self, keys, keypress_threashold=0.75):
        self.keys = keys
        self.threashold = keypress_threashold
        self.key_states = {}
        for key in keys:
            self.key_states[key] = False

    def do(self, action):
        for vec, key_val in zip(action, self.keys):
            if vec > self.threashold: 
                self.key_states[key_val] = True
            else:
                self.key_states[key_val] = False

    def action_vec_length(self): return len(self.keys)

    def get_keys_down(self):
        """
            returns a dictionary containing the key_names
            and a bool for down (true) or up (false)
        """
        return self.key_states

    #old key coding ideas
        depricated_key_codes = [
            ('a','A')
            ('b','B')
            ('c','C'),
            ('d','D'),
            ('e','E'),
            ('f','F'),
            ('g','G'),
            ('h','H'),
            ('i','I'),
            ('j','J'),
            ('k','K'),
            ('l','L'),
            ('m','M'),
            ('n','N'),
            ('o','O'),
            ('p','P'),
            ('q','Q'),
            ('r','R'),
            ('s','S'),
            ('t','T'),
            ('u','U'),
            ('v','V'),
            ('w','W'),
            ('x','X'),
            ('y','Y'),
            ('z','Z'),

            (' ',' '),

            (',','<'),
            ('.','>'),
            ('/','?'),
            (';',':'),
            ('\'','"'),
            ('[','{'),
            (']','}'),
            ('\\','|'),
            ('-','_'),
            ('=','+'),
            ('`','~'),

            ('1','!'),
            ('2','@'),
            ('3','#'),
            ('4','$'),
            ('5','%'),
            ('6','^'),
            ('7','&'),
            ('8','*'),
            ('9','('),
            ('0',')'),

            ('UP'),
            ('DOWN'),
            ('LEFT'),
            ('RIGHT'),
            ('ENTER'),
            ('SHIFT'),
            ('BACKSPACE')
        ]
        #condensed output : ascii keycode
        key_map = {
            0:65, #A
            1:66, #B
            2:67, #C...
            3:68,
            4:69,
            5:70,
            6:71,
            7:72,
            8:73,
            9:74,
            10:75,
            11:76,
            12:77,
            13:78,
            14:79,
            15:80,
            16:81,
            17:82,
            18:83,
            19:84,
            20:85,
            21:86,
            22:87,
            23:88, #...X
            24:89, #Y
            25:90, #Z

            26:32, #SPACE

            27:48, #0
            28:49, #1..
            29:50,
            30:51,
            31:52,
            32:53,
            33:54,
            34:55,
            35:56, #..8
            36:57, #9

            37:188, #,
            38:190, #.
            39:191, #/
            40:186, ##;
            41:222, #'
            42:219, #[
            43:221, #]
            44:220, #\
            45:189, ##-
            46:187, ##=
            47:192, #`

            48:0,
            49:0,
            50:0,
            51:0,
            52:0,
            53:0,
            54:0,
            55:0,

            56:8, #BKSPC
            57:9, #TAB
            58:13, #ENTER
            59:16, #SHIFT
            60:17, #CTLR
            61:18, #ALT
            62:20, #CPSLOCK
            63:27, #ESC
            64:33, #PG UP
            65:34, #PG DOWN
            66:35, #END
            67:36, #HOME
            68:37, #AR LEFT
            69:38, #AR UP
            70:39, #AR RIGHT
            71:40, #AR DOWN
            72:45, #INSERT
            73:46, #DELETE

            74:112, #F1
            75:113, #F2..
            76:114,
            77:115,
            78:116,
            79:117,
            80:118,
            81:119,
            82:120,
            83:121,
            84:122, #..F11
            85:123, #F12
        }
        #while I can use puppeteeter.lib.USKeyboardLayout to rev. lookup
        # a dictionary of K:V pairs of the form:
        # 'KeyA' : {'keyCode':65,'code':'KeyA','shiftKey':'A','key':'a'}
        #pyppeteer does not contain a lib dir
        #so this map should have everything I need     
        examplekey={0: {'ascii': 65, 'pypp': 'KeyA'}}
        big_fat_key_map = {
            (1,66,'KeyB'),
            (2,67,'KeyC'),
            (3,68,'KeyD'),
            (4,69,'KeyE'),
            (5,70,'KeyF'),
            (6,71,'KeyG'),
            (7,72,'KeyH'),
            (8,73,'KeyI'),
            (9,74,'KeyJ'),
            (10,75,'KeyK'),
            (11,76,'KeyL'),
            (12,77,'KeyM'),
            (13,78,'KeyN'),
            (14,79,'KeyO'),
            (15,80,'KeyP'),
            (16,81,'KeyQ'),
            (17,82,'KeyR'),
            (18,83,'KeyS'),
            (19,84,'KeyT'),
            (20,85,'KeyU'),
            (21,86,'KeyV'),
            (22,87,'KeyW'),
            (23,88,'KeyX'),
            (24,89,'KeyY'),
            (25,90,'KeyZ'),

            (26,32,'Space'),

            (27,48,'0'),
            (28,49,'1'),
            (29,50,'2'),
            (30,51,'3'),
            (31,52,'4'),
            (32,53,'5'),
            (33,54,'6'),
            (34,55,'7'),
            (35,56,'8'),
            (36,57,'9'),
            27:48, #0
            28:49, #1..
            29:50,
            30:51,
            31:52,
            32:53,
            33:54,
            34:55,
            35:56, #..8
            36:57, #9

            37:188, #,
            38:190, #.
            39:191, #/
            40:186, ##;
            41:222, #'
            42:219, #[
            43:221, #]
            44:220, #\
            45:189, ##-
            46:187, ##=
            47:192, #`

            48:0,
            49:0,
            50:0,
            51:0,
            52:0,
            53:0,
            54:0,
            55:0,

            56:8, #BKSPC
            57:9, #TAB
            58:13, #ENTER
            59:16, #SHIFT
            60:17, #CTLR
            61:18, #ALT
            62:20, #CPSLOCK
            63:27, #ESC
            64:33, #PG UP
            65:34, #PG DOWN
            66:35, #END
            67:36, #HOME
            68:37, #AR LEFT
            69:38, #AR UP
            70:39, #AR RIGHT
            71:40, #AR DOWN
            72:45, #INSERT
            73:46, #DELETE

            74:112, #F1
            75:113, #F2..
            76:114,
            77:115,
            78:116,
            79:117,
            80:118,
            81:119,
            82:120,
            83:121,
            84:122, #..F11
            85:123, #F12
        }


class Data_Matrix:

    def __init__(self, size):
        self.size = size
        self.data = np.zeros(size)

    def get_size(self): return self.size

    def set_data(self, data): self.data = data

    def set_val(self, loc, val): self.data[loc] = val
    def get_val(self, loc): return self.data[loc]


class Display(Data_Matrix):
    def set_pixel(self, coordinates, color): self.set_val(coordinates, color)
    def read_pixel(self, coordinates): return self.get_val(coordinates)

    #for programatic and possibly user (not DREAM) interface
    #draws in very smallest font readable
    #def write_text(self, text, loc):
    #    raise NotImplementedError()


class Computer():

    def __init__(self, keyboard, display, mouse):
        self.keyboard = keyboard
        self.display = display
        self.mouse = mouse

        self.state_transitions = {
                [False, False]: "neither",
                [False, True]: "down",
                [True, False]: "up",
                [True, True]: "neither",
            } 

        self.keys_states = keyboard.get_keys_down() #fill it with falses
        self.key_transitions = {}

        self.mouse_button_states = {'left': None, 'right': None, 'middle': None}
        self.mouse_button_transitions = {'left': None, 'right': None, 'middle': None}
        self.mouse_dloc = (0.0, 0.0)
        self.mouse_drot = 0.0

    def process(self): 
        self._process_keys()
        self._process_mouse()
        self._computer_logic()
    
    def _computer_logic(self): pass
    
    def _process_keys(self):
        new_keys = self.keyboard.get_keys_down()
        for key_name, new_key_val in new_keys
            self.key_transitions[key_name] = self.state_transitions[[
                    self.key_states[key_name], new_key_val
                ]]
        self.key_states = new_keys

    def _process_mouse(self):
        new_button_states = self.mouse.get_buttons()
        for button_name in self.mouse_button_states:
            self.mouse_button_transitions[button_name] = 
                self.state_transitions[[
                        self.mouse_button_states[button_name],
                        new_button_states[button_name]
                    ]]
        self.mouse_button_states = new_button_states

        self.mouse_dloc = self.mouse.get_delta()
        self.cursor[0] += self.mouse_dloc[0]
        self.cursor[1] += self.mouse_dloc[1]

        self.mouse_drot = self.mouse.get_drot()

    @staticmethod
    def create_and_connect_standard_peripherals(computer, resolution):
        raise NotImplementedError()
        #returns a connected mouse, keyboard, and display at resolution


class StdioUserInterface(Computer):

    def __init__(self, display, *other_peripherals):
        super.__init__()
        self.chars = []
        self.display = display
        self.connect_peripherals(display + other_peripherals)

    @staticmethod
    def all_keys():
        #these are the keys I will use with stdio
        #anything on my laptop's central keyboard is fair
        return """
                ` 1 2 3 4 5 6 7 8 9 0 - =
                   q w e r t y u i o p [ ] \\
                   a s d f g h j k l ; \'
                   z x c v b n m , . /

                ~ ! @ # $ % ^ & * ( ) _ +
                                    { } |
                                    : \"
                                    < > ?
                """.split() 
                + ' '
                + '\t'
                + '\n' 
                + '\r'
    
    def _computer_logic(self):
        self.process_keys()
        print("output:")
        #since this approach only allows
        # one ordered key at a time,
        # I should seriously get a second console
        # to display the output vs. input on main console
        for key in key_queue:
            sys.stdout.write(chr(key))
        
        message = input("message")
        if message != "":
        for i in range(len(message)):
            self.display[i] = onehot(intfromchar(inpt[i]))

            #this approach clips off overflowing chars
            #but that is okay since only programmers user this


class Browser(Computer):
    
    def __init__(self, homepage, *kwargs):
        super.__init__(kwargs)
        self.cursor = (0,0)
        self.uid = random.randint(1000000, 9999999)
        asyncio.get_event_loop()
            .run_until_complete(
                self._start(homepage)
            )

    async def _start(self, homepage="https://jacobfv.github.io/"):
        self.browser = await pyppeteer.launch()
        self.page = await browser.newPage()
        self.page.setViewport({
                width: self.display.get_size()[0],
                heigth: self.display.get_size()[1],
                deviceScaleFactor: 1
            })
        await self.page.goto(homepage)

    def __del__(self):
        asyncio.get_event_loop()
            .run_until_complete(
                self.browser.close()
            )

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
        
    def _computer_logic(self):
        asyncio.get_event_loop()
            .run_until_complete(
                self._async_computer_logic()
            )

    async def _async_computer_logic(self):
        #log keyup/keydown events to the browser
        for key_name, key_val in self.key_transitions:
            eval("self.page.keyboard.{0}({1})".format(key_val, key_name))

        #dispatch mouse button events
        for button_name, button_state in self.mouse_transitions:
            eval("self.page.mouse.{0}(button={1})".format(button_state, button_name))
        
        #move mouse cursor
        await self.page.mouse.move_to(
            x = self.cursor[0],
            y = self.cursor[1],
            steps = 4
            )

        #draw browser screenshot to display
        await self.page.screenshot({
            'path': 'browserpage{0}.png'.format(self.uid),
            'fullPage': True
            })
        screenshot = imageio.imread('browserpage{0}.png'.format(self.uid))
        self.display.set_data(screenshot)


class Linux_Container(Computer):
    pass