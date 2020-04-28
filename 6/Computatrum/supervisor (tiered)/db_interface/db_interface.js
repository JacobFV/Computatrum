const fs = require('fs')
const config = JSON.parse(fs.readFileSync('config.json', 'utf-8'))

let data_path = ''
let data = { }

module.exports.new = (path) => {
    data_path = path
    data = { }
    module.exports.saveSync()
}

module.exports.openAsync = (path, callback) => {
    data_path = path
    fs.readFile(data_path, 'utf-8', (err, opened_data) => {
        data = JSON.parse(opened_data)
        callback()
    })
}

module.exports.openSync = (path) => {
    data_path = path
    data = JSON.parse(fs.readFileSync(data_path, 'utf-8'))
}

module.exports.saveAsync = (callback) => {
    fs.writeFile(data_path, JSON.stringify(data), (err) => callback())
}

module.exports.saveSync = () => {
    fs.writeFileSync(data_path, JSON.stringify(data))
}

module.exports.saveAsAsync = (new_path, callback) => {
    data_path = new_path
    module.exports.saveAsync(callback)
}

module.exports.saveAsSync = (new_path) => {
    data_path = new_path
    module.exports.saveSync()
}

module.exports.listKeys = () => {
    return Object.keys(data)
}

module.exports.read = (key) => {
    return data[key]
}

module.exports.write = (key, value) => {
    data[key] = value
}

module.exports.delete = (key) => {
    delete data[key]
}

setTimeout(this.saveAsync(err => {}), config['autosave'])