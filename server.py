import os
import mimetypes
from microdot import Microdot, Response  # type: ignore

app = Microdot()


@app.route('/')
async def index(request):
    with open('index.html', 'r') as f:
        r = Response(f.read())
    
    r.headers['Content-Type'] = 'text/html'
    return r


@app.route('/<path:path>')
async def static_files(request, path):
    if not os.path.isfile(path):
        return Response('File not found', status_code=404)

    mime_type, _ = mimetypes.guess_type(path)
    with open(path, 'rb') as f:
        content = f.read()

    return Response(
        content,
        headers={'Content-Type': mime_type or 'application/octet-stream'}
    )


app.run(port=8010, debug=True)
