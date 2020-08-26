from flask import Flask, render_template, request, redirect, session
from login_registro import login_registro
from registro_productos import registro_productos
from inicio_inversionista import inicio_inversionista
from emprendimiento import emprendimiento
from emprendimientoInicio import emprendimientoInicio
from emprendedorProfile import emprendedorProfile
from cerrarSesion import cerrarSesion
from admin import admin

app = Flask(__name__)
app.register_blueprint(login_registro, url_prefix="")
app.register_blueprint(registro_productos, url_prefix="")
app.register_blueprint(inicio_inversionista, url_prefix="")
app.register_blueprint(emprendimiento, url_prefix="")
app.register_blueprint(emprendimientoInicio, url_prefix="")
app.register_blueprint(emprendedorProfile, url_prefix="")
app.register_blueprint(cerrarSesion, url_prefix="")
app.register_blueprint(admin, url_prefix="")
app.secret_key = "ILoveFishing"


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
