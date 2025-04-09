# Microservicio _users-ms_

Este microservicio se encarga de gestionar a los usuarios de la plataforma, incluyendo su registro, autenticación y administración básica.

## Funcionalidades principales

* Registro de nuevos usuarios.
* Autenticación mediante OAuth2 con JWT.
* Obtención, actualización y eliminación de usuarios.

## Instrucciones de Uso

1. Clonar el repositorio de GitHub:

```
git clone https://github.com/jubedoyat/users-ms.git
```

2. Abrir la carpeta clonada con un editor como Visual Studio Code o desde una terminal.

3. (Opcional) Crear un entorno virtual:

```
python -m venv venv
```

Y activarlo:

```
source venv/bin/activate
```

4. Instalar los paquetes necesarios:

```
pip install -r requirements.txt
```

5. Ejecutar el microservicio:

```
uvicorn app.main:app --reload --port 8000
```

6. Acceder desde un navegador:

```
http://127.0.0.1:8000
```

## Endpoints

- `POST /users/`: registra un nuevo usuario.
- `GET /users/{user_id}`: obtiene un usuario por su ID (_Mongo ObjectId_).
- `DELETE /users/{user_id}`: elimina un usuario por su ID.
- `PUT /users/{user_id}`: actualiza información de un usuario.
- `GET /users/`: lista todos los usuarios.
- `POST /login`: permite a los usuarios autenticarse y obtener un token JWT.

### Uso

Se recomienda utilizar `/docs/` para interactuar con los endpoints.

### Parámetros

- `/users/{user_id}`: Se debe proporcionar el identificador único del usuario en la base de datos MongoDB (campo `_id`) como parte de la URL. Este identificador se obtiene al crear el usuario y es necesario para operaciones de consulta, actualización o eliminación.

- `/login`: Requiere que el cliente envíe dos campos como parte del formulario (`application/x-www-form-urlencoded`):
    * `username`: corresponde al correo electrónico del usuario registrado.
    * `password`: la contraseña asociada a ese usuario. Esta información es validada y, si es correcta, se devuelve un token JWT para autenticación futura.

### Resultados

- `POST /users/`: Devuelve un objeto JSON con los datos del usuario creado, incluyendo su `_id` y campos como `name`, `email`, `age`, etc. La contraseña no se incluye por seguridad.

- `GET /users/{user_id}`: Devuelve los datos del usuario correspondiente al ID proporcionado. Si no existe, retorna un error `404 Not Found`.

- `POST /login`: Devuelve un token JWT en formato JSON si las credenciales son válidas:

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

Este token debe usarse en futuras peticiones autenticadas en el encabezado `Authorization` como `Bearer <token>`.

- `PUT /users/{user_id}`: Devuelve el usuario actualizado si el ID existe. Si no se encuentra, retorna un `404`.

- `DELETE /users/{user_id}`: Retorna un mensaje de éxito si el usuario fue eliminado correctamente. Si no existe, retorna un `404`.

- En caso de credenciales incorrectas durante el login, se retorna un `401 Unauthorized` con el mensaje `"Invalid username or password"`.