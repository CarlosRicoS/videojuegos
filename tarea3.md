# Enunciado

Cree un programa que agregue al que entregó en el anterior ejercicio el siguiente comportamiento:

    Además de los enemigos actuales, que causan daño al entrar en contacto con el personaje, defina ahora otros que se ven atraídos por el personaje. Esa atracción se da a una distancia d, y hace que se muevan hacia el personaje a una velocidad v.

        Estos enemigos, cuando estén mas allá de una distancia d_o de su posición de origen p_o, automáticamente se regresarán a su punto de origen sin perseguir al jugador,

        Una vez vuelven a su origen pueden volver a perseguir al jugador si cumple el requisito de distancia nuevamente.

    Use los sprites dados tanto para el personaje como para los enemigos. 

        Tanto el jugador, como el nuevo enemigo utilizan sprites animados solamente cuando están en movimiento.

    Agregue un efecto de explosión a los rectángulos, después de estrellarse con otros y antes de desaparecer.

        La explosión contiene una animación nueva para implementar.

        Considere la explosión como una entidad separada que surge cuando las otras desaparecen. La explosión desparece por su cuenta al finalizar su animación.

## Detalles de configuración

Va a existir algunos cambios en la configuración, respecto a la configuración anterior. También aparecen nuevos elementos para configurar.

### De rectángulos a texturas y animaciones

Las entidades anteriormente utilizaban tamaño y color para definirse. Ahora, los rectángulos no se definen con estas caracterpistica, sino con una sola:

    Image: Una ruta relativa al archivo main.py de una imagen de tipo png.

Las entidades de manera opcional, pueden tener animaciones. Las animaciones son una serie de imágenes lineales en una sola textura con un ancho determinado. sus propiedades

    Numero de cuadros del sprite: cuando cuadros en una sola textura tiene.

    Lista de animaciones: una o varias animaciones con las siguientes propiedades

        Nombre

        Cuadro de  inicio: En que cuadro comienza. empieza desde cero

        Cuadro final: En que cuadro termina la animación. Debe ser igual o mayor que el de inicio.

        Velocidad o framerate: Velocidad de la animación en cuadros por segundo. No puede ser cero.

### Enemigos

Todos los enemigos ahora tiene sprites únicos en vez de tamaño y color.

También existe un nuevo tipo de enemigo llamado Hunter, y tiene características propias de animación y textura. El enemigo Hunter tiene animaciones de MOVE e IDLE

### Jugador

El jugador ahora posee una textura y animaciones, en vez de tamaño y color. sus animaciones son  MOVE e IDLE.
Bala

La bala ahora tiene su propio sprite único

## Explosion

Existe una nueva entidad llamada explosión Aparece cuando una bala choca contra un enemigo o un jugador choca contra un enemigo. Tiene una única animación EXPLODE. La entidad desaparece cuando la animación termine.
Detalles de implementación

Este ejercicio es una extensión del trabajo desarrollado hasta éste módulo. Para éste nivel tenga en cuenta lo siguiente:

    Lo primero es modificar el componente de CSurface para que soporte texturas y sprites.

        Esto hará grandes cambios en el calculo de áreas para colisión y tamaños.

        Por lo tanto, se recomienda una propiedad de "área" que determina el dibujado y tamaño de los rectángulos dada una textura y un sprite.

    El gran nuevo componente es el de animación, que será capaz de controla el flujo de la animación de cada personaje.

        Se recomienda tener una clase de ayuda como propiedad del componente para almacenar animaciones.

    Va a existir un nuevo tipo de enemigo, Hunter que representa al nuevo enemigo

    Es posible o crear un nuevo componente etiqueta para ello, o generar una propiedad de tipo de enemigo en la etiqueta de enemigo original.

    Se recomienda también crear una nueva etiqueta para la explosión

    Los sistemas recomendados son:

        Un sistema que controle cualquier componente de animación

        Un sistema para controlar el estado del enemigo nuevo

        Un sistema que controla el estado de la animación del jugador

        Un sistema que se encargue de eliminar las explosiones cuando terminen

    Los archivos json han sido modificados, así como existen nuevos archivos de configuración que deben ser tenidos en cuenta.

## Archivos de configuración

Se espera que, como mínimo, estos archivos de configuración de ejemplo funcionen. Se ofrecen varios para probar diversas situaciones.

    Los archivos de configuración que se deben implementar son los siguientes:

        window.json: Contiene información del título de la ventana, tamaño, fondo y framerate.

        enemies.json: Contiene información de cada tipo de enemigo existente en el juego.

        level_01.json: Contiene información del "nivel", en particular a que tiempo

            Se ha modificado este archivo y contiene información de posición de inicio del jugador y el límite de balas del nivel.

        player.json: Contiene información del rectángulo del jugador

        bullet.json: Contiene información de la bala que dispara el jugador
