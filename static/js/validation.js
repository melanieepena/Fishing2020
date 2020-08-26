$(function () {

  $.validator.setDefaults({
    errorClass: 'help-block',
    highlight: function (element) {
      $(element)
        .closest('.form-group')
        .addClass('has-error');
    },
    unhighlight: function (element) {
      $(element)
        .closest('.form-group')
        .removeClass('has-error');
    },
    errorPlacement: function (error, element) {
      if (element.prop('type') === 'checkbox') {
        error.insertAfter(element.parent());
      } else {
        error.insertAfter(element);
      }
    }
  });
  jQuery.validator.addMethod("letterswithspace", function (value, element) {
    return this.optional(element) || /^[a-z\s]+$/i.test(value);
  }, "letters only");


  $("form[name='formId']").validate({
    rules: {
      email: {
        required: true,
        email: true,
        maxlength: 150
      },
      nombre: {
        required: true,
        letterswithspace: true,
        maxlength: 100
      },
      pais: {
        required: true,
        letterswithspace: true,
        maxlength: 100
      },
      telefono: {
        required: true,
        digits: true,
        maxlength: 25
      },
      biografia: {
        required: true,
        maxlength: 500
      },
      ciudad: {
        required: true,
        letterswithspace: true,
        maxlength: 100
      }

    },
    messages: {

      email: {
        required: 'Por favor, ingrese un correo',
        email: 'Por favor, ingrese un correo válido',
        maxlength: 'Por favor, no ingrese más de 150 caracteres'
      },
      nombre: {
        required: 'Por favor, ingrese un nombre',
        letterswithspace: 'Por favor, utilice solo letras',
        maxlength: 'Por favor, no ingrese más de 100 caracteres'
      },
      pais: {
        required: 'Por favor, ingrese su país',
        letterswithspace: 'Por favor, revise que solo contenga letras',
        maxlength: 'Por favor, no ingrese más de 100 caracteres'

      },
      ciudad: {
        required: 'Por favor, ingrese su ciudad',
        letterswithspace: 'Por favor, revise que solo contenga letras',
        maxlength: 'Por favor, no ingrese más de 100 caracteres'

      },
      telefono: {
        required: 'Por favor, ingrese su numero de telefono',
        digits: 'Por favor, revise que solo contenga números',
        maxlength: 'Por favor, no ingrese más de 25 caracteres'

      },
      biografia: {
        required: 'Por favor, ingrese su biografía',
        maxlength: 'Por favor, no ingrese más de 500 caracteres'
      }
    }

  });
  $("form[name='formIdInv']").validate({
    rules: {
      email: {
        required: true,
        email: true,
        maxlength: 150
      },

      nombre: {
        required: true,
        letterswithspace: true,
        maxlength: 100
      },
      pais: {
        required: true,
        letterswithspace: true,
        maxlength: 100
      },
      biografia: {
        required: true,
        maxLength: 200
      },
      ciudad: {
        required: true,
        letterswithspace: true,
        maxlength: 100

      },

    },
    messages: {

      email: {
        required: 'Por favor, ingrese un correo',
        email: 'Por favor, ingrese un correo válido',
        maxlength: 'Por favor, no ingrese más de 150 caracteres'

      },
      nombre: {
        required: 'Por favor, ingrese un nombre',
        letterswithspace: 'Por favor, revise que solo contenga letras',
        maxlength: 'Por favor, no ingrese más de 100 caracteres'
      },
      pais: {
        required: 'Por favor, ingrese su país',
        letterswithspace: 'Por favor, revise que solo contenga letras',
        maxlength: 'Por favor, no ingrese más de 100 caracteres'

      },
      ciudad: {
        required: 'Por favor, ingrese su ciudad',
        letterswithspace: 'Por favor, revise que solo contenga letras',
        maxlength: 'Por favor, no ingrese más de 100 caracteres'
      },
      biografia: {
        required: 'Por favor, ingrese su biografia',
        maxLength: 'Por favor, revise que su biografía no exceda 200 caracteres'
formId
      }
    }

  });
  $("form[name='crearEmp']").validate({
    rules: {
      estado: {
        required: true,
      },
      descripcion: {
        required: true,
        maxLength: 500
      },
      historia: {
        required: true,
        maxLength: 500
      },
      eslogan: {
        required: true,
        maxlength: 500
      },
      inversion_inicial: {
        required: true,
        number: true,

      },
      venta_año_anterior: {
        required: true,
        number: true,
      },
      oferta_porcentaje: {
        required: true,
        number: true,
        range: [0, 100]
      },
      fecha_fundacion: {
        required: true,
      },
      email: {
        required: true,
        email: true,
        maxlength: 150

      },

      nombre: {
        required: true,
        letterswithspace: true,
        maxlength: 100

      },
      telefono: {
        required: true,
        digits: true,
        maxlength: 25
      }

    },
    messages: {

      email: {
        required: 'Por favor, ingrese un correo',
        email: 'Por favor, ingrese un correo válido',
        maxLength: 'Por favor, revise que no exceda 150 caracteres'

      },
      descripcion: {
        required: 'Por favor, ingrese la descripción de su emprendimiento',
        maxLength: 'Por favor, no exeda 500 palabaras'
      },
      historia: {
        required: 'Por favor, ingrese la descripción de su emprendimiento',
        maxLength: 'Por favor, no exeda 500 palabaras'
      },
      eslogan: {
        required: 'Por favor, ingrese su eslogan',
        maxLength: 'Por favor, no exceda 500 caracteres'
      },
      fecha_fundacion: {
        required: 'Por favor, la fecha de fundación'
      },
      inversion_inicial: {
        required: 'Por favor, ingrese la inversión inicial',
        number: 'Por favor, revise que solo contenga números'

      },
      venta_año_anterior: {
        required: 'Por favor, ingrese la venta del año anterior',
        number: 'Por favor, revise que solo contenga números'

      },
      oferta_porcentaje: {
        required: 'Por favor, ingrese la oferta ej: 20',
        number: 'Por favor, revise que solo contenga números',
        range: 'Por favor, revise que su porcentaje este entre 0 y 100'

      },
      nombre: {
        required: 'Por favor, ingrese el nombre de su emprendimiento',
        letterswithspace: 'Por favor, revise que solo contenga letras',
        maxLength: 'Por favor,  no exceda 100 caracteres'
      },
      telefono: {
        required: 'Por favor, ingrese su numero de telefonos',
        digits: 'Por favor, revise que solo contenga números',
        maxlength: 'Por favor, no ingrese más de 25 caracteres'

      }
    }
  });

  $("form[name='formIdInicioEmp']").validate({
    rules: {
      nombre: {
        required: true,
        letterswithspace: true,
        maxlength: 100

      },
      eslogan: {
        required: true,
        maxlength: 500
      },
      descripcion: {
        required: true,
        maxLength: 500
      }
    },
    messages: {

      descripcion: {
        required: 'Por favor, ingrese la descripción de su emprendimiento',
        maxLength: 'Por favor, no exeda 500 palabaras'
      },
      eslogan: {
        required: 'Por favor, ingrese su eslogan',
        maxLength: 'Por favor, no exeda 500 palabaras'
      },
      nombre: {
        required: 'Por favor, ingrese el nombre de su emprendimiento',
        letterswithspace: 'Por favor, revise que solo contenga letras',
        maxLength: 'Por favor, no exeda 100 palabaras'
      }
    }

  });

  $("form[name='nuevoProducto']").validate({
    rules: {
      nombre: {
        required: true,
        letterswithspace: true,
        maxLength: 100
      },
      descripcion: {
        required: true,
        maxLength: 300
      },
      costoUnitario: {
        required: true,
        number: true
      },
      precioVenta: {
        required: true,
        number: true,

      },
      patente: {
        required: true,
        digits: true,
        maxLength: 20
      }
    },
    messages: {
      nombre: {
        required: 'Por favor, ingrese el nombre del producto',
        letterswithspace: 'Por favor, revise que solo contenga letras',
        maxLength: 'Por favor, no exeda 100 caracteres'
      },
      descripcion: {
        required: 'Por favor, ingrese la descripción del producto',
        maxLength: 'Por favor, no exeda 450 palabaras',
        maxLength: 'Por favor, no exeda 300 caracteres'
      },
      costoUnitario: {
        required: 'Por favor, ingrese el costo unitario del producto',
        number: 'Por favor, ingrese un número'
      },
      precioVenta: {
        required: 'Por favor, ingrese el costo unitario del producto',
        number: 'Por favor, ingrese un número'
      },
      patente: {
        required: 'Por favor, ingrese el costo unitario del producto',
        number: 'Por favor, ingrese un número',
        maxLength: 'Por favor, no exeda 20 caracteres'
      }
    }
  });
  $("form[name='modiProducto']").validate({
    rules: {
      nombre: {
        required: true,
        letterswithspace: true,
        maxLength: 100
      },
      descripcion: {
        required: true,
        maxLength: 300
      },
      costoUnitario: {
        required: true,
        number: true,
      },
      precioVenta: {
        required: true,
        number: true,
      },
      patente: {
        required: true,
        number: true,
        maxLength: 20
      }
    },
    messages: {
      nombre: {
        required: 'Por favor, ingrese el nombre de su emprendimiento',
        letterswithspace: 'Por favor, revise que solo contenga letras',
        maxLength: 'Por favor, no exeda 100 caracteres'
      },
      descripcion: {
        required: 'Por favor, ingrese la descripción de su emprendimiento',
        maxLength: 'Por favor, no exeda 450 palabaras',
        maxLength: 'Por favor, no exeda 300 caracteres'
      },
      costoUnitario: {
        required: 'Por favor, ingrese el costo unitario del producto',
        number: 'Por favor, ingrese un número'
      },
      precioVenta: {
        required: 'Por favor, ingrese el costo unitario del producto',
        number: 'Por favor, ingrese un número'
      },
      patente: {
        required: 'Por favor, ingrese el costo unitario del producto',
        number: 'Por favor, ingrese un número',
        maxLength: 'Por favor, no exeda 20 caracteres'
      }
    }
  });
  $("form[name='infoEMp']").validate({
    rules: {
      fecha_fundacionUP: {
        required: true,
      },
      inversion_inicialUP: {
        required: true,
        number: true
      },
      venta_año_anteriorUP: {
        required: true,
        number: true
      },
      oferta_porcentajeUP: {
        required: true,
        number: true,
        range: [0, 100]

      }
    },
    messages: {
      fecha_fundacionUP: {
        required: 'Por favor, ingrese una fecha'
      },
      inversion_inicialUP: {
        required: 'Por favor, ingrese la inversión inicial de su emprendimiento',
        number: 'Por favor, ingrese sólo números'
      },
      venta_año_anteriorUP: {
        required: 'Por favor, ingrese las ventas del año anterior',
        number: 'Por favor, ingrese sólo números'
      },
      oferta_porcentajeUP: {
        required: 'Por favor, ingrese la oferta',
        number: 'Por favor, ingrese sólo números',
        range: 'Por favor, revise que su porcentaje este entre 0 y 100'
      }
    }
  });

  $("form[name='modifContacto']").validate({
    rules: {
      emailUP: {
        required: true,
        email: true,
        maxLength: 100
      },
      telefonoUP: {
        required: true,
        digits: true,
        maxLength: 25
      }
    },
    messages: {
      emailUP: {
        required: 'Por favor, ingrese su email',
        email: 'Por favor, ingrese un email válido',
        maxLength: 'Por favor, no exeda 100 caracteres'
      },
      telefonoUP: {
        required: 'Por favor, ingrese su número telefónico',
        digits: 'Por favor, ingrese sólo números',
        maxLength: 'Por favor, no exeda 25 caracteres'
      },

    }
  });

  $("form[name='registroemp']").validate({
    rules: {
      nombre: {
        required: true,
        letterswithspace: true
      },
      bio: {
        required: true
      },
      email: {
        required: true,
        email: true
      },
      phone: {
        required: true,
        digits: true,
      },
      country: {
        required: true,
        letterswithspace: true
      },
      city: {
        required: true,
        letterswithspace: true
      }

    },
    messages: {
      nombre: {
        required: 'Por favor, ingrese su nombre',
        letterswithspace: 'Por favor, ingrese unicamente letras'
      },
      emailUP: {
        required: 'Por favor, ingrese su email',
        email: 'Por favor, ingrese un email válido'
      },
      telefonoUP: {
        required: 'Por favor, ingrese su número telefónico',
        digits: 'Por favor, ingrese sólo números'
      },

    }
  });

});