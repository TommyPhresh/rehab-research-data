import os
from flask import Flask

from db import SearchEngine
from user import register_user_loader
from extensions import login_manager, cache, mail

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.secret_key = 'MXt9mp8qaCFg9p8j1eiGI21A$'
    DB_PATH = 'data/rehab-research-v2.db'
    INDEX_PATH = 'index/embeddings.index'
    try:
        app.search_engine = SearchEngine(
            db_path=DB_PATH,
            index_path=INDEX_PATH,
            model_name='all-MiniLM-L6-v2'
        )
        print('Loaded search engine')
    except Exception as e:
        print('Error in search engine load:', e)

    login_manager.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    register_user_loader()
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)