from flask import Blueprint, render_template, request, redirect, session
from productoLogic import productoLogic
from likeLogic import likeLogic
from userLogic import UserLogic
from userObj import UserObj
from emprendedorLogic import emprendedorLogic
from emprendedorObj import emprendedorObj
from emprendimientoLogic import emprendimientoLogic

registro_productos = Blueprint(
    "registro_productos", __name__, template_folder="Templates", static_folder="static"
)


@registro_productos.route("/registroProductosInv", methods=["GET", "POST"])
def registroProductoInv():
    try:
        logicProducto = productoLogic()
        logicEmprendimiento = emprendimientoLogic()
        logicLikes = likeLogic()
        id_emprendimiento = session["empId"]
        id_invrsionista = session["id_inv"]
        data = logicProducto.getAllProductosByIdEmprendimiento(id_emprendimiento)
        data3 = logicEmprendimiento.getDatosGeneralesById(id_emprendimiento)
        data2 = logicEmprendimiento.getDescripcion(id_emprendimiento)
        likes = logicLikes.getAllReaccionesByIdEmprendimiento(id_emprendimiento)

        if data3[0]["facebook"] == "":
            facebook = None
        else:
            facebook = data3[0]["facebook"]
        if data3[0]["instagram"] == "":
            instagram = None
        else:
            instagram = data3[0]["instagram"]
        if data3[0]["youtube"] == "":
            youtube = None
        else:
            youtube = data3[0]["youtube"]

        for registro in data:
            for fila in likes:
                registro["liked"] = False
                if (
                    registro["id"] == fila["id_producto"]
                    and fila["id_inversionista"] == id_invrsionista
                ):
                    registro["liked"] = True
                    break

        vistaEmprendimiento = True
        return render_template(
            "registroProductos.html",
            data=data,
            vistaEmprendimiento=vistaEmprendimiento,
            likes=likes,
            data3=data3,
            data2=data2,
            youtube=youtube,
            facebook=facebook,
            instagram=instagram,
        )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )


@registro_productos.route("/registroProductos", methods=["GET", "POST"])
def registroProducto():
    try:
        logicProducto = productoLogic()
        id_emprendimiento = session["emprendimiento"]
        mostrar = False
        data2 = None
        data = logicProducto.getAllProductosByIdEmprendimiento(id_emprendimiento)
        logicEmprendimiento = emprendimientoLogic()
        # Vista
        vistaEmprendimiento = True

        if request.method == "GET":
            # True para vista inversionista
            vistaEmprendimiento = False
            data2 = logicEmprendimiento.getDescripcion(id_emprendimiento)
            data3 = logicEmprendimiento.getDatosGeneralesById(id_emprendimiento)
            if data3[0]["facebook"] == "":
                facebook = None
            else:
                facebook = data3[0]["facebook"]
            if data3[0]["instagram"] == "":
                instagram = None
            else:
                instagram = data3[0]["instagram"]
            if data3[0]["youtube"] == "":
                youtube = None
            else:
                youtube = data3[0]["youtube"]

            return render_template(
                "registroProductos.html",
                data=data,
                data2=data2,
                data3=data3,
                vistaEmprendimiento=vistaEmprendimiento,
                youtube=youtube,
                facebook=facebook,
                instagram=instagram,
            )
        elif request.method == "POST":
            data3 = logicEmprendimiento.getDatosGeneralesById(id_emprendimiento)
            if data3[0]["facebook"] == "":
                facebook = None
            else:
                facebook = data3[0]["facebook"]
            if data3[0]["instagram"] == "":
                instagram = None
            else:
                instagram = data3[0]["instagram"]
            if data3[0]["youtube"] == "":
                youtube = None
            else:
                youtube = data3[0]["youtube"]

            formId = int(request.form["formId"])
            if formId == 1:
                nombre = request.form["nombre"]
                foto = request.files["fileToUpload"]
                descripcion = request.form["descripcion"]
                costoUnitario = request.form["costoUnitario"]
                precioVenta = request.form["precioVenta"]
                patente = request.form["patente"]
                nombre_foto = foto.filename

                if foto.filename == "":
                    nombre_foto = "products.png"
                    logicProducto.insertNewProductoWithoutPhoto(
                        nombre,
                        nombre_foto,
                        descripcion,
                        costoUnitario,
                        precioVenta,
                        patente,
                        id_emprendimiento,
                    )
                else:
                    binary_foto = foto.read()
                    logicProducto.insertNewProducto(
                        nombre,
                        binary_foto,
                        descripcion,
                        costoUnitario,
                        precioVenta,
                        patente,
                        id_emprendimiento,
                    )
                data = logicProducto.getAllProductosByIdEmprendimiento(
                    id_emprendimiento
                )

            # Elimina emprendimiento
            elif formId == 2:
                id_producto = request.form["id_producto"]
                logicProducto.deleteProducto(id_producto)
                data = logicProducto.getAllProductosByIdEmprendimiento(
                    id_emprendimiento
                )

            # Direcciona hacia el form de update
            elif formId == 3:
                mostrar = True
                nombre = request.form["nombre"]
                nombre_foto = request.form["nombre_foto"]
                descripcion = request.form["descripcion"]
                costoUnitario = float(request.form["costoUnitario"])
                precioVenta = float(request.form["precioVenta"])
                patente = int(request.form["patente"])
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

            # Modifica el producto
            elif formId == 4:
                nombre = request.form["nombre"]
                foto = request.files["fileToUpload"]
                descripcion = request.form["descripcion"]
                costoUnitario = float(request.form["costoUnitario"])
                precioVenta = float(request.form["precioVenta"])
                patente = int(request.form["patente"])
                id_producto = int(request.form["id_producto"])
                nombre_foto = foto.filename

                if foto.filename == "":
                    logicProducto.updateProductoWithoutPhoto(
                        id_producto,
                        nombre,
                        descripcion,
                        costoUnitario,
                        precioVenta,
                        patente,
                    )
                else:
                    binary_foto = foto.read()
                    logicProducto.updateProducto(
                        id_producto,
                        nombre,
                        binary_foto,
                        descripcion,
                        costoUnitario,
                        precioVenta,
                        patente,
                    )
                data = logicProducto.getAllProductosByIdEmprendimiento(
                    id_emprendimiento
                )

            return render_template(
                "registroProductos.html",
                data=data,
                mostrar=mostrar,
                data2=data2,
                youtube=youtube,
                facebook=facebook,
                instagram=instagram,
            )
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )
