#!/usr/bin/env python3
"""
flask module with i18n and l10n
"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index() -> str:
    """index page to say hello"""
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
