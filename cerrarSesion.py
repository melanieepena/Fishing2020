from flask import Blueprint, render_template, request, redirect, session

cerrarSesion = Blueprint(
    "cerrarSesion", __name__, template_folder="Templates", static_folder="static"
)


@cerrarSesion.route("/cerrarSesion", methods=["GET", "POST"])
def cerrarSesionInv():
    session.clear()
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return render_template("index.html")
