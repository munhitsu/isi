from flask import Flask

from flask.ext.jsonpages import JSONPages
from flask import render_template
from subprocess import Popen, PIPE


app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
pages = JSONPages(app)
for page in pages:
    print page

@app.route('/')
def index():
    page = pages.get_or_404('index')
    template = page.content.get('template', 'default.html')
    return render_template(template, page=page)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.content.get('template', 'default.html')
    return render_template(template, page=page)

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
