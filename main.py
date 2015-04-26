import os, bottle, uuid, json

import settings

from utils import get_color_palete

app = bottle.Bottle()
bottle.TEMPLATE_PATH.append(settings.TEMPLATE_ROOT)


def handle_file_upload():
  upload = bottle.request.files.get('upload')
  if upload is None:
    bottle.redirect('/')
    return

  path = str(uuid.uuid4())+'.'+ os.path.splitext(upload.filename)[1]
  upload.save(settings.IMG_ROOT+'\\'+path)
  return path


@app.get('/')
@bottle.view('index.html')
def index():
  return dict(title="")


@app.route('/static/<filename:path>')
def server_static(filename):
  return bottle.static_file(filename, root=settings.STATIC_ROOT)


@app.post('/upload')
def upload_image():
  path = handle_file_upload()
  bottle.redirect('/palete/'+path)


@app.get('/palete/<path>')
@bottle.view('dominants.html')
def get_color_palete_view(path):
  return get_color_palete(path)


@app.post('/update')
def update_color_palete():
  try:
    img_uuid_filename = bottle.request.POST.get('img_src').rsplit('/', 1)[1]
  except:
    return json.dumps({'status': 'error'})

  color_count = int(bottle.request.POST.get('color_count', 10))
  tolerance = int(bottle.request.POST.get('tolerance', 1))

  return json.dumps(get_color_palete(img_uuid_filename, color_count, tolerance))



if __name__ == '__main__':
  bottle.run(app, host='localhost', port=8080, debug=settings.DEBUG, reloader=True)