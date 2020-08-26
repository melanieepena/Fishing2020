from flask import Flask, render_template, request, redirect, session, Blueprint
from userLogic import UserLogic
from userObj import UserObj
from inversorLogic import inversorLogic
from inversorObj import inversorObj
from emprendedorLogic import emprendedorLogic
from emprendimientoLogic import emprendimientoLogic
from categoriaLogic import CategoriaLogic
from productoObj import productoObj
from productoLogic import productoLogic
from adminLogic import adminLogic
import pymysql.err

admin = Blueprint(
    "admin", __name__, template_folder="Templates", static_folder="static"
)


@admin.route("/Admin", methods=["GET", "POST"])
def Admin():
    try:
        user = session["user"]
        usuario = user["usuario"]
        return render_template("indexAdmin.html", usuario=usuario)
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
@admin.route("/inversionistaAdmin", methods=["GET", "POST"])
def inversionista():
    try:
        user = session["user"]
        logic = inversorLogic()
        uLogic = UserLogic()
        message = ""
        verdadero = False
        if request.method == "GET":
            data = logic.getAllInversionista()
            for registro in data:
                usuario = uLogic.getUserById(registro["id_usuario"])
                userName = usuario.user
                registro["id_usuario"] = userName
            return render_template(
                "inversionistaAdmin.html", data=data, message=message
            )

        elif request.method == "POST":  # "POST"
            formId = int(request.form["formId"])
            # Insertar
            if formId == 1:

                # Recoger datos
                name = request.form["nombre"]
                email = str(request.form["email"])
                country = request.form["pais"]
                bio = request.form["biografia"]
                city = request.form["ciudad"]
                foto = request.files["fileToUpload"]
                nombre_foto = foto.filename
                userName = request.form["name_usuario"]
                password = request.form["password"]
                binary_foto = foto.read()
                usuarioExiste = uLogic.checkUserInUsuario(userName, 2)
                if usuarioExiste:
                    data = logic.getAllInversionista()
                    for registro in data:
                        usuario = uLogic.getUserById(registro["id_usuario"])
                        userName = usuario.user
                        registro["id_usuario"] = userName
                    return render_template(
                        "inversionistaAdmin.html",
                        data=data,
                        message="El usuario ya existe, intentelo nuevamente",
                    )
                else:
                    uLogic.insertNewUser(userName, password, 2)
                    usuario = uLogic.getUserByUser(userName)
                    idUsuario = usuario.id
                    if foto.filename == "":
                        nombre_foto = "default.png"
                    logicInversor = inversorLogic()
                    if nombre_foto == "default.png":
                        logicInversor.insertNewInversorWithoutPhoto(
                            name, bio, email, idUsuario, country, city, nombre_foto
                        )
                    else:
                        logicInversor.insertNewInversor(
                            name, bio, email, idUsuario, country, city, binary_foto
                        )
                    message = "Se ha insertado un nuevo inversionista"
                    data = logic.getAllInversionista()
                    for registro in data:
                        usuario = uLogic.getUserById(registro["id_usuario"])
                        userName = usuario.user
                        registro["id_usuario"] = userName

                    return render_template(
                        "inversionistaAdmin.html", data=data, message=message
                    )

            # Eliminar
            elif formId == 2:
                id = int(request.form["id"])

                try:
                    logic.deleteInversionista(id)
                    data = logic.getAllInversionista()
                    for registro in data:
                        usuario = uLogic.getUserById(registro["id_usuario"])
                        userName = usuario.user
                        registro["id_usuario"] = userName
                    message = "Se ha eliminado un usuario de inversionista"

                except pymysql.err.MySQLError as error:
                    print(
                        "Failed inserting BLOB data into MySQL table {}".format(error)
                    )
                    message = (
                        "No se puede eliminar. Afecta la integridad de la base de datos"
                    )
                    data = logic.getAllInversionista()
                    for registro in data:
                        usuario = uLogic.getUserById(registro["id_usuario"])
                        userName = usuario.user
                        registro["id_usuario"] = userName

                return render_template(
                    "inversionistaAdmin.html", data=data, message=message
                )

            # Update
            elif formId == 3:
                id = int(request.form["id"])
                nombre = request.form["nombre"]
                biografia = request.form["biografia"]
                email = request.form["email"]
                userName = request.form["name_usuario"]
                session["userNameInv"] = userName
                pais = request.form["pais"]
                ciudad = request.form["ciudad"]
                # ----------------------------------
                usuario = uLogic.getUserByUser(userName)
                id_usuario = usuario.id
                verdadero = True
                data = logic.getAllInversionista()
                for registro in data:
                    usuario = uLogic.getUserById(registro["id_usuario"])
                    userName = usuario.user
                    registro["id_usuario"] = userName

                return render_template(
                    "inversionistaAdmin.html",
                    data=data,
                    message=message,
                    verdadero=verdadero,
                    id=id,
                    nombre=nombre,
                    biografia=biografia,
                    email=email,
                    id_usuario=id_usuario,
                    pais=pais,
                    ciudad=ciudad,
                )

            # Modificar inversionista
            else:
                id = int(request.form["id"])
                nombre = request.form["nombre"]
                biografia = request.form["biografia"]
                email = request.form["email"]
                userName = session["userNameInv"]
                pais = request.form["pais"]
                ciudad = request.form["ciudad"]
                foto = request.files["fileToUpload"]
                nombre_foto = foto.filename
                try:
                    usuario = uLogic.getUserByUser(userName)
                    id_usuario = usuario.id
                    if foto.filename == "":
                        logic.updateInversionista(
                            id, nombre, biografia, email, id_usuario, pais, ciudad
                        )
                    else:
                        binary_foto = foto.read()
                        logic.updateInversionistaConFoto(
                            id,
                            nombre,
                            biografia,
                            email,
                            pais,
                            ciudad,
                            binary_foto,
                            id_usuario,
                        )
                    data = logic.getAllInversionista()
                    for registro in data:
                        usuario = uLogic.getUserById(registro["id_usuario"])
                        userName = usuario.user
                        registro["id_usuario"] = userName
                    message = "Se ha modificado el inversionista"

                except pymysql.err.MySQLError as error:
                    print(
                        "Failed inserting BLOB data into MySQL table {}".format(error)
                    )
                    message = "No se puede modificar. No existe el id usuario"
                    data = logic.getAllInversionista()
                    for registro in data:
                        usuario = uLogic.getUserById(registro["id_usuario"])
                        userName = usuario.user
                        registro["id_usuario"] = userName

                return render_template(
                    "inversionistaAdmin.html", data=data, message=message
                )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------


@admin.route("/emprendedorAdmin", methods=["GET", "POST"])
def emprendedor():
    try:
        user = session["user"]
        logic = emprendedorLogic()
        uLogic = UserLogic()
        message = ""
        verdadero = False
        data = logic.getAllEmprendedores()
        for registro in data:
            usuario = uLogic.getUserById(registro["id_usuario"])
            userName = usuario.user
            registro["id_usuario"] = userName
        if request.method == "GET":
            return render_template("emprendedorAdmin.html", data=data, message=message)
        elif request.method == "POST":
            formId = int(request.form["formId"])
            # Inserta una categoría
            if formId == 1:
                userName = request.form["userName"]
                password = request.form["password"]
                name = request.form["nombre"]
                email = request.form["email"]
                phone = request.form["telefono"]
                country = request.form["pais"]
                city = request.form["ciudad"]
                bio = request.form["biografia"]
                name = request.form["nombre"]
                foto = request.files["fileToUpload"]
                nombre_foto = foto.filename
                binary_foto = foto.read()
                usuarioExiste = uLogic.checkUserInUsuario(userName, 3)
                if usuarioExiste:
                    data = logic.getAllEmprendedores()
                    for registro in data:
                        usuario = uLogic.getUserById(registro["id_usuario"])
                        userName = usuario.user
                    registro["id_usuario"] = userName
                    message = "Se ha insertado un nuevo usuario"
                    return render_template(
                        "emprendedorAdmin.html",
                        data=data,
                        message="El usuario ya existe, intentelo nuevamente",
                    )
                else:
                    uLogic.insertNewUser(userName, password, 3)
                    usuario = uLogic.getUserByUser(userName)
                    id_user = usuario.id

                    if foto.filename == "":
                        nombre_foto = "default.png"
                    if nombre_foto == "default.png":
                        logic.insertNewEmprendedorWithoutPhoto(
                            name,
                            email,
                            phone,
                            id_user,
                            country,
                            city,
                            bio,
                            nombre_foto,
                        )
                    else:
                        logic.insertNewEmprendedor(
                            name,
                            email,
                            phone,
                            id_user,
                            country,
                            city,
                            bio,
                            binary_foto,
                        )
                    data = logic.getAllEmprendedores()
                    for registro in data:
                        usuario = uLogic.getUserById(registro["id_usuario"])
                        userName = usuario.user
                    registro["id_usuario"] = userName
                    message = "Se ha insertado un nuevo usuario"
                    return render_template(
                        "emprendedorAdmin.html", data=data, message=message
                    )

            # Elimina una categoria
            elif formId == 2:
                id = int(request.form["id"])

                try:
                    logic.deleteEmprendedor(id)
                    data = logic.getAllEmprendedores()
                    message = "Se ha eliminado un usuario"

                except pymysql.err.MySQLError as error:
                    print(
                        "Failed inserting BLOB data into MySQL table {}".format(error)
                    )
                    message = "No se puede eliminar. Afecta la integridad de los datos"
                    data = logic.getAllEmprendedores()
                    for registro in data:
                        usuario = uLogic.getUserById(registro["id_usuario"])
                        userName = usuario.user
                        registro["id_usuario"] = userName

                return render_template(
                    "emprendedorAdmin.html", data=data, message=message
                )
            # Va al form para dar update
            elif formId == 3:
                id = int(request.form["id"])
                nombre = request.form["nombre"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                userName = request.form["id_usuario"]
                pais = request.form["pais"]
                ciudad = request.form["ciudad"]
                biografia = request.form["biografia"]
                return render_template(
                    "emprendedorAdmin.html",
                    data=data,
                    message=message,
                    verdadero=True,
                    id=id,
                    nombre=nombre,
                    email=email,
                    telefono=telefono,
                    userName=userName,
                    pais=pais,
                    ciudad=ciudad,
                    biografia=biografia,
                )
            # Modifica una categoria
            else:
                id = int(request.form["id"])
                nombre = request.form["nombre"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                userName = request.form["userName"]
                pais = request.form["pais"]
                ciudad = request.form["ciudad"]
                biografia = request.form["biografia"]
                foto = request.files["fileToUpload"]
                nombre_foto = foto.filename
                # try:
                usuario = uLogic.getUserByUser(userName)
                id_usuario = usuario.id
                if foto.filename == "":
                    logic.updateEmprendedorbyIdUsuario(
                        id_usuario, nombre, email, telefono, pais, ciudad, biografia,
                    )
                else:
                    binary_foto = foto.read()
                    logic.updateEmprendedorbyIdUsuarioWithPhoto(
                        id_usuario,
                        nombre,
                        email,
                        telefono,
                        pais,
                        ciudad,
                        biografia,
                        binary_foto,
                    )
                message = "Se ha modificado con éxito"
                data = logic.getAllEmprendedores()
                for registro in data:
                    usuario = uLogic.getUserById(registro["id_usuario"])
                    userName = usuario.user
                    registro["id_usuario"] = userName

                # except mysql.connector.Error and TypeError as error:
                #   print("Failed inserting BLOB data into MySQL table {}".format(error))
                #  message = "No se puede modificar. No existe el usuario"

                return render_template(
                    "emprendedorAdmin.html", verdadero=False, data=data, message=message
                )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
@admin.route("/productosAdmin", methods=["POST", "GET"])
def productos():
    try:
        user = session["user"]
        logic = adminLogic()
        datos = logic.getAllEmprendimientoID()
        if request.method == "GET":
            return render_template("productosAdmin.html", datosx=datos, mostrar=False)

        elif request.method == "POST":
            if request.form.get("formId"):
                formId = int(request.form["formId"])
                # Mostrar productos de un determinado emprendimiento
                if formId == 1:
                    id_Empren = request.form["id"]
                    Empren_Name = request.form["name"]
                    logicProductos = productoLogic()
                    productos = logicProductos.getAllProductosByIdEmprendimiento(
                        id_Empren
                    )
                    datos = logic.getAllEmprendimientoID()
                    return render_template(
                        "productosAdmin.html",
                        prductos=True,
                        datos=productos,
                        name=Empren_Name,
                        datosx=datos,
                        idEmpren=id_Empren,
                    )
                # Insertar
                if formId == 2:
                    nombre = request.form["nombre"]
                    foto = request.files["fileToUpload"]
                    descripcion = request.form["descripcion"]
                    costoUnitario = request.form["costoUnitario"]
                    precioVenta = request.form["precioVenta"]
                    patente = request.form["patente"]
                    nombre_foto = foto.filename
                    id_Empren = request.form["idEmpren"]
                    logicProductos = productoLogic()

                    if foto.filename == "":
                        nombre_foto = "products.png"
                        logicProductos.insertNewProductoWithoutPhoto(
                            nombre,
                            nombre_foto,
                            descripcion,
                            costoUnitario,
                            precioVenta,
                            patente,
                            id_Empren,
                        )
                    else:
                        binary_foto = foto.read()
                        logicProductos.insertNewProducto(
                            nombre,
                            binary_foto,
                            descripcion,
                            costoUnitario,
                            precioVenta,
                            patente,
                            id_Empren,
                        )
                    Empren_Name = request.form["name"]
                    productos = logicProductos.getAllProductosByIdEmprendimiento(
                        id_Empren
                    )
                    datos = logic.getAllEmprendimientoID()
                    return render_template(
                        "productosAdmin.html",
                        prductos=True,
                        datos=productos,
                        name=Empren_Name,
                        datosx=datos,
                        idEmpren=id_Empren,
                        message="Se ha insertado el producto",
                    )

                # Delete
                if formId == 3:
                    id_producto = request.form["id"]
                    logicProductos = productoLogic()
                    logicProductos.deleteProducto(id_producto)
                    id_Empren = request.form["idEmpren"]
                    Empren_Name = request.form["name"]
                    logicProductos = productoLogic()
                    productos = logicProductos.getAllProductosByIdEmprendimiento(
                        id_Empren
                    )
                    datos = logic.getAllEmprendimientoID()
                    return render_template(
                        "productosAdmin.html",
                        prductos=True,
                        datos=productos,
                        name=Empren_Name,
                        datosx=datos,
                        idEmpren=id_Empren,
                        message="Se ha eliminado el producto",
                    )
                # Mando al form de modificacion
                if formId == 4:
                    nombre = request.form["nombre"]
                    nombre_foto = request.form["nombre_foto"]
                    descripcion = request.form["descripcion"]
                    costoUnitario = float(request.form["costoUnitario"])
                    precioVenta = float(request.form["precioVenta"])
                    patente = request.form["patente"]
                    id_producto = int(request.form["id_producto"])
                    data2 = {
                        "id_producto": id_producto,
                        "nombre": nombre,
                        "nombre_foto": nombre_foto,
                        "descripcion": descripcion,
                        "costo_unitario": costoUnitario,
                        "precio_venta": precioVenta,
                        "patente": patente,
                    }
                    id_Empren = request.form["idEmpren"]
                    Empren_Name = request.form["name"]
                    logicProductos = productoLogic()
                    productos = logicProductos.getAllProductosByIdEmprendimiento(
                        id_Empren
                    )
                    datos = logic.getAllEmprendimientoID()
                    return render_template(
                        "productosAdmin.html",
                        prductos=True,
                        datos=productos,
                        name=Empren_Name,
                        datosx=datos,
                        data2=data2,
                        mostrar=True,
                        idEmpren=id_Empren,
                    )
                # Modifica el producto
                if formId == 5:
                    nombre = request.form["nombre"]
                    foto = request.files["fileToUpload"]
                    descripcion = request.form["descripcion"]
                    costoUnitario = float(request.form["costoUnitario"])
                    precioVenta = float(request.form["precioVenta"])
                    patente = request.form["patente"]
                    id_producto = int(request.form["id_producto"])
                    nombre_foto = foto.filename
                    logicProductos = productoLogic()
                    if foto.filename == "":
                        logicProductos.updateProductoWithoutPhoto(
                            id_producto,
                            nombre,
                            descripcion,
                            costoUnitario,
                            precioVenta,
                            patente,
                        )
                    else:
                        binary_foto = foto.read()
                        logicProductos.updateProducto(
                            id_producto,
                            nombre,
                            binary_foto,
                            descripcion,
                            costoUnitario,
                            precioVenta,
                            patente,
                        )
                    id_Empren = request.form["idEmpren"]
                    Empren_Name = request.form["name"]
                    productos = logicProductos.getAllProductosByIdEmprendimiento(
                        id_Empren
                    )
                    datos = logic.getAllEmprendimientoID()
                    return render_template(
                        "productosAdmin.html",
                        prductos=True,
                        datos=productos,
                        name=Empren_Name,
                        datosx=datos,
                        idEmpren=id_Empren,
                        message="Se ha modificado el producto",
                    )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
@admin.route("/fundadoresAdmin", methods=["GET", "POST"])
def fundadores():
    try:
        user = session["user"]
        logic = adminLogic()
        verdadero = False
        if request.method == "GET":
            data = logic.getAllFundadores()
            message = ""
            return render_template("fundadoresAdmin.html", data=data, message=message)
        elif request.method == "POST":
            formId = int(request.form["formId"])
            # INSERTAR
            if formId == 1:
                user = request.form["user"]
                emprendimiento = request.form["name"]
                rol = 3
                logicUsuario = UserLogic()
                logicEmpre = adminLogic()
                # Comprobando si existe
                existeUsuario = logicUsuario.checkUserInUsuario(user, rol)
                existeEmprendimiento = logicEmpre.checkEmprendimiento(emprendimiento)

                if existeUsuario and existeEmprendimiento:
                    # Compruebo si no lo habian registrado antes en el mismo emprendimiento
                    logicRegist = emprendimientoLogic()
                    idEmprendimiento = logicEmpre.getEmprendimientoByName(
                        emprendimiento
                    )
                    AlreadyExist = logicRegist.checkUserAlredyExist(
                        user, idEmprendimiento.getId()
                    )
                    if AlreadyExist is False:
                        rows = logic.insertNewFundadorByName(user, emprendimiento)
                        data = logic.getAllFundadores()
                        message = "Se ha agregado al fundador"
                        return render_template(
                            "fundadoresAdmin.html", data=data, message=message
                        )
                    else:
                        data = logic.getAllFundadores()
                        message = (
                            "El usuario ya se encuentra asignado a este emprendimiento."
                        )
                        return render_template(
                            "fundadoresAdmin.html", data=data, massage=message
                        )
                else:
                    data = logic.getAllFundadores()
                    message = "El usuario o emprendimiento seleccionado no existe. Pruebe de nuevo"
                    return render_template(
                        "fundadoresAdmin.html", data=data, message=message
                    )
            # ELIMINAR
            elif formId == 2:
                id = int(request.form["id"])
                logicDelete = emprendimientoLogic()
                logicDelete.deleteFundador(id)
                message = "Se ha eliminado un fundador"
                data = logic.getAllFundadores()
                return render_template(
                    "fundadoresAdmin.html", data=data, message=message
                )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
@admin.route("/EmprendimientoAdmin", methods=["GET", "POST"])
def signUPEmprendimiento():
    try:
        user = session["user"]
        logic = emprendimientoLogic()
        message = ""
        verdadero = False
        logicUser = UserLogic()
        categorias = CategoriaLogic().getAllCategorias()
        if request.method == "GET":
            data = logic.getAllEmprendimientoLen()
            return render_template(
                "emprendimientoAdmin.html",
                data=data,
                message=message,
                categorias=categorias,
            )

        elif request.method == "POST":  # "POST"
            formId = int(request.form["formId"])
            message = ""
            # Inserta una emprendimiento
            if formId == 1:
                estado = str(request.form["estado"])
                descripcion = request.form["descripcion"]
                historia = str(request.form["historia"])
                eslogan = request.form["eslogan"]
                inversion_inicial = request.form["inversion_inicial"]
                fecha_fundacion = request.form["fecha_fundacion"]
                venta_año_anterior = request.form["venta_año_anterior"]
                user_emprendedor = request.form["user_emprendedor"]
                nombre = request.form["nombre"]
                foto = request.files["fileToUpload"]
                nombre_foto = foto.filename
                video = request.form["video"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                facebook = request.form["facebook"]
                instagram = request.form["instagram"]
                youtube = request.form["youtube"]

                if logicUser.checkUserInUsuario(user_emprendedor, 3):
                    id_emprendedor = logic.getIdEmprendedorByUser(user_emprendedor)
                    try:
                        if foto.filename == "":
                            nombre_foto = "default.png"

                            logic.insertNewEmprendimientoWithoutPhoto(
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
                            logic.insertNewEmprendimiento(
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
                        message = "Se ha insertado un nuevo emprendimiento"

                        id_emprendimiento = logic.getNewIdEmprendimiento(
                            nombre, eslogan, fecha_fundacion
                        )

                        for checkbox in categorias:
                            id_categoria = checkbox["id"]
                            value = request.form.get(str(id_categoria))
                            if value:
                                logic.insertEspecialidad(
                                    id_emprendimiento, id_categoria
                                )

                        data = logic.getAllEmprendimientoLen()

                        return render_template(
                            "emprendimientoAdmin.html",
                            data=data,
                            message=message,
                            categorias=categorias,
                        )

                    except pymysql.err.MySQLError as error:
                        print(
                            "Failed inserting BLOB data into MySQL table {}".format(
                                error
                            )
                        )
                        message = "No se puede insertar. No existe el id emprendedor"
                        data = logic.getAllEmprendimientoLen()

                    return render_template(
                        "emprendimientoAdmin.html",
                        data=data,
                        message=message,
                        categorias=categorias,
                    )
                else:
                    message = "No se puede insertar. No existe el usario ingersado o no es emprendedor"
                    data = logic.getAllEmprendimientoLen()
                    return render_template(
                        "emprendimientoAdmin.html",
                        data=data,
                        message=message,
                        categorias=categorias,
                    )

            # Elimina un emprendimiento
            elif formId == 2:
                id = int(request.form["id"])

                try:
                    logic.deleteEmprendimientoByIdEmprendimiento(id)
                    message = "Se ha eliminado el emprendimiento"
                    data = logic.getAllEmprendimientoLen()

                except pymysql.err.MySQLError as error:
                    print(
                        "Failed inserting BLOB data into MySQL table {}".format(error)
                    )
                    message = "No se puede eliminar. Afecta la integridad de los datos"
                    data = logic.getAllEmprendimientoLen()
                return render_template(
                    "emprendimientoAdmin.html",
                    data=data,
                    message=message,
                    categorias=categorias,
                )
            # Va al form para dar update
            elif formId == 3:
                id = int(request.form["id"])
                estado = str(request.form["estado"])
                descripcion = request.form["descripcion"]
                historia = str(request.form["historia"])
                eslogan = request.form["eslogan"]
                inversion_inicial = request.form["inversion_inicial"]
                fecha_fundacion = request.form["fecha_fundacion"]
                venta_año_anterior = request.form["venta_año_anterior"]
                id_emprendedor = request.form["id_emprendedor"]
                nombre = request.form["nombre"]
                nombre_foto = request.form["nombre_foto"]
                video = request.form["video"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                facebook = request.form["facebook"]
                instagram = request.form["instagram"]
                youtube = request.form["youtube"]
                verdadero = True
                data = logic.getAllEmprendimientoLen()
                return render_template(
                    "emprendimientoAdmin.html",
                    data=data,
                    verdadero=verdadero,
                    id=id,
                    estado=estado,
                    descripcion=descripcion,
                    historia=historia,
                    eslogan=eslogan,
                    inversion_inicial=inversion_inicial,
                    fecha_fundacion=fecha_fundacion,
                    venta_año_anterior=venta_año_anterior,
                    id_emprendedor=id_emprendedor,
                    nombre=nombre,
                    nombre_foto=nombre_foto,
                    video=video,
                    email=email,
                    telefono=telefono,
                    facebook=facebook,
                    instagram=instagram,
                    youtube=youtube,
                    categorias=categorias,
                )

            # Modifica al emprendimiento
            else:
                id = int(request.form["id"])
                estado = str(request.form["estado"])
                descripcion = request.form["descripcion"]
                historia = str(request.form["historia"])
                eslogan = request.form["eslogan"]
                inversion_inicial = request.form["inversion_inicial"]
                fecha_fundacion = request.form["fecha_fundacion"]
                venta_año_anterior = request.form["venta_año_anterior"]
                nombre = request.form["nombre"]
                foto = request.files["fileToUpload"]
                video = request.form["video"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                facebook = request.form["facebook"]
                instagram = request.form["instagram"]
                youtube = request.form["youtube"]

                try:
                    if foto.filename == "":
                        nombre_foto = "default.png"
                        logic.updateEmprendimientoWitoutPhoto(
                            id,
                            estado,
                            descripcion,
                            historia,
                            eslogan,
                            inversion_inicial,
                            fecha_fundacion,
                            venta_año_anterior,
                            nombre,
                            video,
                            email,
                            telefono,
                            facebook,
                            instagram,
                            youtube,
                        )
                    else:
                        binary_foto = foto.read()
                        logic.updateEmprendimiento(
                            id,
                            estado,
                            descripcion,
                            historia,
                            eslogan,
                            inversion_inicial,
                            fecha_fundacion,
                            venta_año_anterior,
                            nombre,
                            binary_foto,
                            video,
                            email,
                            telefono,
                            facebook,
                            instagram,
                            youtube,
                        )
                    data = logic.getAllEmprendimientoLen()
                    message = "Se ha modificado el emprendimiento"

                except pymysql.err.MySQLError as error:
                    print(
                        "Failed inserting BLOB data into MySQL table {}".format(error)
                    )
                    message = "No se puede modificar. No existe el id emprendedor"
                    data = logic.getAllEmprendimientoLen()

                return render_template(
                    "emprendimientoAdmin.html",
                    data=data,
                    message=message,
                    categorias=categorias,
                )
    except KeyError:
        return render_template(
            "logInForm.html",
            messageSS="Su sesión ha expirado, ingrese nuevamente",
            categorias=categorias,
        )


# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
@admin.route("/categoriaAdmin", methods=["GET", "POST"])
def categoria():
    try:
        user = session["user"]
        logic = adminLogic()
        massage = ""
        verdadero = False
        if request.method == "GET":
            data = logic.getAllCategorias()
            return render_template("categoriaAdmin.html", data=data, massage=massage)
        elif request.method == "POST":
            formId = int(request.form["formId"])
            # Inserta una categoría
            if formId == 1:
                categoria = request.form["categoria"]
                existe = logic.checkCategoria(categoria)
                if existe:
                    massage = "La categoría ya existe. Inserte de nuevo"
                else:
                    logic.insertCategoria(categoria)
                    massage = "Se ha insertado una nueva categoría"
                data = logic.getAllCategorias()
                return render_template(
                    "categoriaAdmin.html", data=data, massage=massage
                )
            # Elimina una categoria
            elif formId == 2:
                id = int(request.form["id"])
                try:
                    logic.deleteCategoria(id)
                    massage = "Se ha eliminado una categoría"
                    data = logic.getAllCategorias()

                except pymysql.err.MySQLError as error:
                    print(
                        "Failed inserting BLOB data into MySQL table {}".format(error)
                    )
                    massage = "No se puede eliminar. Afecta la integridad de los datos"
                    data = logic.getAllCategorias()

                return render_template(
                    "categoriaAdmin.html", data=data, massage=massage
                )
            # Va al form para dar update
            elif formId == 3:
                id = int(request.form["id"])
                categoria = request.form["categoria"]
                print(categoria)
                verdadero = True
                data = logic.getAllCategorias()
                return render_template(
                    "categoriaAdmin.html",
                    data=data,
                    verdadero=verdadero,
                    categoria=categoria,
                    id=id,
                )
            # Modifica una categoria
            elif formId == 4:
                id = int(request.form["id"])
                categoria = request.form["categoria"]
                logic.updateCategoria(id, categoria)
                data = logic.getAllCategorias()
                massage = "Se ha modificado la categoría"
                return render_template(
                    "categoriaAdmin.html", data=data, verdadero=False, massage=massage
                )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
@admin.route("/agregarAdmin", methods=["GET", "POST"])
def agregarAdmin():
    try:
        user = session["user"]
        admin_user = user["usuario"]
        logic = adminLogic()
        message = ""
        verdadero = False
        data = logic.getAllAdmin()
        for registro in data:
            registro["borrar"] = False
            if registro["usuario"] == admin_user:
                registro["borrar"] = True
                break
        if request.method == "GET":
            data = logic.getAllAdmin()
            for registro in data:
                registro["borrar"] = False
                if registro["usuario"] == admin_user:
                    registro["borrar"] = True
                    break
            return render_template("agregarAdmin.html", data=data, message=message)
        elif request.method == "POST":
            data = logic.getAllAdmin()
            for registro in data:
                registro["borrar"] = False
                if registro["usuario"] == admin_user:
                    registro["borrar"] = True
                    break
            formId = int(request.form["formId"])
            # INSERTAR
            if formId == 1:
                usuario = request.form["usuario"]
                password = request.form["password"]
                rol = 1
                verdadero = False
                logicUsuario = UserLogic()
                logic = adminLogic()
                # Comprobando si existe
                existeUsuario = logicUsuario.checkUserInUsuario(usuario, rol)

                if not existeUsuario:
                    rows = logic.insertAdmin(usuario, password)
                    message = "Se ha agregado un nuevo administrador"
                    data = logic.getAllAdmin()
                    for registro in data:
                        registro["borrar"] = False
                        if registro["usuario"] == admin_user:
                            registro["borrar"] = True
                            break
                    return render_template(
                        "agregarAdmin.html",
                        data=data,
                        message=message,
                        verdadero=verdadero,
                    )
                else:
                    message = "El usuario ya existe, pruebe otro"
                    data = logic.getAllAdmin()
                    for registro in data:
                        registro["borrar"] = False
                        if registro["usuario"] == admin_user:
                            registro["borrar"] = True
                            break
                    return render_template(
                        "agregarAdmin.html",
                        data=data,
                        message=message,
                        verdadero=verdadero,
                    )
            # ELIMINAR
            elif formId == 2:
                id = int(request.form["id"])
                logic.deleteAdmin(id)
                message2 = "Se ha eliminado un administrador"
                data = logic.getAllAdmin()
                for registro in data:
                    registro["borrar"] = False
                    if registro["usuario"] == admin_user:
                        registro["borrar"] = True
                        break
                return render_template(
                    "agregarAdmin.html", data=data, message2=message2
                )
            # form para dar update
            elif formId == 3:
                logic = adminLogic()
                verdadero = True
                id = int(request.form["id"])
                usuario = request.form["usuario"]
                password = request.form["password"]
                data = logic.getAllAdmin()
                for registro in data:
                    registro["borrar"] = False
                    if registro["usuario"] == admin_user:
                        registro["borrar"] = True
                        break
                return render_template(
                    "agregarAdmin.html",
                    usuario=usuario,
                    password=password,
                    data=data,
                    verdadero=verdadero,
                    id=id,
                )
            # UPDATE
            elif formId == 4:
                logic = adminLogic()
                id = int(request.form["id"])
                usuario = request.form["usuario"]
                password = request.form["password"]
                rol = 1
                logicUsuario = UserLogic()
                logic.updateAdmin(id, usuario, password)
                message2 = "Se ha modificado al administrador"
                data = logic.getAllAdmin()
                for registro in data:
                    registro["borrar"] = False
                    if registro["usuario"] == admin_user:
                        registro["borrar"] = True
                        break
                return render_template(
                    "agregarAdmin.html", data=data, message2=message2
                )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )
