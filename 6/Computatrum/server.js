const path = require('path')
const fs = require('fs')

const BASE = 36

const express = require('express')
const app = express()
const PORT = 80
const ENDPOINT = `http://localhost:${PORT}`

const spawn = require('child_process').spawn
let computatrums = []

const bodyParser = require('body-parser')
app.use(bodyParser.json())

app.use(express.static(path.join(__dirname, 'web')))

app.get('.*/load/:page', (req, res) => {
    res.writeHead(301, {location: `${ENDPOINT}/${req.params.page}/index.html`})
    res.end()
})

app.get('/launchpad/api/base_paths', (req, res) => {
    base_paths_root = settings().base_paths_root
    res.send(
        fs.readdirSync(base_paths_root).map(
            suffix => { 
                return {
                    'suffix': suffix,
                    'fullpath': path.join(base_paths_root, suffix)
                }
            }
        )
    )     
})
app.post('.*/api/launch_computatrum', (req, res) => {
    console.log('launch')
    //post launch request
    /* {
        'launch_script': 'computatrum_simplex.py',
        'initial_state': 'paused'
    } */
    //claim lowest free id
    name = 'c' + (BASE*BASE*Math.random()).toString(BASE)
    computatrums += {
        name: name,
        launch_script: req.body.launch_script,
        base_path: req.body.base_path,
        state: req.body.initial_state,
        ideal_fps: req.body.ideal_fps,
        actual_fps: 0,
        thumbpad_up: 0.00,
        thumbpad_down: 0.00,
        thumbpad_left: 0.00,
        thumbpad_right: 0.00,
        A_button: false,
        B_button: false,
        C_button: false,
        D_button: false,
        L_button: false,
        R_button: false,
        reward: 0.00,
        punish: 0.00,
        alive: true,
        please_save: false
    }
    index = computatrums.length - 1
    spawn(
        settings().python_keyword,
        [
            path.join(__dirname, 'computatrum', 'computatrum.py'),
            '--supervisor-endpoint', ENDPOINT,
            '--name', name, 
            '--launch-script', computatrums[index].launch_script,
            '--base-path', computatrums[index].base_path,
            '--state', computatrums[index].state,
            '--fps', computatrums[index].ideal_fps
        ]
    )
})
app.get('.*/api/active_computatrums', (req, res) => {
    res.send(JSON.stringify(
        computatrums
            .filter(computatrum => computatrum.alive)
            .map(computatrum => computatrum.name)
    ))
})
app.post('.*/api/computatrum_properties', (req, res) => {
    //write properties
    index = computatrums.findIndex(computatrum => computatrum.name = req.body.name)
    properties = req.body.properties
    switch(req.body.mode) {
        case 'write':
            for(var key in properties) {
                computatrums[index][key] = properties[key]
            }
            res.send(200)
            break;
        case 'read':
            res.send(JSON.stringify(
                properties.map(key => [key, computatrums[index][key]])
            ))
            break;
        default:
            console.log(`POST ${req.body} without specifying {mode: 'read' | 'write'}`)
    }
})

function settings() {
    return JSON.parse(fs.readFileSync('save/settings.json', 'utf-8'))
}

app.listen(80, () => console.log(`computatrum supervisor listening on port ${PORT}`))