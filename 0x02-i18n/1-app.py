#!/usr/bin/env python3
"""
flask module with i18n and l10n
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Flask babel configuration class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@app.route("/", strict_slashes=False)
def index() -> str:
    """index page to say hello"""
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
