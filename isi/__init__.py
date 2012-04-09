from flask import Flask

from flask.ext.jsonpages import JSONPages
from flask import render_template
from subprocess import Popen, PIPE
from flask.helpers import send_from_directory
import os.path
from werkzeug.exceptions import NotFound

app = Flask(__name__)

#TODO: disable static="" on production not to duplicate nginx check
app.config.from_pyfile('settings.cfg')
pages = JSONPages(app)

@app.route('/')
def index():
    page = pages.get_or_404('')
    template = page.content.get('template', 'default.html')
    return render_template(template, **page.content)

@app.route('/<path:path>/')
def page(path):
    #as werkzeug uses unordered dictionary for url mapping, let's hack for static files
    try:
        return send_from_directory(os.path.join(app.root_path,"static"), path, as_attachment=True)
    except NotFound:
        pass
    page = pages.get_or_404(path)
    template = page.content.get('template', 'default.html')
    return render_template(template, **page.content)



#github hook
#TODO: move to separate module
app.config.setdefault('GITHUBHOOK_CMD', "git pull")

#TODO: add throttling
@app.route("/githubhook", methods=['POST'])
def githubhook():
    cwd = app.root_path
    def system(cmd):
        print ''.join(Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True, cwd=cwd).communicate())

    cmd = app.config['GITHUBHOOK_CMD']

    print "Received POST, running: %s" % cmd
    system(cmd)
    return 'ok'


def main():
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()
