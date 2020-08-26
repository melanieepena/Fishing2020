from flask import Blueprint, Flask, render_template, request, redirect, session
import mysql.connector
from mysql.connector import Error
from emprendedorLogic import emprendedorLogic
from emprendimientoLogic import emprendimientoLogic
from categoriaLogic import CategoriaLogic


emprendedorProfile = Blueprint(
    "emprendedorProfile", __name__, static_folder="static", template_folder="Templates",
)


@emprendedorProfile.route("/emprendedorProfile", methods=["GET", "POST"])
def ProfileEmp():
    try:
        logic = emprendedorLogic()
        logicEmprendimiento = emprendimientoLogic()
        user = session["user"]
        idUsuario = int(user["id"])
        data = logic.getDatosGeneralesById(idUsuario)
        idEmprendedor = data[0]["id"]
        categorias = CategoriaLogic().getAllCategorias()
        session["id_emprendedor"] = idEmprendedor

        if request.method == "GET":
            # Datillos
            dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                idEmprendedor
            )
            data2 = logic.getNotification(idEmprendedor)
            return render_template(
                "emprendedorProfile.html",
                data=data,
                dataEmprendimiento=dataEmprendimiento,
                data2=data2,
                categorias=categorias,
            )

        elif request.method == "POST":
            verdadero = False
            verdaderoEmprendimiento = False
            formId = int(request.form["formId"])
            data2 = logic.getNotification(idEmprendedor)
            # Modificar informacion personal
            if formId == 1:
                id = idUsuario
                nombre = request.form["nombre"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                pais = request.form["pais"]
                ciudad = request.form["ciudad"]
                biografia = request.form["biografia"]

                verdadero = True

                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    idEmprendedor
                )
                data = logic.getDatosGeneralesById(id)
                return render_template(
                    "emprendedorProfile.html",
                    id=id,
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    verdadero=verdadero,
                    nombre=nombre,
                    email=email,
                    telefono=telefono,
                    pais=pais,
                    ciudad=ciudad,
                    biografia=biografia,
                    categorias=categorias,
                )

            # Aplicar cambios en informacion general
            elif formId == 2:
                data2 = logic.getNotification(idEmprendedor)
                nombre = request.form["nombre"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                pais = request.form["pais"]
                ciudad = request.form["ciudad"]
                biografia = request.form["biografia"]
                foto = request.files["fileToUpload"]
                nombre_foto = foto.filename

                if foto.filename == "":
                    logic.updateEmprendedorbyIdUsuario(
                        idUsuario, nombre, email, telefono, pais, ciudad, biografia
                    )
                else:
                    binary_foto = foto.read()
                    logic.updateEmprendedorbyIdUsuarioWithPhoto(
                        idUsuario,
                        nombre,
                        email,
                        telefono,
                        pais,
                        ciudad,
                        biografia,
                        binary_foto,
                    )
                data = logic.getDatosGeneralesById(idUsuario)
                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    idEmprendedor
                )

                return render_template(
                    "emprendedorProfile.html",
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    categorias=categorias,
                )

            # Crear nuevo emprendimiento
            elif formId == 3:
                verdaderoEmprendimiento = True

                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    idEmprendedor
                )
                data = logic.getDatosGeneralesById(idUsuario)
                categorias = CategoriaLogic().getAllCategorias()
                return render_template(
                    "emprendedorProfile.html",
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    verdaderoEmprendimiento=verdaderoEmprendimiento,
                    categorias=categorias,
                )

            # Insertar nuevo emprendimiento
            elif formId == 4:
                data2 = logic.getNotification(idEmprendedor)
                id_emprendedor = idEmprendedor
                estado = request.form["estado"]
                descripcion = request.form["descripcion"]
                historia = request.form["historia"]
                eslogan = request.form["eslogan"]
                inversion_inicial = request.form["inversion_inicial"]
                fecha_fundacion = request.form["fecha_fundacion"]
                venta_año_anterior = request.form["venta_año_anterior"]
                nombre = request.form["nombre"]
                foto = request.files["fileToUpload"]
                nombre_foto = foto.filename
                video = request.form["video"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                facebook = request.form["facebook"]
                instagram = request.form["instagram"]
                youtube = request.form["youtube"]

                if foto.filename == "":
                    nombre_foto = "default.png"

                    logicEmprendimiento.insertNewEmprendimientoWithoutPhoto(
                        estado,
                        descripcion,
                        historia,
                        eslogan,
                        inversion_inicial,
                        fecha_fundacion,
                        venta_año_anterior,
                        id_emprendedor,
                        nombre,
                        nombre_foto,
                        video,
                        email,
                        telefono,
                        facebook,
                        instagram,
                        youtube,
                    )
                else:
                    binary_foto = foto.read()
                    logicEmprendimiento.insertNewEmprendimiento(
                        estado,
                        descripcion,
                        historia,
                        eslogan,
                        inversion_inicial,
                        fecha_fundacion,
                        venta_año_anterior,
                        id_emprendedor,
                        nombre,
                        binary_foto,
                        video,
                        email,
                        telefono,
                        facebook,
                        instagram,
                        youtube,
                    )
                id_emprendimiento = logicEmprendimiento.getNewIdEmprendimiento(
                    nombre, eslogan, fecha_fundacion
                )
                categorias = CategoriaLogic().getAllCategorias()

                for checkbox in categorias:
                    id_categoria = checkbox["id"]
                    value = request.form.get(str(id_categoria))
                    if value:
                        logicEmprendimiento.insertEspecialidad(
                            id_emprendimiento, id_categoria
                        )

                data = logic.getDatosGeneralesById(idUsuario)
                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    id_emprendedor
                )

                return render_template(
                    "emprendedorProfile.html",
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    categorias=categorias,
                )

            # Sale del emprendimiento by IdEmprendimiento
            elif formId == 5:
                data2 = logic.getNotification(idEmprendedor)
                id_emprendimiento = int(request.form["id"])
                logicEmprendimiento.salirEmprendimiento(
                    idEmprendedor, id_emprendimiento
                )
                data = logic.getDatosGeneralesById(idUsuario)
                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    idEmprendedor
                )
                return render_template(
                    "emprendedorProfile.html",
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    categorias=categorias,
                )

            # Va hacia el emprendimiento que se selecciona
            elif formId == 6:
                id = int(request.form["id"])
                emprendimiento = logicEmprendimiento.getEmprendimientoById(id)
                session["emprendimiento"] = emprendimiento.id
                return redirect("/emprendimientoInicio")
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )
