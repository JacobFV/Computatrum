const express = require('express')
const bodyParser = require('body-parser')
const port = 80

module.exports = (app_logic) => { 
    const server = express()
    server.use(bodyParser.json())
    
    //web serving
    server.use(express.static(path.join(__dirname, 'web')))
    //application serving
    server.get('/api/computatrum_states', (req, res) => {
        res.send(app_logic.getComputatrumStates())
    })
    server.get('/api/interface_buttons', (req, res) => {
        res.send(app_logic.getInterfaceButtons())
    })
    server.get('/api/launch_computatrum', (req, res) => {
        app_logic.launchComputatrum(
            req.params.fps,
            req.params.image,
            `http://localhost:${port}`)
    })
    //database serving
    server.get('/computatrum_ids', (req, res) => {
        res.send(app_logic.allComputatrumIds())
    })
    server.get('/computatrums/:id', (req, res) => {
        res.send(app_logic.getComputatrumAllProperties(req.params.id))
    })
    server.post('/computatrums/:id', (req, res) => {
        app_logic.setComputatrumProperties(
            req.params.id,
            req.body)
    })
    server.get('/computatrums/:id/:property', (req, res) => {
        res.send(app_logic.getComputatrumSomeProperties(
            req.params.id,
            [req.params.property]))
    })
    server.post('/computatrums/:id/:property', (req, res) => {
        app_logic.setComputatrumProperties(
            req.params.id,
            {
                req.params.property: req.body
            }
        )
    })

    return {
        listen: () => {
            server.listen(port, () => console.log(`Example app listening on port ${port}!`))
        }
    }
}