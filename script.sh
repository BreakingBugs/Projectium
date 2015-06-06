#! /bin/bash
python CrearBasedeDatos.py
if [ $? -eq 0 ];then
    echo "Creando migraciones..."
    python manage.py makemigrations
    echo "Migrando base de datos..."
    python manage.py migrate
    echo "Poblando base de datos..."
    #python manage.py loaddata fechascambiadas
    #python manage.py loaddata init_with_files
    #python manage.py loaddata fixtures/initial_data.json
    echo "Creando versiones iniciales..."
    #python manage.py createinitialrevisions
    echo "Ejecutando pruebas..."
    #python -Wi manage.py test
else
    echo "Lo sentimos, no se pudo realizar la poblacion."
fi