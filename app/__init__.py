from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__)
    from app import views
    app.register_blueprint(views.bp)
    return app


app = create_app()


if __name__ == '__main__':
    app.run()
