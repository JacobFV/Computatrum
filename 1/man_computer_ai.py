from Dream.dream import Dream
from Dream.Interface import core, eye, interface, computer

random = core.Random()
punisher = core.Punishment()
minimizer = core.Minimizer()
predictor_fitter = core.Fit_Predictor()

persistant_thoughts = core.SimpleRecurrentData(100)

#senses and actuators
mouse = computer.Mouse()
keyboard = computer.Keyboard(computer.Browser.all_keys())
display = computer.Display((800, 600))
eye1 = eye.VirtualEye(display.data, focus_size=(10, 10), sensitivity=2.5)
eye2 = eye.VirtualEye(display.data, focus_size=(10, 10), sensitivity=2.5)
browser = computer.Browser(mouse=mouse, keyboard=keyboard, display=display)
browser.load("https://jacobfv.github.io/")

stdio_keyboard = computer.Keyboard(computer.StdioUserInterface.all_keys())
stdio_display = computer.Display((128, len(computer.StdioUserInterface.all_keys())))
stdio_reader = eye.VirtualEye(stdio_display.data, focus_size=(1, 64), sensitivity=1)
stdio_interface = computer.StdioUserInterface(
        keyboard = stdio_keyboard,
        mouse = computer.Mouse(),
        display = stdio_display
    )

layers = [
        1000, 900, 800, 700, 600, 500, 500, 600, 700, 800, 900, 1000
    ]
dream = Dream(
    decider_layer_sizes=layers,
    predictor_layer_sizes=layers,
    interfaces=[
        random, punisher, minimizer, predictor_fitter,
        persistant_thoughts,
        mouse, keyboard, eye1, eye2,
        stdio_keyboard, stdio_reader
        ])

#round 1 may not have a file to load from
BASE_PATH = "C:\\Users\\Jacob\\path to folder\\dream\\"
LTM_PATH = BASE_PATH + "dream0.ltm"
STM_PATH = BASE_PATH + "dream0.stm"
try: 
    dream.load_LTM(LTM_PATH) 
    dream.load_STM(STM_PATH)
except:
    pass

for i in range(1e2):
    stdio_interface.process() #print user output, request input, and draw to display
    dream.think() #think
    browser.process() #do rendering

    #if I had a GUI,
        #now would be the time to
        #present and image of the current eyes' views
        #and what the browser is displaying
        #and thoughts are thinking

try: 
    dream.save_LTM(LTM_PATH)
    dream.save_STM(STM_PATH)
except:
    print("error saving")