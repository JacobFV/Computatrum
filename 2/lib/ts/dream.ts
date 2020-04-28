class Dream {
    
    senses: Sense[]
    actuators: Actuator[]

    constructor(dLayers: Number[],
                pLayers: Number[],
                senses: Sense[],
                actuators: Actuator[]
                ) {
                    this.senses = senses
                }
}

interface Interface {
    (): Number[];
}

class Sense implements Interface {
    sense(): Number[] {
        return [1, 2]
    }
    obe(): Number {
        return new Number(3)
    }
}