#!/usr/bin/env python3
"""
flask module with i18n and l10n
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Optional


class Config:
    """Flask babel configuration class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Retrieve user preferred locale"""
    lang = request.args.get('locale')
    if lang and lang in app.config['LANGUAGES']:
        return lang

    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    h_locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if h_locale:
        return h_locale

    return app.config['BABEL_DEFAULT_LOCALE']


def get_user() -> Optional[str]:
    """Retrieve user"""
    user = request.args.get('login_as')

    if user:
        return users.get(int(user))
    return None


@app.before_request
def before_request() -> None:
    """Function that runs before each request to find the user."""
    g.user = get_user()


@app.route("/", strict_slashes=False)
def index() -> str:
    """index page to say hello"""
    return render_template("6-index.html", user=g.user)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
