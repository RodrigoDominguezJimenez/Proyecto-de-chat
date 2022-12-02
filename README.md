# Proyecto-de-chat

## UNIVERSIDAD VERACRUZANA
### Facultad de Estadística e Informática
### E.E: Programación de sistemas
#### Periodo Agosto 2022 - Enero 2023

#### Integrantes del equipo
1. Rodrigo Domínguez Jiménez
2. Carlos Alberto Tamariz Morales
3. Daniel Sebastián Sánchez Medina
4. Vanessa Michelle Grapain Aldana
5. Aldahir Abisai Leal Cardeña
6. Isaias Landa Cervantes
7. Axel Naim Gomez Carreta
8. Erick Leonardo Martínez Hernández
9. Edgar Alejandro Hernández Maruri

## INTRODUCCIÓN
En la facultad de Estadística e Informática se  ha visto en un conflicto por no contar con un sistema de chat para que los estudiantes se comuniquen entre sí, por lo que se propone este programa que permita interactuar entre los mismos estudiantes, estudiantes maestros, estudiantes y secretarias, para que faciliten y ayuden a los jóvenes sobre las dudas que tengan de manera más rápida. 
Con ello lo que buscamos es que el trato sea de manera grupal o directa en el chat, lo que beneficia en estos tiempos de “pandemia” ya que sería de manera virtual  para que así haya menor riesgo de contagio de COVID-19 y se facilite el trato sea el lugar en cual este el alumno.

## DIAGRAMA DE CLASES 
![Diagramaclienteservidor](https://user-images.githubusercontent.com/111407329/204823356-b444dbaa-b50f-4c68-a8d1-644b34c0ce68.png)


## MÉTODOS
### QThread
### Señales
#### ¿Que son las señales?
Las señales son una característica del sistema operativo que proporciona un medio de notificar a un programa de un evento, y manejarlo de forma asíncrona.
Pueden ser generados por el propio sistema o enviados desde un proceso a otro.
Al igual que con otras formas de programación basada en eventos, se reciben señales estableciendo una función de devolución de llamada, llamada un manejador de señal,
que se invoca cuando se produce la señal. Los argumentos al manejador de señal son el número de señal y la pila desde el punto en el programa que fue interrumpido por
la señal.
### Sockets

## FUNCIONES

### HandleBroadcast
Funcion encargada del manejo de los broadCast, este se encarga de mandar los mensajes enviados por el usuario para que los reciban los demas usuarios en el chat grupal, tomando como argumento jsonObj siendo este emitido por la clase RecvMsg.

### FUNCION RUN
Método que representa la actividad del hilo. Se puede redefinir este método en una subclase. El método run() estándar ejecuta el objeto que se pasó al constructor en como argumento target, de haberlo, con argumentos secuenciales y por clave tomados de los argumentos args y kwargs, respectivamente.

### sendText
La funcion se encarga de revisar si es "chat" entonces es tipo broadcast y el mensaje que se manda lo podra ver cualquier usuario que este conectado, si no, entonces es de tipo privado, tiene un destinatario y un mensaje que iria de un usuario a otro.

### senBroadcaast(NumPy Broadcast())
Funcion se utiliza para devolver un objeto que imita la transmisión. Describe la capacidad de NumPy para tratar arrays de diferentes formas durante operaciones aritméticas.

## PRUEBAS

## CONCLUSIÓN

## BIBLIOGRAFÍA

https://rico-schmidt.name/pymotw-3/signal/index.html#:~:text=Las%20se%C3%B1ales%20son%20una%20caracter%C3%ADstica,y%20manejarlo%20de%20forma%20as%C3%ADncrona.
