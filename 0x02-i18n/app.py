#!/usr/bin/env python3
"""
flask module with i18n and l10n
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
from typing import Optional
import pytz
from datetime import datetime


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


@babel.timezoneselector
def get_timezone() -> str:
    """Retrieve user preferred timezone"""
    timezone = request.args.get('timezone')

    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user:
        try:
            timezone = g.user.get('timezone')
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return app.config.get('BABEL_DEFAULT_TIMEZONE', 'UTC')


def get_user() -> Optional[str]:
    """Retrieve user"""
    user = request.args.get('login_as')

    if user:
        try:
            return users.get(int(user))
        except (ValueError, TypeError):
            pass
    return None


@app.before_request
def before_request() -> None:
    """Function that runs before each request to find the user."""
    g.user = get_user()


@app.route("/", strict_slashes=False)
def index() -> str:
    """index page to say hello"""
    current_datetime = format_datetime(datetime.utcnow())
    return render_template(
        "index.html",
        user=g.user,
        current_datetime=current_datetime
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
