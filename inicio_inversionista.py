from flask import Blueprint, render_template, request, redirect, session
from userLogic import UserLogic
from userObj import UserObj
from inversorLogic import inversorLogic
from inversorObj import inversorObj
from emprendedorLogic import emprendedorLogic
from emprendedorObj import emprendedorObj
from emprendimientoLogic import emprendimientoLogic
from interesLogic import interesLogic
from especialidadObj import especialidadObj
from guardadosLogic import guardadosLogic
from guardadosObj import guardadosObj
from productoLogic import productoLogic
from productoObj import productoObj
from busquedaLogic import busquedaLogic
from likeLogic import likeLogic
from ofertaLogic import ofertaLogic
from categoriaLogic import CategoriaLogic

# Envio correo
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

inicio_inversionista = Blueprint(
    "module2_bp", __name__, template_folder="Templates", static_folder="static"
)


@inicio_inversionista.route("/InicioInv", methods=["GET", "POST"])
def InicioInv():
    try:
        session["empId"] = ""
        user = session["user"]
        id_user = int(user["id"])
        logicInt = interesLogic()
        logicInv = inversorLogic()
        datos = logicInv.getIdInversor(id_user)
        Inversor = logicInv.createDictionary(datos)
        id_inv = int(Inversor["id"])
        session["id_inv"] = id_inv
        intereses = logicInt.getAllInteresByIdInv(id_inv)
        data = []
        for registro in intereses:
            if registro not in data:
                data.append(registro)

        if request.method == "GET":
            return render_template("inicioInversionista.html", data=data, message="")
        elif request.method == "POST":
            return render_template("inicioInversionista.html", data=data, message="")
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


@inicio_inversionista.route("/busqueda", methods=["GET", "POST"])
def busqueda():
    try:
        busqueda = request.form["busqueda"]
        bLogic = busquedaLogic()

        if request.method == "GET":
            return render_template("busquedas.html", message="")
        elif request.method == "POST":
            logicEmp = emprendimientoLogic()
            empData = []
            Emprendimientos = bLogic.buscarEmprendimiento(busqueda)
            prodData = bLogic.buscarProducto(busqueda)

            for id_emprendimiento in Emprendimientos:
                Emprendimiento = logicEmp.getEmprendimientoById(id_emprendimiento)
                empData.append(Emprendimiento)
            return render_template(
                "busquedas.html", prodData=prodData, empData=empData, busqueda=busqueda,
            )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


@inicio_inversionista.route("/perfilInversionista", methods=["GET", "POST"])
def perfilInversionista():
    try:
        # Datos de sesion
        user = session["user"]
        id_user = int(user["id"])
        logicInv = inversorLogic()
        categorias = CategoriaLogic().getAllCategorias()

        if request.method == "GET":
            datos = logicInv.getIdInversor(id_user)
            Inversor = logicInv.createDictionary(datos)
            id_inv = int(Inversor["id"])
            nombre = Inversor["nombre"]
            biografia = Inversor["biografia"]
            ciudad = Inversor["ciudad"]
            pais = Inversor["pais"]
            email = Inversor["email"]
            nombre_foto = Inversor["nombre_foto"]
            interes = logicInv.getIntereses(id_inv)
            return render_template(
                "perfil_inversionista.html",
                nombre=nombre,
                ciudad=ciudad,
                biografia=biografia,
                pais=pais,
                email=email,
                message="",
                interes=interes,
                nombre_foto=nombre_foto,
                categorias=categorias,
            )
        elif request.method == "POST":
            formId = int(request.form["formId"])
            print(formId)
            if formId == 1:
                datos = logicInv.getIdInversor(id_user)
                Inversor = logicInv.createDictionary(datos)
                id_inv = int(Inversor["id"])
                nombre = Inversor["nombre"]
                biografia = Inversor["biografia"]
                ciudad = Inversor["ciudad"]
                pais = Inversor["pais"]
                email = Inversor["email"]
                nombre_foto = Inversor["nombre_foto"]
                interes = logicInv.getIntereses(id_inv)
                return render_template(
                    "perfil_inversionista.html",
                    editar=True,
                    nombre=nombre,
                    ciudad=ciudad,
                    biografia=biografia,
                    pais=pais,
                    email=email,
                    message="",
                    interes=interes,
                    categorias=categorias,
                )
            if formId == 2:
                # Update
                datos = logicInv.getIdInversor(id_user)
                Inversor = logicInv.createDictionary(datos)
                id_inv = int(Inversor["id"])
                pic = request.files["fileToUpload"]
                name = request.form["nombre"]
                bio = request.form["biografia"]
                city = request.form["ciudad"]
                country = request.form["pais"]
                mail = request.form["email"]
                if pic.filename == "":
                    logicInv.updateInversionista(
                        id_inv, name, bio, mail, id_user, country, city
                    )
                else:
                    binary_foto = pic.read()
                    logicInv.updateInversionistaConFoto(
                        id_inv, name, bio, mail, country, city, binary_foto, id_user
                    )

                # Actualizar datos
                datos = logicInv.getIdInversor(id_user)
                Inversor = logicInv.createDictionary(datos)
                id_inv = int(Inversor["id"])
                nombre = Inversor["nombre"]
                biografia = Inversor["biografia"]
                ciudad = Inversor["ciudad"]
                pais = Inversor["pais"]
                email = Inversor["email"]
                foto = Inversor["foto"]
                nombre_foto = Inversor["nombre_foto"]
                print(nombre_foto)
                interes = logicInv.getIntereses(id_inv)

                return render_template(
                    "perfil_inversionista.html",
                    editar=False,
                    nombre=nombre,
                    ciudad=ciudad,
                    biografia=biografia,
                    pais=pais,
                    email=email,
                    foto=foto,
                    nombre_foto=nombre_foto,
                    message="",
                    interes=interes,
                    categorias=categorias,
                )
            if formId == 3:
                # Borrar interes
                idInteres = int(request.form["id"])
                logicInv.deleteInteres(idInteres)

                datos = logicInv.getIdInversor(id_user)
                Inversor = logicInv.createDictionary(datos)
                id_inv = int(Inversor["id"])
                nombre = Inversor["nombre"]
                biografia = Inversor["biografia"]
                ciudad = Inversor["ciudad"]
                pais = Inversor["pais"]
                email = Inversor["email"]
                nombre_foto = Inversor["nombre_foto"]
                interes = logicInv.getIntereses(id_inv)

                return render_template(
                    "perfil_inversionista.html",
                    editar=False,
                    nombre=nombre,
                    ciudad=ciudad,
                    biografia=biografia,
                    pais=pais,
                    email=email,
                    message="Interes eliminado",
                    interes=interes,
                    nombre_foto=nombre_foto,
                    categorias=categorias,
                )
            if formId == 4:
                datos = logicInv.getIdInversor(id_user)
                Inversor = logicInv.createDictionary(datos)
                id_inv = int(Inversor["id"])
                nombre = Inversor["nombre"]
                biografia = Inversor["biografia"]
                ciudad = Inversor["ciudad"]
                pais = Inversor["pais"]
                email = Inversor["email"]
                nombre_foto = Inversor["nombre_foto"]
                interes = logicInv.getIntereses(id_inv)
                return render_template(
                    "perfil_inversionista.html",
                    nombre=nombre,
                    ciudad=ciudad,
                    biografia=biografia,
                    pais=pais,
                    email=email,
                    message="",
                    interes=interes,
                    agregar=True,
                    categorias=categorias,
                    nombre_foto=nombre_foto,
                )
            if formId == 5:
                datos = logicInv.getIdInversor(id_user)
                Inversor = logicInv.createDictionary(datos)
                id_inv = int(Inversor["id"])
                user = session["user"]
                id_user = int(user["id"])
                # Insertando nuevos intereses
                categorias = CategoriaLogic().getAllCategorias()
                for checkbox in categorias:
                    id_categoria = checkbox["id"]
                    value = request.form.get(str(id_categoria))
                    AlreadyExist = logicInv.checkInteresAlradyAdded(
                        id_inv, id_categoria
                    )
                    if value and AlreadyExist is False:
                        logicInv.insertNewInteres(id_categoria, id_inv)

                nombre = Inversor["nombre"]
                biografia = Inversor["biografia"]
                ciudad = Inversor["ciudad"]
                pais = Inversor["pais"]
                email = Inversor["email"]
                nombre_foto = Inversor["nombre_foto"]
                interes = logicInv.getIntereses(id_inv)
                return render_template(
                    "perfil_inversionista.html",
                    nombre=nombre,
                    ciudad=ciudad,
                    biografia=biografia,
                    pais=pais,
                    email=email,
                    message="Interes agregado",
                    interes=interes,
                    nombre_foto=nombre_foto,
                    categorias=categorias,
                )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


@inicio_inversionista.route("/guardar", methods=["GET", "POST"])
def guardar():
    logic = guardadosLogic()
    id_inv = session["id_inv"]
    id_producto = int(request.form["id"])
    existeGuardado = logic.checkGuardado(id_inv, id_producto)
    if not existeGuardado:
        logic.guardar(id_inv, id_producto)
    if request.method == "GET":
        return redirect("/registroProductosInv")
    elif request.method == "POST":
        return redirect("/registroProductosInv")


@inicio_inversionista.route("/guardadosInv", methods=["GET", "POST"])
def guardadosInv():
    try:
        # Datos de sesion
        user = session["user"]
        id_user = int(user["id"])
        logicInv = inversorLogic()
        datos = logicInv.getIdInversor(id_user)
        Inversor = logicInv.createDictionary(datos)
        id_inv = int(Inversor["id"])
        # Guardados
        logicSave = guardadosLogic()
        data = logicSave.getAllGuardados(id_inv)
        if request.method == "GET":
            return render_template("guardadosInversionista.html", data=data, message="")
        elif request.method == "POST":
            formId = int(request.form["formId"])
            id_prod = request.form["id"]
            if formId == 2:
                logicSave.deleteGuardado(id_inv, id_prod)
                data = logicSave.getAllGuardados(id_inv)
            return render_template("guardadosInversionista.html", data=data, message="")
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


@inicio_inversionista.route("/infoEmprendimiento", methods=["GET", "POST"])
def correo():
    try:
        logic = emprendimientoLogic()
        message = ""
        idEmprendimiento = session["empId"]
        logicOferta = ofertaLogic()
        if request.method == "GET":
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            data3 = logic.getDatosGeneralesById(idEmprendimiento)
            data4 = logic.getDescripcion(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            return render_template(
                "informacion.html",
                data=data,
                data2=data2,
                data3=data3,
                data4=data4,
                message=message,
                vistaInversor=True,
                ultima_oferta=ultima_oferta,
            )
        elif request.method == "POST":
            # Datos de sesion
            user = session["user"]
            id_user = int(user["id"])
            usuario = user["usuario"]
            logicInv = inversorLogic()
            datos = logicInv.getIdInversor(id_user)

            idEmprendimiento = session["empId"]
            logicEmpr = emprendimientoLogic()
            infoEmpren = logicEmpr.getIdEmprendimiento(idEmprendimiento)
            logicEmpr.FundadoresByEmprendimientoCorreo(usuario, idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            message = request.form["message"]
            user = "fishing.corporation2020@gmail.com"
            password = "ilovefishing123"

            # Host y puerto SMTP de Gmail
            gmail = smtplib.SMTP("smtp.gmail.com", 587)

            # protocolo de cifrado de datos
            gmail.starttls()

            # Credenciales
            gmail.login(user, password)

            # muestra de la depuracion de la operacion de envio 1=True
            gmail.set_debuglevel(1)

            header = MIMEMultipart()
            header["Subject"] = "¡Alguien está interesado en tu emprendimiento!"
            header["From"] = "fishing.corporation2020@gmail.com"
            header["To"] = f"{infoEmpren.getEmail()}"
            Intro = f"{datos.getNombre()} {datos.getEmail()} está interesado en tu emprendimiento.\nSu mensaje es el siguiente: "
            mensaje = Intro + message

            mensaje = MIMEText(mensaje, "html")  # Content-type:text/html
            header.attach(mensaje)

            # Enviar email: remitentente, destinatario, mensaje
            gmail.sendmail(
                "fishing.corporation2020@gmail.com",
                f"{infoEmpren.getEmail()}",
                header.as_string(),
            )

            # Cerrar la conexion SMTP
            gmail.quit()
            print("Correo enviado exitosamente")

            message1 = "Correo enviado exitosamente"
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            # logicEmpr.FundadoresByEmprendimientoCorreo(id_user, idEmprendimiento)
            return render_template(
                "informacion.html",
                data=data,
                data2=data2,
                message1=message1,
                vistaInversor=True,
                ultima_oferta=ultima_oferta,
            )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


@inicio_inversionista.route("/like", methods=["GET", "POST"])
def like():
    logic = likeLogic()
    id_inv = session["id_inv"]
    id_producto = int(request.form["id"])
    logic.like(id_inv, id_producto)
    if request.method == "GET":
        return redirect("/registroProductosInv")
    elif request.method == "POST":
        return redirect("/registroProductosInv")


@inicio_inversionista.route("/unLike", methods=["GET", "POST"])
def unLike():
    logic = likeLogic()
    id_inv = session["id_inv"]
    id_producto = int(request.form["id"])
    logic.unLike(id_inv, id_producto)
    if request.method == "GET":
        return redirect("/registroProductosInv")
    elif request.method == "POST":
        return redirect("/registroProductosInv")
