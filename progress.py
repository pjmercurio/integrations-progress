import os

from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "secret_l801#+#a&^1mz)_p&qyq51j51@20_74c-xi%&i)b*u_dt^2=2key"
)


def get_progress_color(progress, scale):
    ratio = progress / scale

    if ratio < 0.2:
        return "#AD0000"
    if ratio < 0.4:
        return "#d8554d"
    if ratio < 0.6:
        return "#efad4d"
    if ratio < 0.8:
        return "#5bc0de"
    if ratio < 0.9:
        return "#347ab6"

    return "#5B53FF"


def get_template_fields(progress):
    title = request.args.get("title")

    scale = 100
    try:
        scale = int(request.args.get("scale"))
    except (TypeError, ValueError):
        pass

    progress_width = 60 if title else 90
    try:
        progress_width = int(request.args.get("width"))
    except (TypeError, ValueError):
        pass

    progress_height = 20
    try:
        progress_height = int(request.args.get("height"))
    except (TypeError, ValueError):
        pass
    
    font_size = 30
    if progress_height < 20:
        font_size = 11
    elif progress_height < 40:
        font_size = 14
    elif progress_height < 60:
        font_size = 16
    elif progress_height < 100:
        font_size = 20

    return {
        "title": title,
        "title_width": 10 + 6 * len(title) if title else 0,
        "title_color": request.args.get("color", "428bca"),
        "scale": scale,
        "font_size": font_size,
        "progress": progress,
        "progress_width": progress_width,
        "progress_height": progress_height,
        "progress_color": get_progress_color(progress, scale),
        "suffix": request.args.get("suffix", "%"),
    }


@app.route("/<int:progress>/")
def get_progress_svg(progress):
    template_fields = get_template_fields(progress)

    template = render_template("progress.svg", **template_fields)
    
    response = make_response(template)
    response.headers["Content-Type"] = "image/svg+xml"
    return response


@app.route("/")
def redirect_to_github():
    return get_progress_svg(0)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4444))
    app.run(host="0.0.0.0", port=port)
