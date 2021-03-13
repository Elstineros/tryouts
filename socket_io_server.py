from aiohttp import web
import socketio
import os

# create a new aysnc socket io server
socket_io = socketio.AsyncServer()

#create a new Aiohttp web application
web_app = web.Application()

#bind the socket.io server to the web application instance
socket_io.attach(web_app)

#define endpoints 
async def index(request):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'index.html')
    with open(filename) as file_obj:
        return web.Response(text = file_obj.read(), content_type='text/html')

variable = 0

i = 1
while i < 6:
  print(i)
  variable = i
  i += 1

@socket_io.on('message')
async def print_message(id, message):
    print("socket id is {}".format(id))
    print(message)
    #enabling two-way communication
    await socket_io.emit('message', str(variable) + ' ' + message)


#bind the aiohttp endpoint to the web_application
web_app.router.add_get('/',index)

#start the server
if __name__ == '__main__':
    web.run_app(web_app)
