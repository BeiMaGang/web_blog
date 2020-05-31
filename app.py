# coding = utf8
from flask import Flask, render_template
from flask_cors import CORS
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex = items[0]


def create_app(config_name='dev'):
    app = Flask(
        __name__,
        template_folder='frontend/templates',
        static_folder='frontend/assets',
    )
    app.url_map.converters['reg'] = RegexConverter
    CORS(app)

    @app.route('/<reg(".*\.html$"):page>')
    def dif_page(page):
        return render_template(page)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('login.html')
    #
    # @app.route('/login.html', methods=['GET', 'POST'])
    # def index1():
    #     return render_template('login.html')
    #
    # @app.route('/register.html', methods=['GET', 'POST'])
    # def index2():
    #     return render_template('register.html')

    from view import auth
    app.register_blueprint(auth.bp, url_prefix='/auth')

    from view import blog
    app.register_blueprint(blog.bp)

    from view import user
    app.register_blueprint(user.bp)

    from view import comment
    app.register_blueprint(comment.bp)

    return app