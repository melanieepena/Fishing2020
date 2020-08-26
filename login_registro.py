from flask import Blueprint, render_template, request, redirect, session
from userLogic import UserLogic
from userObj import UserObj
from inversorLogic import inversorLogic
from inversorObj import inversorObj
from emprendedorLogic import emprendedorLogic
from emprendedorObj import emprendedorObj
from emprendimientoLogic import emprendimientoLogic
from categoriaLogic import CategoriaLogic
import os

login_registro = Blueprint(
    "module1_bp", __name__, template_folder="Templates", static_folder="static"
)


@login_registro.route("/logIn", methods=["GET", "POST"])
def logIn():
    if request.method == "GET":
        return render_template("logInForm.html", message="")
    elif request.method == "POST":  # "POST"
        user = request.form["user"]
        password = request.form["password"]
        logic = UserLogic()
        # emprendedorLogic = emprendedorLogic()
        # emprendimientoLogic = emprendimientoLogic()
        userData = logic.getUser(user, password)
        if userData is not None:
            if userData.rol == 1:
                dataDic = logic.createDictionary(userData)
                session["user"] = dataDic
                usuario = dataDic["usuario"]
                return redirect("/Admin")
            if userData.rol == 2:
                dataDic = logic.createDictionary(userData)
                session["user"] = dataDic
                return redirect("/InicioInv")
            elif userData.rol == 3:
                dataDic = logic.createDictionary(userData)
                session["user"] = dataDic
                return redirect("/emprendedorProfile")
        else:
            return render_template(
                "loginform.html", message="Error. Usuario o contraseña incorrecta"
            )


@login_registro.route("/signUpInversor", methods=["GET", "POST"])
def signUpInversor():
    if request.method == "GET":
        categorias = CategoriaLogic().getAllCategorias()
        return render_template("registroInv.html", message="", categorias=categorias)
    elif request.method == "POST":  # "POST"
        name = request.form["nombre"]
        user = request.form["user"]
        rol = 2
        password = str(request.form["password"])
        email = str(request.form["email"])
        country = request.form["country"]
        bio = request.form["bio"]
        city = request.form["city"]
        foto = request.files["fileToUpload"]
        nombre_foto = foto.filename
        binary_foto = foto.read()

        if foto.filename == "":
            nombre_foto = "default.png"
        # Creando nuevo usuario
        logicUsuario = UserLogic()
        existeUsuario = logicUsuario.checkUserInUsuario(user, rol)
        if existeUsuario:
            return render_template(
                "registroInv.html",
                errorMessage="Este usuario ya existe, inténtelo nuevamente",
                namex=name,
                emailx=email,
                countryx=country,
                biox=bio,
                cityx=city,
            )
        else:
            logicUsuario.insertNewUser(user, password, rol)
            userData = logicUsuario.getUser(user, password)
            idUsuario = int(userData.getId())
            # Creando nuevo Inversor
            logicInversor = inversorLogic()
            if nombre_foto == "default.png":
                logicInversor.insertNewInversorWithoutPhoto(
                    name, bio, email, idUsuario, country, city, nombre_foto
                )
            else:
                logicInversor.insertNewInversor(
                    name, bio, email, idUsuario, country, city, binary_foto
                )
            logicInversor.getNewInversor(name, bio, email, idUsuario, country, city)
            idInversor = int(
                logicInversor.getNewInversor(
                    name, bio, email, idUsuario, country, city
                ).getId()
            )
            # Insertando nuevos intereses
            categorias = CategoriaLogic().getAllCategorias()
            for checkbox in categorias:
                id_categoria = checkbox["id"]
                value = request.form.get(str(id_categoria))
                if value:
                    logicInversor.insertNewInteres(id_categoria, idInversor)

            dataDic = logicUsuario.createDictionary(userData)
            session["user"] = dataDic

            return redirect("/InicioInv")


@login_registro.route("/signUpEmprendedor", methods=["GET", "POST"])
def signUpEmprendedor():
    if request.method == "GET":
        return render_template("registroEmp.html", message="")
        # return render_template("ejem.html", message="")

    elif request.method == "POST":  # "POST"
        # Recuperando datos
        name = request.form["nombre"]
        user = request.form["user"]
        rol = 3
        password = str(request.form["password"])
        email = str(request.form["email"])
        country = request.form["country"]
        phone = request.form["phone"]
        city = request.form["city"]
        bio = request.form["bio"]
        foto = request.files["fileToUpload"]
        nombre_foto = foto.filename
        binary_foto = foto.read()

        if foto.filename == "":
            nombre_foto = "default.png"
        ####
        # Creando nuevo usuario
        logicUsuario = UserLogic()
        # Comprobando rrrrff5
        existeUsuario = logicUsuario.checkUserInUsuario(user, rol)
        if existeUsuario:
            return render_template(
                "registroEmp.html",
                errorMessage="Este usuario ya existe, inténtelo nuevamente",
                namex=name,
                emailx=email,
                countryx=country,
                cityx=city,
                phonex=phone,
            )
        else:
            logicUsuario.insertNewUser(user, password, rol)
            userData = logicUsuario.getUser(user, password)
            id_user = int(userData.getId())
            # Creando nuevo emprendedor
            logicEmprendedor = emprendedorLogic()

            if nombre_foto == "default.png":
                logicEmprendedor.insertNewEmprendedorWithoutPhoto(
                    name, email, phone, id_user, country, city, bio, nombre_foto,
                )
            else:
                logicEmprendedor.insertNewEmprendedor(
                    name, email, phone, id_user, country, city, bio, binary_foto,
                )
            dataDic = logicUsuario.createDictionary(userData)
            session["user"] = dataDic
            return redirect("/emprendedorProfile")
