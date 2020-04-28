#just a sinlge file with a top-level function like:
def intelligenceAndBodyParts(base_path, endpoint)
    mouse_eye = MouseEye.Load(path=base_path+'mouse_eye.json')
    keyboard = Keyboard.New(Keyboard.Regular_Keys())
    brain = HTMBrain(p1, p2, p3,
        stm=base_path+'stm',
        ltm=base_path+'ltm',
        sensory_nerves=
            mouse_eye.sensory_nerves + 
            keyboard.sensory_nerves,
        motor_nerves=
            mouse_eye.motor_nerves
            keyboard.motor_nerves
        )
    return brain, [mouse_eye, keyboard] 
#every base_path should effectively represent a folder containing computatrum information
#this file should be kept with any saves
#it is run by the computatrum class
#on save, the computatrum simply calls save on its intelligence and body parts