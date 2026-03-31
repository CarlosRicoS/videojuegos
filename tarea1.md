# Pregunta 1

## Enunciado

Cree un programa que genere una serie de rectángulos con diferentes colores que rebotan en la pantalla. Estos rectángulos responden a varios archivos de configuración que determinan sus características. La configuración de la ventana también responde a un archivo de configuración.

Un ejemplo del resultado del ejercicio se puede ver aquí
(SEMANA UNO - EJERCICIO - RESULTADO WEB)
https://misw-4407-desarrollo-de-videojuegos.github.io/web-cohorte-2026-12/

## Detalles de configuración

#### Ventana

La ventana está definida por un archivo de configuración llamado window.json. Las propiedades de la ventana son:

    - El titulo de la ventana

    - El tamaño de la ventana (en pixeles)

    - El fondo de color de la ventana

    - El "framerate", o velocidad del reloj

#### Enemigos

Todos los rectángulos están definido en un archivo de configuración llamado enemies.json. 
Cada rectángulo tiene las siguiente propiedades:

    - Un nombre

    - Un tamaño (x, y)

    - Un color (r, g, b)

    - Una velocidad mínima y una velocidad máxima

#### Nivel

Los rectángulos aparecen en la pantalla en respuesta a un archivo de configuración level_01.json que define una lista de eventos de aparición, que especifica:

    - El tipo de rectángulo que va a aparecer (usando su nombre como referencia).

    - Un tiempo de cuando debe aparecer (en segundos).

    - Una posición donde aparecerá (de la esquina superior izquierda). 

El ángulo de dirección hacia donde sale el cada rectángulo es al azar.

### Detalles de implementación

Este ejercicio es una extensión de la serie de videos de la práctica de la primera semana soportará dos nuevos requerimientos.

    Va a existir un nuevo sistema que va a crear nuevos rectángulos, uno por uno, cada cierta cantidad de tiempo a partir de un archivo de configuración hasta terminar con todos los rectángulos.

        - Se debe crear un nuevo componente, Llamado CEnemySpawner, y un nuevo sistema, llamado  system_enemy_spawner. 

            - Debe existir solamente UNA ÚNICA entidad con UN componente de CEnemySpawner. No pueden existir múltiples entidades con un componente CSpawner ni otras entidades deben tener este componente.

            - Este componente contendrá la información de utilidad para el sistema de spawn. En esencia, debe contener la información del JSON cargado que representa un nivel. La información la pueden organizar como lo vean mejor posible. 

            - No trabajen directamente con el archivo JSON de nivel. Guarden la información dentro del componente CEnemySpawner. 

                - Los otros archivos JSON los pueden tener precargados en el motor y usarlo cuando se necesario (e.g. cambiar un aspecto de la ventana o crear un cuadrado) 

        - El sistema se encargará de generar los rectángulos solicitados en el archivo de configuración en una posición de la pantalla, dada la información del tiempo definido por cada evento de la configuración.

            - No está permitido el uso de Timers o Schedulers nativos de python para este sistema. Es obligatorio que registren el paso del tempo con el uso de delta_time. 

            - No deben cargar archivos JSON dentro de un sistema. El sistema no es para eso, el archivo JSON debe estar cargado y procesado dentro del componente y cambiarlas propiedades ahí. Los archivos JSON se pueden cargar desde otra clase (o la clase misma del motor) y tenerlas listas para usar donde sea necesario.

            - El sistema lo único que debe hacer es crear cuadrados según el tipo cuando el tiempo transcurrido sea igual o supere el tiempo asignado de cada evento según los datos del componente.

            - Los sistemas solamente utilizan los datos obtenidos a través del paradigma ECS. El sistema no debe de tener lógica adicional a lo que pretende hacer, la idea de los sistemas y componentes es que sean lo más mínimos posibles. 

            - Es recomendado crear una variable para cada evento de creación que registre si ya ha sido disparado o no. De esta manera se puede marcar y luego ignorar el evento si ya ha sido ejecutado. Aunque no es obligatorio hacerlo de esta manera, es la forma recomendada.

### Archivos de configuración

Varios ejemplos de archivos de configuración (los cuales serán utilizados para probar en la evaluación) se pueden descargar desde aquí :
(SEMANA UNO - EJERCICIO - RECURSOS PARA VERIFICACIÓN)
https://misw-4407-desarrollo-de-videojuegos.github.io/web-cohorte-2025-12/

Se espera que, como mínimo, estos archivos de configuración de verificación funcionen (solo deben copiar y pegar lo que está adentro y reemplazar por cada archivo de configuración equivalente).

    - Los archivos de configuración que se deben implementar son los siguientes:

        - window.json: Contiene información del título de la ventana, tamaño, fondo y framerate.

        - enemies.json: Contiene información de cada tipo de enemigo existente en el juego.

        - level_01.json: Contiene información del "nivel", en particular a que tiempo aparecen qué rectángulos en qué color y qué posición en el mundo, junto con una velocidad mínima y máxima. Al rectángulo creado se le asigna asigna una velocidad al azar entre esos dos valores. Su dirección inicial se asigna al azar.

            - En el ejemplo de configuración de nivel aparecen seis rectángulos. Pero es posible tener más de seis, o es posible que no exista ninguno.

Para los archivos de configuración, es necesario saber cargar archivos de tipo json en Python. Para saber más sobre como cargar archivos JSON en Python pueden visitar este sitio web: https://www.geeksforgeeks.org/read-json-file-using-python/
