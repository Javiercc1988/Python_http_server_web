import socket

HOST = 'localhost'
PORT = 15200

#AF_INET = IPV4 / SOCK_STREAM = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT)) # Bindeamos al servidor
    s.listen(1)  # Ponemos a escuchar 1 conexion
    print(f"Servidor preparado en el puerto: {PORT}")
    # Una vez hemos creado el socket empezamos el bucle para que acepte las peticiones que le vayan llegando.


    while True:
        conn, addr = s.accept()
        # Aceptamos las conexiones (esto devuelve 2 parametros)
        clientRequest = conn.recv(1024).decode("utf-8")


        #--------------------------------------------------------#
        # PARA VER LA CABECERA DE LA PETICION COMPLETA DESCOMENTAR LA SIGUIENTE LINEA
        # print("PETICION DEL CLIENTE ", clientRequest)
        #--------------------------------------------------------#


        splitList = clientRequest.split(" ")
        # Separamos con un espacio las peticiones del cliente
        method = splitList[0] 
        # Aquí cogemos "GET" que está en la primera posicion en la petición
        requestingFile = splitList[1]
        # Aquí cogemos "/" o lo que pida el cliente por ejemplo img

        print(f"El cliente realiza peticion de: {requestingFile} ")

        fileRequested = requestingFile.split("?")[0]
        fileRequested = fileRequested.lstrip("/")

        if fileRequested == "":
            fileRequested = "index.html"
        # Si la petición está vacía devolvemos el INDEX
        elif fileRequested == "css":
            fileRequested = "css/main.css"

        try:
            file = open(fileRequested, "rb")
            response = file.read()
            file.close()

            header = "HTTP/1.1 200 OK\r\n"

            if fileRequested.endswith(".jpg"):
                MIMEtype = "image/jpg"
            elif fileRequested.endswith(".css"):
                MIMEtype = "text/css"
            elif fileRequested.endswith(".png"):
                MIMEtype = "image/png"
            else:
                MIMEtype = "text/html"
            header += 'Content-type: ' +str(MIMEtype)+"\n\n"
            # MORE MIMEtypes: https://developer.mozilla.org/es/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types

        except Exception as e:
            header = "HTTP/1.1 404 OK\n\n"
            response = "Error 404: File not found\n\n".encode("utf-8")

        final_response = header.encode("utf-8")
        final_response += response
        conn.send(final_response)
        
