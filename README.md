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
9. Mauricio Hernández Sánchez
10. Mario Azael Garcia Rodriguez
11. Juan Daniel Cebada Colula 
12. Victor Emmanuel López Espejo
13. Samuel Ruiz Castillo
14. Edgar Alejandro Hernandez Maruri
15. Cristian Jair Hernández Durán
16. Germán de Jesús Suárez Tapia
17. Jesús Herón Gálvez Vázquez

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

### StarServer
En esta función se inicializa el servidor y por cada cliente que se conecta, se crea un hilo, y un socket donde se guarda la dirección, que después manda un mensaje diciendo que el servidor está escuchando y muestra la dirección ip y el puerto donde esta corriendo el servidor, seguido de que cuando un cliente se conecta, también imprime “cliente conectado de”, y la información del cliente se guarda en un hilo.

### HandleNotif
En la primera parte del metodo, la primera función es que esta diciendo que si recibe un cliente en la conexion del servidor, se le mostrara un mensaje de exito y le aplicara el nombre de usuario, y la funcion del if es que esta diciendo que si recibe una notificación de tipo de conexión, se ejecutará el código, en caso contrario se mostraria un mensaje que diciendo que se desconecto y se borrara el nombre de usuario. 

### HandleBroadcast
Funcion encargada del manejo de los broadCast, este se encarga de mandar los mensajes enviados por el usuario para que los reciban los demas usuarios en el chat grupal, tomando como argumento jsonObj siendo este emitido por la clase RecvMsg.

### HandleDirect
En esta funcion se encarga de mandar el mensaje de manera directa a un usuario en especifico, si no existe un tab con el usuario que queremos enviar el mensaje se crea uno con un textEdit el cual llama a una funcion para que solo pueda ser de lectura ademas este recibe el nickname del cliente de origen, y el nickname junto con un jsoObj son agregados al tab, en cambio si este tab ya existe solo reasigna los datos antes mencionados al tab, por ultimo se pregunta si el jsonObj es de tipo file el cursor mostrara un mensaje de que enviaron un archivo junto con el nickname del cliente de origen con un mensaje, si no solo mostrara el nickname del cliente de origen y el mensaje

### Run
Método que representa la actividad del hilo. Se puede redefinir este método en una subclase. El método run() estándar ejecuta el objeto que se pasó al constructor en como argumento target, de haberlo, con argumentos secuenciales y por clave tomados de los argumentos args y kwargs, respectivamente.

### checkNoEmpty
De lo que se encarga esta función es la de checar que los campos de Nickname, server IP y el del puerto del servidor, si estos cuadros de textos se encuentran vacíos el botón de ‘Connect to server’ no estará habilitado

![](https://user-images.githubusercontent.com/113154040/205403477-c32328f5-88d2-4ecb-83da-be5c6f6570bc.png)  ![](https://user-images.githubusercontent.com/113154040/205403491-3161a2dc-7448-4e68-a958-6eb878e8c8af.png)}

### connetServer
Lo que se encarga hacer esta función es la de asignar a las variables ‘nickname’, ‘ip’ y ‘port’ los textos que se encuentran en los ‘QLineEdit’ para posteriormente mandarlos al servidor y hacer el registro, al final se cierra la ventana de ‘Custom dialog’

### senBroadcaast(NumPy Broadcast())
Funcion se utiliza para devolver un objeto que imita la transmisión. Describe la capacidad de NumPy para tratar arrays de diferentes formas durante operaciones aritméticas.

### sendDirect
Se encarga del envio un mensaje a un cliente especifico.El "cliente" llama al objeto para verificar que se encuntre en el indice del receptor, mediante el metodo IF, 
dando la funcion para devolver un objeto que imita la transmisión 

### sendText
Se encarga de varificar si la opcion es un 'chat', luego con un json envia un mensaje de tipo broadcast y el mensaje que se escribió, si no, con el json enva el mensaje de tipo privado a un receptor seguido del mensaje.

### cliente.py
Hace la entrada a la clase CustomDialog y se ejecutan los metodos de dichas clases, despues hace la comparativa si el atributo connect esta en verdadero o en falso; si esta condición es verdadera se toma los atributos de "ip", "port" y "nickname" del objeto "dlg" y se mandan a la función de "connetServer".

### clientHandle
Manejo de clientes, los clientes pueden enviar 3 tipos de mensajes; handshake, broadcast y direct.
El handshake permite que responda con la lista de clientes, avisa a los otros clientes que el usuario se ha conectado. El broadcast permite enviar mensajes a todos los clientes. El direct permite enviar mensajes directos entre clientes.

### handleClientList
Este metodo se encarga de crear una caja div usando html para informarnos dentro de ella que nos hemos conectado al chat y también nos indica "Tú" en los mensajes que 
han sido enviados por nosotros mismos, usando como argumento json0bj

### sendHandshake
Esta función crea un mensaje escribiendo el tipo, que es un hansdhake, y mediante el uso del *json.dump* agrega el nickname del usuario.
Además, mediante el *socket.send* envía el mensaje encriptándolo con *(msg.encode())*.

### closeEvent
Verifica que tenga atributos utilizando una condicional con el método *hasattr()*, y de ser verdadero, retorna un **true**, dándole la instrucción al socket para que se apague, todo esto gracias al comando *socket.shutdown(*socket.**SHUT_DOWN*)*.

## PRUEBAS
#### como se ve la interfaz
![prueba 1](https://raw.githubusercontent.com/RodrigoDominguezJimenez/Proyecto-de-chat/c1c6b54d0c4aaedd0939378b164d5acce2670880/pruevbas/Captura%20de%20pantalla%202022-12-11%20232127.png)  
#### como se ve la configuracion  
(![image](https://user-images.githubusercontent.com/113264761/206968425-100dbfe3-b88f-467e-a1ae-b855ed40530b.png)  
#### el servidor   
( ![image](https://user-images.githubusercontent.com/113264761/206968503-2d56371b-6c65-4f3e-9852-b689b1fb8636.png)  
#### pruebas con usuarios 
( ![image](https://user-images.githubusercontent.com/113264761/206968547-1796a721-b149-475b-880d-ac8d52a274fb.png)  
( ![image](https://user-images.githubusercontent.com/113264761/206968611-da1da371-bbb5-43ef-9ff0-7e7a9d416cf7.png)  
( ![image](https://user-images.githubusercontent.com/113264761/206968670-6cd79df9-a6c7-4ce5-8ec9-583a5feec424.png)  
( ![image](https://user-images.githubusercontent.com/113264761/206968713-46f4aa99-ec66-4030-ad88-bb47e65c85df.png)  
( ![image](https://user-images.githubusercontent.com/113264761/206968780-b9785718-854b-43be-95d6-b3efec8eaa08.png)  
( ![image](https://user-images.githubusercontent.com/113264761/206968888-42eb6ea8-1ecb-44ca-bac4-c0425a22b0ab.png)  


## CONCLUSIÓN

## BIBLIOGRAFÍA

https://rico-schmidt.name/pymotw-3/signal/index.html#:~:text=Las%20se%C3%B1ales%20son%20una%20caracter%C3%ADstica,y%20manejarlo%20de%20forma%20as%C3%ADncrona.
