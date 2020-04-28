const fs = require('fs')
const path = require('path')
const spawn = require('child_process').spawn

const settings = JSON.parse(fs.readFileSync('settings.json', 'utf-8'))

module.exports = (db_interface) => { return {
    allComputatrumIds: () => {
        return db_interface.listKeys()
    },
    getComputatrumAllProperties: (id) => {
        return db_interface.read(id)
    },
    getComputatrumSomeProperties: (id, properties) => {
        computatrum = module.exports.getComputatrum(id)
        values = { }
        properties.foreach(property => {
            values[property] = computatrum[property]
        })
        return values
    },
    setComputatrumProperties: (id, new_properties_values) => {
        computatrum = db_interface.read(id)
        for(const property in new_properties_values) {
            computatrum[property] = new_properties_values[property]
        }
        db_interface.write(id, computatrum)
    },
    launchComputatrum: (fps, image, endpoint, id) => {
        let dirs = __dirname.split(path.sep) // ends with 'app_logic' dir
        dirs.pop() //ends with 'supervisor' dir
        dirs = path.join(...dirs, 'computatrum', 'computatrum.py')
        
        id = id || 'c-'((settings.name.base ** settings.name.digits) * Math.random()).toString(settings.name.base)
    
        db_interface.write(id, {
            'id': id,
            'image': image,
            'state': settings.computatrum_states[0],
            'desired_fps': fps
        })
        spawn(settings['python_command'], [
            dirs,
            '--id', id,
            '--image', image,
            '--initial-state', settings.computatrum_states[0],
            '--desired-fps', fps,
            '--endpoint', endpoint
        ])
    },
    didTerminateSuccessfully: (id) => {
        db_interface.delete(id)
    },
    getComputatrumStates: () => {
        return settings.computatrum_states
    },
    getInterfaceButtons: () => {
        return settings.interface_buttons
    }
}}