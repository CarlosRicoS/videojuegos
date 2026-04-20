Enunciado

Complemente el programa entregado en el ejercicio anterior con la siguiente funcionalidad:

    Agregue un texto para dibujar un título en la pantalla principal del juego

    Agregue un evento extra para pausar y reanudar el juego con la tecla "P". Debe de mostrar un texto que indica que el juego está pausado

    Cargue efectos de sonido para las colisiones y para el movimiento del personaje.

    Haga sonar los efectos de sonido en los momentos adecuados

    Use los patrones ServiceLocator para cargar los recursos de sonido, imagen y texto que necesite

Personalización del juego

Esta es la oportunidad para hacer el juego propio, con características propias que deseen. Deben implementar aunque sea una característica única. Las condiciones para la característica son:

    Que use un elemento de input del teclado o el ratón

    Que sea temporal y requiera "recargar"

    Que tenga algún elemento visible que sea diferente de los actuales.

    Que la opción de recargar se vea ya sea en una barra de carga o en un número en forma de texto desplegado en la pantalla

    Se espera que apliquen los elementos de gamefeel en este efecto especial (en resumen, hagan que se sienta bien)

    Se esperan instrucciones de input muy simples en forma de texto en la pantalla

    No hay una regla para el efecto que deseen crear. pero si necesitan ayuda, aquí hay un par de sugerencias.

        Una defensa especial por 2 segundos activados por una tecla o el ratón. Durante esos 2 segundos, todos los enemigos a una distancia menor a dU serán eliminados. Una vez usada, la defensa no puede activarse por 5 segundos.

        Una ataque especial activado con una tecla o el ratón. El ataque divide una bala en cuatro que disparan en las diagonales de la bala. Una vez usado, el ataque especial no puede usarse por 2.5 segundos. (Demostrado en el proyecto de ejemplo)

Distribución

    Finalmente, suba el juego a itch.io, ya sea en despliegue web o en despliegue de ejecutable descargable y adjunte un archivo README.txt con el enlace dentro de la entrega.


Detalles de configuración

Solamente existe un cambio nuevo en los archivos de configuración actuales:
Sonidos

Los sonidos se encuentran asociados a cada entidad que los necesite, con el parámetro sound. 

Los asteroides, las balas y las explosiones tienen un sonido cuando aparecen en la pantalla. Los enemigos de tipo Hunter únicamente tiene un sonido tiene un sonido llamado sound_chase , que se activa cuando comienza a perseguir al jugador.
Interfaz

La configuración de la interfaz se establece en un archivo de su creación llamado interface.json. Este archivo contiene propiedades de texto fijo, la cuales son:

    La ruta de recurso de fuente tipo .ttf, que debe ser cargado usando el patrón Service Locator.

    Una cadena de caracteres que indica el contenido texto

    El color del texto

    Un tamaño del texto

No hay una especificación de cómo está construido este archivo. La estructura y ordenamiento del mismo es a su discreción. El único requerimiento es que exista y lo usen para procesar las propiedades básicas de sus textos.
Personalización

Para los detalles de personalización no se provee ningún archivo de configuración dedicado. Se espera que ustedes creen esos archivos de configuración, si lo ven necesario.
Detalles de implementación

Los elementos más importante que se recomiendan crear son los siguientes:

    Una clase de ServiceLocator, que guarde los servicios de carga de sonidos, imágenes, fuentes, etc.

    Los servicios individuales deben tener métodos específicos para cada clase.

    Los textos en pygame son superficies y se  recomienda modificar el componente de superficie para poder crear a partir de texto, colores y fuentes.

        Para crear texto estático solo se requiere un método de clase llamado from_text para obtener una superficie a partir de texto.

        Un texto dinámico requiere de recrear la superficie de fuente desde cero fon font.render(texto, color). Es decir que un texto que cambie debe hacer esto dentro de un sistema que ejecuta la función de font.render con el texto adecuado y reemplazar la superficie y el área del componente.

    La personalización es individual y depende de lo que deseen lograr. Sin embargo, como objetivo de este curso se requiere ejercer al patrón ECS de principio a fin.

    Para pausar y reanudar un juego en ECS, simplemente deben considerar ejecutar o no los sistemas pertinentes en pausa. Sin un sistema de movimiento, nada se mueve o sin un sistema de colisión, nada "choca".