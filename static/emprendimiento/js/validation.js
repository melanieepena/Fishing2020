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
        email: true

      },

      nombre: {
        required: true,
        lettersonly: false
        letterswithspace: true


      },
      pais: {
        required: true,
        letterswithspace: true

      },

      telefono: {
        required: true,
        digits: true,

      },
      biografia: {
        required: true

      },
      ciudad: {
        required: true,
        letterswithspace: true

      },

    },
    messages: {

      email: {
        required: 'Por favor, ingrese un correo',
        email: 'Por favor, ingrese un correo válido',

      },
      nombre: {
        required: 'Por favor, ingrese un nombre'
      },
      pais: {
        required: 'Por favor, ingrese su país',
        letterswithspace: 'Por favor, revise que solo contenga letras'

      },
      ciudad: {
        required: 'Por favor, ingrese su ciudad',
        letterswithspace: 'Por favor, revise que solo contenga letras'

      },
      telefono: {
        required: 'Por favor, ingrese su numero de telefono',
        digits: 'Por favor, revise que solo contenga números'

      },
      biografia: {
        required: 'Por favor, ingrese su numero de telefonos',

      }
    }

  });
  $("form[name='formIdInv']").validate({
    rules: {
      email: {
        required: true,
        email: true

      },

      nombre: {
        required: true,
        letterswithspace: false
      },
      pais: {
        required: true,
        letterswithspace: true

      },

      telefono: {
        required: true,
        digits: true,

      },
      biografia: {
        required: true
      },
      ciudad: {
        required: true,
        letterswithspace: true

      },

    },
    messages: {

      email: {
        required: 'Por favor, ingrese un correo',
        email: 'Por favor, ingrese un correo válido',

      },
      nombre: {
        required: 'Por favor, ingrese un nombre',
        letterswithspace: 'Por favor, revise que solo contenga letras'
      },
      pais: {
        required: 'Por favor, ingrese su país',
        letterswithspace: 'Por favor, revise que solo contenga letras'

      },
      ciudad: {
        required: 'Por favor, ingrese su ciudad',
        letterswithspace: 'Por favor, revise que solo contenga letras'

      },
      telefono: {
        required: 'Por favor, ingrese su numero de telefono',
        digits: 'Por favor, revise que solo contenga números'

      },
      biografia: {
        required: 'Por favor, ingrese su numero de telefonos',

      }
    }

  });
  $("form[name='crear']").validate({
    rules: {
      estado: {
        required: true,
      },
      descripcion: {
        required: true,
      },
      historia: {
        required: true,
      },
      eslogan: {
        required: true,
        letterswithspace: true
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
      },
      fecha_fundacion: {
        required: true,
      },
      email: {
        required: true,
        email: true

      },

      nombre: {
        required: true,

      },
      pais: {
        required: true,
        letterswithspace: true


      },

      telefono: {
        required: true,
        digits: true,

      },
      biografia: {
        required: true
      },
      ciudad: {
        required: true,
        letterswithspace: true

      },

    },
    messages: {

      email: {
        required: 'Por favor, ingrese un correo',
        email: 'Por favor, ingrese un correo válido',

      },
      historia: {
        required: 'Por favor, ingrese la historia de su emprendimiento'
      },
      descripcion: {
        required: 'Por favor, ingrese la descripción de su emprendimiento'
      },
      eslogan: {
        required: 'Por favor, ingrese su eslogan'
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
        number: 'Por favor, revise que solo contenga números'

      },
      nombre: {
        required: 'Por favor, ingrese el nombre de su emprendimiento'
      },
      pais: {
        required: 'Por favor, ingrese su país',
        lettersonly: 'Por favor, revise que solo contenga letras'

      },
      ciudad: {
        required: 'Por favor, ingrese su ciudad',
        letterswithspace: 'Por favor, revise que solo contenga letras'

      },
      telefono: {
        required: 'Por favor, ingrese su numero de telefonos',
        digits: 'Por favor, revise que solo contenga números'

      },
      biografia: {
        required: 'Por favor, ingrese su numero de telefonos',

      }
    }

  });

  $("form[name='formIdInicioEmp']").validate({
    rules: {
      nombre: {
        required: true,
        letterswithspace: true
      },
      eslogan: {
        required: true,
      },
      descripcion: {
        required: true,
      }
    },
    messages: {

      descripcion: {
        required: 'Por favor, ingrese la descripción de su emprendimiento'
      },
      eslogan: {
        required: 'Por favor, ingrese su eslogan'
      },
      nombre: {
        required: 'Por favor, ingrese el nombre de su emprendimiento'
      }
    }

  });

  $("form[name='nuevoProducto']").validate({
    rules: {
      nombre: {
        required: true,
      },
      descripcion: {
        required: true,
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
        digits: true,
      }
    },
    messages: {
      nombre: {
        required: 'Por favor, ingrese el nombre de su emprendimiento'
      },
      descripcion: {
        required: 'Por favor, ingrese la descripción de su emprendimiento'
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
        number: 'Por favor, ingrese un número'
      }
    }

  });

});