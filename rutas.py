from BD import conexion_cursor
from wsgi_app import Wsgiclass, render_template

app = Wsgiclass()


@app.ruta("/")
def inicio(request, response):
    html_respuesta = render_template("index.html")
    response.text = html_respuesta["text"]
    response.content_type = html_respuesta["type"]


@app.ruta("/profesores")
def home_page(request, response):
    search_query = request.GET.get("search", "").strip()
    cnx, curs = conexion_cursor(dictionary=True)

    if search_query:
        sql_query = (
            "SELECT idProfesor ID, nombreProfesor Nombre, mailProfesor Mail, celularProfesor Celular "
            "FROM profesores "
            "WHERE nombreProfesor LIKE %s"
        )
        curs.execute(sql_query, ("%" + search_query + "%",))
        data = curs.fetchall()

        if not data:
            no_results_message = "No se encontraron coincidencias"
        else:
            no_results_message = ""
    else:
        curs.execute(
            "SELECT idProfesor ID, nombreProfesor Nombre, mailProfesor Mail, celularProfesor Celular FROM profesores"
        )
        data = curs.fetchall()
        no_results_message = ""

    html_respuesta = render_template(
        "tablaProfesores.html",
        tabla=data,
        search_query=search_query,
        no_results_message=no_results_message,
    )
    response.text = html_respuesta["text"]
    response.content_type = html_respuesta["type"]


@app.ruta("/editar_profesor")
def editar_profesor(request, response):
    cnx, curs = conexion_cursor(dictionary=True)
    id_profesor = request.GET.get("id_profesor")
    curs.execute(
        "SELECT idProfesor ID, nombreProfesor Nombre, mailProfesor Mail, celularProfesor Celular FROM profesores WHERE idProfesor = %s",
        (id_profesor,),
    )
    profesor = curs.fetchone()

    if profesor:
        html_respuesta = render_template("editar_profesor.html", profesor=profesor)
        response.text = html_respuesta["text"]
        response.content_type = html_respuesta["type"]
    else:
        response.text = "Profesor no encontrado"


@app.ruta("/guardar_cambios_profesor")
def guardar_cambios_profesor(request, response):
    if request.method == "POST":
        id_profesor = request.POST.get("id_profesor")
        nombre = request.POST.get("nombre")
        mail = request.POST.get("mail")
        celular = request.POST.get("celular")
        cnx, curs = conexion_cursor(dictionary=True)
        print(id_profesor, nombre, mail, celular)
        consulta = "UPDATE profesores SET nombreProfesor = %s, mailProfesor = %s, celularProfesor = %s WHERE idProfesor = %s"
        curs.execute(consulta, (nombre, mail, celular, id_profesor))
        cnx.commit()
        response.status_code = 302
        response.location = "/profesores"
