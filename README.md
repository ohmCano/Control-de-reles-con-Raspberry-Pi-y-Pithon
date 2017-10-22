# Control-de-reles-con-Raspberry-Pi-y-Pithon
Sistema de control de módulo de 8 relés con raspberryPi y python.

*Importante. Si modificamos el archivo /etc/profile y añadimos la siguiente linea

sudo python ruta/rele8.py

Conseguimos que el escript se ejecute automáticamente cada vez que la rPi se encienda. Por eso necesito un mecanismo que guarde el estado de
los relés para que en el caso de que se vaya la luz, al volver a iniciar la rPI los relés se activen o se desactiven según la úlitma configuración.

Recuerdamos que el excript se ejecuta en cli, desde nos pide modificar el estado de alguno de los reles. Cada vez que se modifica uno de los
relés se actualiza el fichero que contiene la información de los estados.
