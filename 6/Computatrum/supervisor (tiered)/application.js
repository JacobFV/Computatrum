console.log('computatrum supervisor running')

//const web_server = require('./web_server/web_server')
const app_logic = require('./app_logic/app_logic')
const db_interface = require('./db_interface/db_interface')

db_interface.open('db.json')
web_server.serve(app_logic(db_interface)).listen()