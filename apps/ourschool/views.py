
#=====================================================================================================================
#        IMPORTACIONES
#====================================================================================================================

from django.urls import reverse
from django.core.mail import BadHeaderError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .models import Usuario, Animal, EventoAnimal
from django.contrib import messages
from django.db.models import Q


#=====================================================================================================================
#        VISTAS CRUD 
#=====================================================================================================================

def inicio(request):
    return render(request, 'ourschool/inicio.html')

def registrarse(request):
    return render(request, 'ourschool/registrarse.html')

def inicio_profesor(request):
   
    return render(request, 'ourschool/inicio_profesor.html')

def inicio_estudiante(request):
    return render(request, 'ourschool/inicio_estudiante.html')

def iniciar(request):
    email = None
    clave = None

    if request.method == "POST":
        email = request.POST.get("correo")
        clave = request.POST.get("contrasena")

    try:
        usuario = Usuario.objects.get(correo=email, contrasena=clave)
        messages.success(request, "Bienvenido!")

        request.session['logueo'] = {'rol': usuario.rol,'correo':usuario.correo}
        if usuario.rol == 2:
            return render(request, 'ourschool/inicio_estudiante.html')
        elif usuario.rol == 3:
            return render(request, 'ourschool/inicio_estudiante.html')
        elif usuario.rol == 1:
            return redirect('lista_usuarios')
        else:
            messages.error(request, "Rol no válido")

    except Usuario.DoesNotExist:
        messages.error(request, "Usuario o contraseña no válidos")
        return render(request, 'ourschool/iniciar.html')

def cerrar_session(request):
    try:
        del request.session['logueo']
        messages.success(request, 'Sesión cerrada correctamente')
        return redirect('inicio')

    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('inicio')  # O redirige a la página que consideres apropiada en caso de error
    

def registro(request):
    if request.method == "POST":
        # Obtener datos del formulario
        nom_ape = request.POST.get('nombre_apellido')
        tipo_doc = request.POST.get('tipo_documento')
        num_doc = request.POST.get('numero_documento')
        tel = request.POST.get('telefono')
        cor = request.POST.get('correo')
        fec_nac = request.POST.get('fecha_nacimiento')
        contr = request.POST.get('contrasena')
        r = request.POST.get('rol')

        try:
            # Crear un nuevo objeto Usuario
            nuevo_usuario = Usuario(
                nombre_apellido=nom_ape,
                tipo_documento=tipo_doc,
                numero_documento=num_doc,
                telefono=tel,
                correo=cor,
                fecha_nacimiento=fec_nac,
                contrasena=contr,
                rol=r
            )

            # Validar el objeto
            nuevo_usuario.full_clean()

            # Guardar el objeto en la base de datos
            nuevo_usuario.save()

            messages.success(request, 'Se guardó correctamente')
            return redirect('iniciar')

        except ValidationError as e:
            messages.warning(request, f'Error: {e}')

    return HttpResponseRedirect(reverse('inicio'))




def eliminar_usuario(request, correo):
    if request.method == 'GET':
        usuario = get_object_or_404(Usuario, correo=correo)
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('lista_usuarios')  
    else:
        return redirect('lista_usuarios')  

def admin_editar_formulario(request, correo):
    q = Usuario.objects.get(correo=correo)
    contexto = {"id": correo, "data": q}
    return render(request, 'ourschool/perfil.html', contexto)

def perfil(request):
    usuario = request.session.get("logueo", False)
    q = Usuario.objects.get(correo=usuario['correo'])
    contexto = {"data": q}
    return render(request, "ourschool/perfil.html", contexto)

def guardar_cambios_usuario(request, correo):
    if request.method == "POST":
        usuario = Usuario.objects.get(correo=correo)
        # Actualizar los campos del usuario con los datos del formulario
        usuario.nombre_apellido = request.POST.get('nombre_apellido')
        usuario.correo = request.POST.get('correo')
        usuario.contrasena = request.POST.get('contrasena')
        usuario.telefono = request.POST.get('telefono')
        # Guardar los cambios en la base de datos
        usuario.save()
        return redirect('inicio_estudiante')  # Redirigir a la página de perfil o a donde desees
    else:
        # Manejar el caso en el que no se haya enviado un formulario
        return redirect('inicio_estudiante')  # Redirigir a la página de perfil o a donde desees






#==========================================================================================================================================
#        OTRAS FUNCIONES 
#===================================================================================================================================================================

def lista_usuarios(request):
    # Obtener datos de la base de datos
    data = Usuario.objects.all()

    # Pasar los datos a la plantilla
    return render(request, 'ourschool/inicio_estudiante.html', {'data': data})


def guardar(request):
    if request.method == "POST":
        id = request.POST.get("id")
        nomb = request.POST.get("nombre")
        desc = request.POST.get("descripcion")

        if id == "":
            # crear
            try:
                cat = Categoria(
                    nombre=nomb,
                    descripcion=desc
                )
                cat.save()
                messages.success(request, "Guardado correctamente!!")
            except Exception as e:
                messages.error(request, f"Error. {e}")
        else:
            # actualizar
            try:
                q = Categoria.objects.get(pk=id)
                q.nombre = nomb
                q.descripcion = desc
                q.save()
                messages.success(request, "Actualizado correctamente!!")
            except Exception as e:
                messages.error(request, f"Error. {e}")

        return HttpResponseRedirect(reverse("tienda:listar_categorias", args=()))
    else:
        messages.warning(request, "No se enviaron datos...")
        return HttpResponseRedirect(reverse("tienda:form_cat", args=()))

def recuperar_contrasena(request):
    return PasswordResetView.as_view(
        template_name='ourschool/correo.html',
        email_template_name='ourschool/correo.html',
        success_url='/password_reset/done/',
    )(request)

def correo(request):
    if request.method == 'POST':
        destinatario = request.POST.get('email')  # Obtener el correo electrónico del formulario
        mensaje = """
            <h1 style='color:blue;'>CowDB</h1>
            <h3 style='color:black;'>Su solicitud ha sido tomada correctamente, un administrador se comunicará con usted para restablecer su contraseña</h3>
            <h1 style='color:black;'>2025</h1>
            """

        try:
            msg = EmailMessage("Tienda ADSO", mensaje, settings.EMAIL_HOST_USER, [destinatario])
            msg.content_subtype = "html"  # Habilitar html
            msg.send()
            return redirect('password_reset_done')
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    else:
        # Si no es una solicitud POST, redirigir o mostrar un mensaje de error adecuado
        return HttpResponse("Método no permitido")







#===========================================================================================================================================
#        INTEGRACION CowDB 
#============================================================================================================================================




# ---------------------------------------------------
#   CRUD animales
# ---------------------------------------------------
def mis_animales(request):
    if 'logueo' not in request.session:
        return redirect('iniciar')

    correo = request.session['logueo']['correo']
    usuario = get_object_or_404(Usuario, correo=correo)

    # Obtener el parámetro del buscador
    query = request.GET.get("q", "")

    # Filtrar animales solo del usuario
    animales = Animal.objects.filter(dueño=usuario)

    # Si hay búsqueda, filtrar por nombre, código o ID
    if query:
        animales = animales.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(id__icontains=query)
        )

    return render(request, "ourschool/mis_animales.html", {
        "animales": animales,
        "query": query
    })


# ---------------------------------------------------
#   CREAR ANIMAL
# ---------------------------------------------------
def crear_animal(request):
    if 'logueo' not in request.session:
        return redirect('iniciar')

    correo = request.session['logueo']['correo']
    usuario = get_object_or_404(Usuario, correo=correo)

    if request.method == "POST":
        codigo = request.POST.get("codigo")
        nombre = request.POST.get("nombre")
        foto = request.FILES.get("foto")

        if not codigo or not nombre:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("crear_animal")

        Animal.objects.create(
            dueño=usuario,
            codigo=codigo,
            nombre=nombre,
            foto=foto
        )

        messages.success(request, "Animal registrado correctamente.")
        return redirect("mis_animales")

    return render(request, "ourschool/crear_animal.html")


# ---------------------------------------------------
#   EDITAR ANIMAL
# ---------------------------------------------------
def editar_animal(request, animal_id):
    if 'logueo' not in request.session:
        return redirect('iniciar')

    animal = get_object_or_404(Animal, id=animal_id)

    if request.method == "POST":
        animal.codigo = request.POST.get("codigo")
        animal.nombre = request.POST.get("nombre")

        if request.FILES.get("foto"):
            animal.foto = request.FILES.get("foto")

        animal.save()
        messages.success(request, "Animal actualizado correctamente.")
        return redirect("mis_animales")

    return render(request, "ourschool/editar_animal.html", {
        "animal": animal
    })


# ---------------------------------------------------
#   ELIMINAR ANIMAL
# ---------------------------------------------------
def eliminar_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    animal.delete()
    messages.success(request, "Animal eliminado.")
    return redirect("mis_animales")



# ---------------------------------------------------
#   eventos animales 
# ---------------------------------------------------


def agregar_evento(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        fecha = request.POST.get("fecha")
        descripcion = request.POST.get("descripcion") 

        EventoAnimal.objects.create(
            animal=animal,
            tipo=tipo,
            fecha=fecha,
            descripcion=descripcion
        )

        return redirect("detalle_animal", animal.id)

    return render(request, "ourschool/agregar_evento.html", {
        "animal": animal
    })

def detalle_animal(request, animal_id):
    if 'logueo' not in request.session:
        return redirect('iniciar')

    animal = Animal.objects.get(id=animal_id)
    eventos = EventoAnimal.objects.filter(animal=animal).order_by('-fecha')

    return render(request, "ourschool/detalle_animal.html", {
        "animal": animal,
        "eventos": eventos
    })



def editar_evento(request, evento_id):
    evento = EventoAnimal.objects.get(id=evento_id)
    animal = evento.animal  # para redirigir después

    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect("detalle_animal", animal.id)
    else:
        form = EventoForm(instance=evento)

    return render(request, "ourschool/editar_evento.html", {"form": form, "evento": evento})



def eliminar_evento(request, evento_id):
    evento = EventoAnimal.objects.get(id=evento_id)
    animal_id = evento.animal.id
    evento.delete()
    return redirect("detalle_animal", animal_id)
