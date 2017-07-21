from sanic import Sanic
from sanic.response import text
from sanic.response import json
from bp_cookie import bp_cookie

app = Sanic(__name__)
app.blueprint(bp_cookie)

async def notify_server_started_after_five_seconds():
    await asyncio.sleep(2)
    print('Server successfully started!')

app.add_task(notify_server_started_after_five_seconds())

@app.middleware('request')
async def print_on_request(request):
    print("[Middleware] Pre-processing the request...")

@app.middleware('response')
async def print_on_response(request, response):
    print("[Middleware] Post-processing the response...")

@app.route("/")
async def test(request):
    # return text("Hello world!")
    return json({"hello": "world!"})

@app.route('/tag/<tag>')
async def tag_handler(request, tag):
    return text('Tag - {}'.format(tag))

@app.route('/number/<integer_arg:int>')
async def integer_handler(request, integer_arg):
    return text('Integer - {}'.format(integer_arg))

@app.route('/number/<number_arg:number>')
async def number_handler(request, number_arg):
    return text('Number - {}'.format(number_arg))

@app.route('/person/<name:[A-z]>')
async def person_handler(request, name):
    return text('Person - {}'.format(name))

@app.route('/folder/<folder_id:[A-z0-9]{0,4}>')
async def folder_handler(request, folder_id):
    return text('Folder - {}'.format(folder_id))

@app.route('/get', methods=['GET'], host='localhost')
async def get_handler(request):
    return text('GET request - {}'.format(request.args))

# if the host header doesn't match example.com, this route will be used
@app.route('/get', methods=['GET'])
async def get_handler(request):
    return text('GET request in default - {}'.format(request.args))

@app.websocket('/feed')
async def feed(request, ws):
    while True:
        data = 'hello!'
        print('Sending: ' + data)
        await ws.send(data)
        data = await ws.recv()
        print('Received: ' + data)

@app.route('/query_string')
def query_string(request):
    return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })

@app.route("/form")
def post_json(request):
    return json({ "received": True, "form_data": request.form, "test": request.form.get('test') })



app.run(host='0.0.0.0', port=8088, debug=True)

