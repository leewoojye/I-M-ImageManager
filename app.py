from hashlib import sha1
from shutil import rmtree
from stat import S_ISREG, ST_CTIME, ST_MODE
import json
import os
import time
import textfromimage
from keybertt import mainpoint

from PIL import Image, ImageFile #이미지 정보 조회, 편집 기능 제공
from gevent.event import AsyncResult
from gevent.queue import Empty, Queue
from gevent.timeout import Timeout
import flask
import findfile


DATA_DIR = 'C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static'
KEEP_ALIVE_DELAY = 25
MAX_IMAGE_SIZE = 800, 600
MAX_IMAGES = 10
MAX_DURATION = 300

APP = flask.Flask(__name__, static_folder=DATA_DIR)
BROADCAST_QUEUE = Queue()

try:  # Reset saved files on each start
    rmtree(DATA_DIR, True)
    os.mkdir(DATA_DIR)
except OSError:
    pass


def broadcast(message):
    """Notify all waiting waiting gthreads of message."""
    waiting = []
    try:
        while True:
            waiting.append(BROADCAST_QUEUE.get(block=False))
    except Empty:
        pass
    print('Broadcasting {} messages'.format(len(waiting)))
    for item in waiting:
        item.set(message)


def receive():
    """Generator that yields a message at least every KEEP_ALIVE_DELAY seconds.

    yields messages sent by `broadcast`.

    """
    now = time.time()
    end = now + MAX_DURATION
    tmp = None
   
    while now < end:
        if not tmp:
            tmp = AsyncResult()
            BROADCAST_QUEUE.put(tmp)
        try:
            yield tmp.get(timeout=KEEP_ALIVE_DELAY)
            tmp = None
        except Timeout:
            yield ''
        now = time.time()


def safe_addr(ip_addr):
    """Strip off the trailing two octets of the IP address."""
    return '.'.join(ip_addr.split('.')[:2] + ['xxx', 'xxx'])


def save_normalized_image(path, data,sha1sum): #이미지에서 텍스트 추출 및 핵심 단어를 찾아서 메모장에 저장하는 과정까지 포함.
    """Generate an RGB thumbnail of the provided image."""
    image_parser = ImageFile.Parser()
    try:
        image_parser.feed(data)
        image = image_parser.close()
    except IOError:
        return False

    image.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(path)
    
    textfromimage.tdi(sha1sum)
    mainpoint.pointword(sha1sum)
    mainpoint.relativeword(sha1sum)
    
    #file_path = "C:\\upload\\1{}.txt".format(sha1sum) #전문 텍스트 파일은 저장 공간을 위해 핵심 단어 추출이 끝나면 삭제한다.
    #if os.path.exists(file_path):
    #    os.remove(file_path)
    
    #이미지에서 텍스트 추출, 텍스트에서 핵심 단어 추출, "핵심 단어와 관련된 단어들도 같이" 메모장에 저장.
    return True


def event_stream(client):
    """Yield messages as they come in."""
    force_disconnect = False
    try:
        for message in receive():
            yield 'data: {}\n\n'.format(message)
        print('{} force closing stream'.format(client))
        force_disconnect = True
    finally:
        if not force_disconnect:
            print('{} disconnected from stream'.format(client))


@APP.route('/search', methods=['GET', 'POST'])
def search():
    uid=flask.request.args.get('uid') #get이냐 post냐 방식에 따라 request.form, request.args 달라짐
   
    image_file=[]
    image_file=findfile.searcher(uid) #image_file="{}".format(findfile.searcher(uid))
    if image_file==[]: #아무 사진도 검색되지 않으면 fail 문장 출력.
        return flask.render_template('showing_fail.html')
    else:
        return flask.render_template('showing.html', image_file=image_file)
    
    
@APP.route('/post', methods=['POST'])
def post():
    """Handle image uploads."""
    sha1sum = sha1(flask.request.data).hexdigest()
    target = os.path.join(DATA_DIR, '{}.jpg'.format(sha1sum)) #sha1sum 인자는 파일 이름에 해당함.
    message = json.dumps({'src': target,
                          'ip_addr': safe_addr(flask.request.access_route[0])})
    try:
        if save_normalized_image(target, flask.request.data, sha1sum):
            broadcast(message)  # Notify subscribers of completion
    except Exception as exception:  # Output errors
        return '{}'.format(exception)
    return 'success'


@APP.route('/stream')
def stream():
    """Handle long-lived SSE streams."""
    return flask.Response(event_stream(flask.request.access_route[0]),
                          mimetype='text/event-stream')


@APP.route('/')
def home(): #갤러리에 이미지를 보여주는 코드
    """Provide the primary view along with its javascript."""
    image_infos = []
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        file_stat = os.stat(filepath)
        if S_ISREG(file_stat[ST_MODE]):
            image_infos.append((file_stat[ST_CTIME], filepath))

    images = []
    for i, (_, path) in enumerate(sorted(image_infos, reverse=True)):
        if i >= MAX_IMAGES:
            os.unlink(path)
            continue
        images.append('<div><img alt="User uploaded image" src="{}" /></div>'
                      .format(path))
    return """

<!doctype html>
<title>Image Manager</title>
<meta charset="utf-8" />
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.1/jquery-ui.min.js"></script>
<link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.1/themes/vader/jquery-ui.css" />

<style>
  body {
    max-width: 800px;
    margin: auto;
    padding: 1em;
    background: white;
    color: #000;
    font: 16px/1.6 menlo, monospace;
    text-align:center;
  }
  a {
    color: #000;
  }
  .notice {
    font-size: 80%%;
  }
  .search {
      position: relative;
      width: 300px;
  }
  input {
      width: 100%%;
      border: 1px solid #bbb;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 14px;
  }
#drop {
    font-weight: bold;
    text-align: center;
    padding: 1em 0;
    margin: 1em 0;
    color: #555;
    border: 2px dashed #555;
    border-radius: 7px;
    cursor: default;
}
#drop.hover {
    color: #f00;
    border-color: #f00;
    border-style: solid;
    box-shadow: inset 0 3px 4px #888;
}
</style>

<h3>Image Manager(디지털 이미지 관리 서비스)</h3>
<p>
모두가 볼 수 있도록 이미지를 업로드하세요. 유효한 이미지는 현재 연결된 모든 사람에게 푸시되며 가장 최근 %s개의 이미지만 저장됩니다.</p>
<p class="notice">디지털 이미지 관리 페이지에 오신 걸 환영합니다. 이미지를 업로드하고 이미지 속 텍스트를
바탕으로 한 이미지 관리 서비스를 이용해보세요.</p>
<noscript>Note: You must have javascript enabled in order to upload and
dynamically view new images.</noscript>
<fieldset>
  <p id="status">Select an image</p>
  <div id="progressbar"></div>
  <input id="file" type="file" />
  <div id="drop">or drop image here</div>
</fieldset>

<form action='/search'>
  <input type='text' name='uid' placeholder="검색어를 입력해 원하는 사진을 찾아보세요" required/>
  <input type="submit" value="검색"/>
</form>

<div id="images">%s</div>
<script>
  function sse() {
      var source = new EventSource('/stream');
      source.onmessage = function(e) {
          if (e.data == '')
              return;
          var data = $.parseJSON(e.data);
          var upload_message = 'Image uploaded by ' + data['ip_addr'];
          var image = $('<img>', {alt: upload_message, src: data['src']});
          var container = $('<div>').hide();
          container.append($('<div>', {text: upload_message}));
          container.append(image);
          $('#images').prepend(container);
          image.load(function(){
              container.show('blind', {}, 1000);
          });
      };
  }
  function file_select_handler(to_upload) {
      var progressbar = $('#progressbar');
      var status = $('#status');
      var xhr = new XMLHttpRequest();
      xhr.upload.addEventListener('loadstart', function(e1){
          status.text('uploading image');
          progressbar.progressbar({max: e1.total});
      });
      xhr.upload.addEventListener('progress', function(e1){
          if (progressbar.progressbar('option', 'max') == 0)
              progressbar.progressbar('option', 'max', e1.total);
          progressbar.progressbar('value', e1.loaded);
      });
      xhr.onreadystatechange = function(e1) {
          if (this.readyState == 4)  {
              if (this.status == 200)
                  var text = 'upload complete: ' + this.responseText;
              else
                  var text = 'upload failed: code ' + this.status;
              status.html(text + '<br/>Select an image');
              progressbar.progressbar('destroy');
          }
      };
      xhr.open('POST', '/post', true);
      xhr.send(to_upload);
  };
  function handle_hover(e) {
      e.originalEvent.stopPropagation();
      e.originalEvent.preventDefault();
      e.target.className = (e.type == 'dragleave' || e.type == 'drop') ? '' : 'hover';
  }

  $('#drop').bind('drop', function(e) {
      handle_hover(e);
      if (e.originalEvent.dataTransfer.files.length < 1) {
          return;
      }
      file_select_handler(e.originalEvent.dataTransfer.files[0]);
  }).bind('dragenter dragleave dragover', handle_hover);
  $('#file').change(function(e){
      file_select_handler(e.target.files[0]);
      e.target.value = '';
  });
  sse();

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-510348-17']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>
""" % (MAX_IMAGES, '\n'.join(images))  # noqa


if __name__ == '__main__':
    APP.debug = True
    APP.run('0.0.0.0', threaded=True)