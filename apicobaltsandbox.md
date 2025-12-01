API Transaccional
Documentación para VISA y Mastercard
Cobalt | www.cobalt.tech
TABLA DE CONTENIDOS
INTRODUCCIÓN....................................................................................................................................3
CONSIDERACIONES GENERALES...........................................................................................................4
Tipos de Transacciones....................................................................................................................4
Definición de claves.........................................................................................................................4
Headers............................................................................................................................................4
ERRORES Y ESTADOS.............................................................................................................................5
Composición de mensajes de error.................................................................................................5
Códigos de error..............................................................................................................................5
Estados de una transacción.............................................................................................................5
AUTORIZACIÓN.....................................................................................................................................7
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
Generación de token........................................................................................................................7
TRANSACCIONES...................................................................................................................................9
+ =
Cobalt
Lista de Transacciones......................................................................................................................9
Venta..............................................................................................................................................11
Transacciones con tarjeta tokenizada............................................................................................13
Transacciones autenticadas...........................................................................................................15
PreAutorización..............................................................................................................................16
Ajuste.............................................................................................................................................17
Reembolso.....................................................................................................................................18
3
1 2 3
Consultar datos de una Transacción..............................................................................................19
LOGOTIPO
LA MARCA
Parámetros 3DS..............................................................................................................................20
CORPORATIVO
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
El logotipo es el signo gráfico
cualquier soporte.
identificador de la marca en todas
HISTORIAL DE VERSIONES...................................................................................................................26
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
+
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 2
1. INTRODUCCIÓN
El API Transaccional permite procesar una transacción directamente desde API sin
necesidad de una interfaz gráfica. Esta API está diseñada para comercios que manejen un
gran volumen de transacciones y necesiten administrar de su lado los datos del cada
cliente.
Esta API actualmente soporta transacciones con tarjetas VISA y Mastercad. Para el
procesamiento de tarjetas Clave solicite el servicio Checkout.
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
Esta API soporta respuestas en formato JSON y formato XML según desee el desarrollador.
Para dichos formatos será necesario enviar en el header Accept los valores application/json o
+ =
Cobalt
application/xml respectivamente.
3
1 2 3
LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
+
LA MARCA
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 3
2. CONSIDERACIONES GENERALES
a. Tipos de Transacciones
Existen diferentes tipos de transacciones. Esta API soporta transacciones de Ventas,
Preautorizaciones, Ajustes, transacciones de Crédito y Reversa.
Para realizar la reversa de una transacción es necesario indicar cuál es la transacción que se
desea reversar (o anular) . Esta transacción debe de haber sido autorizada en el mismo día que
se realiza la reversa. Si se desea reversar una transacción de días anteriores es necesario realizar
una transacción de Crédito.
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
+ =
Cobalt
b. Definición de claves
i. {{host}}: URL proporcionada por la entidad.
ii. {{client_id}}: ClientId entregado por la entidad.
iii. {{client_secret}}: ClientSecret entregado por la entidad.
iv. {{access_token}}: Token de acceso.
3
1 2 3
v. {{transaction_id}}: ID de la transacción en el sistema CBO.
LOGOTIPO
LA MARCA
CORPORATIVO
c. Headers
El logotipo es el signo gráfico
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
Para todas las llamadas es necesario enviar los siguientes headers:
+
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Header Isotipo
Valor
logotipo
Authorization Bearer {{access_token}}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 4
3. ERRORES Y ESTADOS
a. Composición de mensajes de error
{
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
"status": "error",
"message": "Invalid parameters",
"data": {
"amount": [
"El parámetro amount es requerido"
]
},
+ =
Cobalt
}
"error": "invalid_parameter"
b. Códigos de error
Código Error Descripción
400 invalid_parameter Ha fallado la validación de algún parámetro.
401 unauthorized_access La autenticación proporcionada no es correcta. Revise las
1 2 3
credenciales otorgadas.
3
LOGOTIPO
CORPORATIVO
LA MARCA
ÁREA DE
SEGURIDAD
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
El logotipo es el signo gráfico
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
+
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
c. Estados de una transacción
Isotipo
logotipo
Una transacción puede tener varios estados durante el procesamiento.
Estado Descripción
pending Estado inicial de una transacción. Indica que todavía está pendiente de ser procesada.
authenticating La transacción se encuentra pendiente de autenticación 3DS por parte del tarjehabiente.
processing La transacción se encuentra en procesamiento. La duración este estado puede ser de hasta 30
segundos.
orphan La transacción se envió a procesar pero no se obtuvo ningún tipo de respuesta.
authorized La transacción se ha procesado y el cobro fue autorizado por el banco emisor de la tarjeta.
denied La transacción se ha procesado pero el cobro fue denegado por el banco emisor de la tarjeta.
Revise la razón en el valor response_code.
refused La transacción ha sido rechazada por el sistema y no se ha procesado debido a algún tipo de
incumplimiento comercial.
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 5
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
+ =
Cobalt
3
1 2 3
LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
LA MARCA
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
+
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 6
4. AUTORIZACIÓN
Esta API utiliza el estandar OAuth2 para la autorización segura del uso de los endpoints
expuestos. El proceso de autorización se compone de un client_id y un client_secret. Estos
elementos se envían en una petición POST para obtener un token de autorización válido
para ser usado en cualquiera de los enpoints. Se debe tener en cuenta que este token tiene
un tiempo de expiración y serán necesario volver a generar uno nuevo cuando este haya
expirado.
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
a. Generación de token
i. Endpoint: {{host}}/oauth/token
ii. Método: POST
+ =
Cobalt
iii. Parámetros
Parámetro Tipo Descripción
grant_type Requerido. Texto. Valor fijo: client_credentials.
client_id Requerido. Texto. Cliend ID generado para el servicio comercial.
client_secret Requerido. Texto. Client Secret generado para el servicio comercial.
3
1 2 3
LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
b. Ejemplo
{
LA MARCA
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
+
Isotipo
logotipo
"grant_type": "client_credentials",
"client_id": "9d44c02a-ea81-4e9a-bacb-10c68fcdf776",
"client_secret": "1L0EAhrQklxe9gQ43G4rynwIzaptwSDkrH4Yg1gG"
}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 7
c. Respuesta
{
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
"token_type": "Bearer",
"expires_in": 86400,
"access_token":
"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZDQ0YzAyYS1lYTgxLTRlOWEtYmFjYi0xMG
M2OGZjZGY3NzYiLCJqdGkiOiI5ODAyNzMxOTk4YzM4NDdiNjljNDE4OGZlMGEyOTBjYzViYTY4YzkyM
DA0MjNlYzAzNmY0YzgxYmE3OWI2MDZmMjRhYTVhN2IxNTM5YzNkNyIsImlhdCI6MTcyOTI2MTA5N
y40NTYyOTUsIm5iZiI6MTcyOTI2MTA5Ny40NTYyOTgsImV4cCI6MTcyOTM0NzQ5Ny40NTI1NTQsInN
1YiI6IiIsInNjb3BlcyI6W119.fqkSmSrrG6xaY4yXXm1nhUoL86kIf5s1Nfn1brMDVPueB_NmC0GWVWx
DyXLYbiuiIV9X5em_Y-lSCWBIcg89yfB-
KgMtohYWroSRdKJi1EHX5GwVecKrzQ1fwHF06IHjnJMC4rTlYDkqLGOKwarLBywWreu4GNscihNq4u
RIbSX8b7C6sB2TQeBiTiB84O5FWhNEhueHVtZiDIsMzWV7xfeea64-jfPQT3b2-
wkR4PJ_3sxMnp_E83DcrQR_ujConIdYblZSrhd6p2ks3n7faQWyNI6gOHHdVFleV7nr5jkhRX_LFAUo1
+ =
Cobalt
hovwryr1cUQEHjHmmxni4vGqY9c1mgXca_oCVX5El90z-tTxwRJSc35qMpZ86wO-W7-
8ONRXx8Fz0oUgfvsFQnQCkvc8cHocm8wkLSjvDKRMgjCQ9jvEynil0000Q3_vbhSWKkPUihelD_78yK
03bY8LmiqilbHuBDNFD74ZocwfB5v4oKf5rBzv47r7pm8E5W0-
7jW1QlKF1lrIvrCLPwUzdXNJ6lGEH4LgLCWI7hGvPi__qBJepOtypYKFgkNWp6HwTxagDm4zJlxSrsaPp
0dSpbywlSZQuKfHa8EhkVSvwycgxHQ1lM5NjUNTxXQpzOJT_ryvyNfv3yR7vWqabDxIzB40JPi0jHYP
W0Vi9R1SGfBdXoumQI"
}
3
1 2 3
LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
+
LA MARCA
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 8
5. TRANSACCIONES
a. Lista de Transacciones
i. Endpoint: {{host}}/api/v2/transactions
ii. Método: GET
iii. Parámetros
Parámetro Tipo Descripción
limit page start_date Opcional. Numérico. Opcional. Numérico. Opcional. Fecha. 0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
end_date Opcional. Fecha. Límite máximo de transacciones a devolver. Por defecto 20.
Página de la lista transacciones. Por defecto 1.
Fecha inicial del rango que comprenderá la lista de los resultados
devueltos. Formato: YYYY-MM-DD.
Fecha final del rango que comprenderá la lista de los resultados
devueltos. Formato: YYYY-MM-DD.
+ =
Cobalt
3
1 2 3
LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
+
LA MARCA
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 9
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
iv. Respuesta
{
"status": "ok",
"message": "success",
"data": {
"current_page": 1,
"data": [
{
"id": 280902,
"identifier": 130280902,
"service_id": 21,
"merchant_id": "123696969",
"terminal_id": "CNTRGEEK",
"processor": "simulator",
"type": "sale",
"status": "authorized",
"ballot": "00000001",
"pan": "449187******5094",
"exp_date": "2023-09-01T00:00:00.000000Z",
"currency_code": "840",
+ =
Cobalt
"card_holder": "MC",
"amount": 100,
"tax": 0,
"reversal_tx": null,
"adjustment_tx": null,
"response_code": "00",
"authorization_number": "352539",
"reference_number": "048493539351",
"brand_reference": null,
"processed_at": "2023-04-25 13:10:10",
"created_at": "2023-04-25T13:10:09.000000Z",
3
1 2 3
"updated_at": "2023-04-25T13:10:10.000000Z",
LOGOTIPO
"metadatas": {
LA MARCA
CORPORATIVO
Estas son las 4 variedades de uso,
El logotipo es el signo gráfico
"ip": "127.0.0.1",
pudiéndose adaptar sin problema a
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
"card_brand": "VISA"
identifica a la marca.
}
}
+
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
],
"first_page_url": "http://cbo.local/api/transactions?limit=1&page=1",
logotipo
Isotipo
"from": 1,
"last_page": 1,
"last_page_url": "http://cbo.local/api/transactions?limit=1&page=1",
"links": [
{
"url": null,
"label": "&laquo; Previo",
"active": false
},
{
"url": "http://cbo.local/api/transactions?limit=1&page=1",
"label": "1",
"active": true
},
{
"url": "http://cbo.local/api/transactions?limit=1&page=2",
"label": "Siguiente &raquo;",
"active": false
}
],
"next_page_url": null,
"path": "http://cbo.local/api/transactions",
"per_page": "20",
"prev_page_url": null,
"to": 1,
"total": 1
}
}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 10
b. Venta
i. Endpoint: {{host}}/api/v2/transactions/sale
ii. Método: POST
iii. Parámetros
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
Parámetro Tipo Descripción
amount Requerido. Numérico. Monto a cobrar expresado en centavos de dólar.
pan Requerido. Texto. Numeración de la tarjeta.
exp_date Requerido. Fecha. Fecha de vencimiento de la tarjeta. Formato: MM/YY.
currency_code Requerido. Texto. Acrónimo de la moneda. Para dólar: USD.
cvv2 Opcional. Texto. Código de Verficación de la tarjeta.
card_holder + =
Cobalt
Opcional Texto. Nombre del titular de la tarjeta.
tax Opcional. Numérico. Valor de ITBMS expresado en centavos de dólar.
tip Opcional. Numérico. Valor de propina expresado en centavos de dólar.
metas Opcional. Array. Matriz Clave-Valor de datos adicionales a enviar.
3ds_params Opcional. Array. Matriz Clave-Valor de datos para la autenticación 3DS. Ver
sección Parámetros 3DS.
webhook 1 LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
Requerido si
3ds_params está
presente.
URL del comercio donde se enviará el resultado de la
2 transacción.
LA MARCA
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
iv. Ejemplo
+
3
3
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
{
"currency_code": "USD",
"amount": "100",
"tax": "0",
"tip": "0",
"pan": "4491870000005094",
"exp_date": "09/23",
"card_holder": "MC"
}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 11
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
v. Respuesta
{
"status": "ok",
"message": "success",
"data": {
"id": 280910,
"identifier": 130280910,
"service_id": 21,
"merchant_id": "123696969",
"terminal_id": "CNTRGEEK",
"processor": "simulator",
"type": "sale",
"status": "authorized",
"ballot": "00000008",
"pan": "449187******5094",
"exp_date": "2023-09-01T00:00:00.000000Z",
"currency_code": "840",
"card_holder": "MC",
+ =
Cobalt
"amount": 100,
"tax": 0,
"reversal_tx": null,
"adjustment_tx": null,
"response_code": "00",
"authorization_number": "765004",
"reference_number": "047894276372",
"brand_reference": null,
"processed_at": "2023-04-25 23:50:00",
"created_at": "2023-04-25T23:49:58.000000Z",
"updated_at": "2023-04-25T23:50:00.000000Z",
1 2 3
"metadatas": {
3
LOGOTIPO
"ip": "127.0.0.1",
LA MARCA
CORPORATIVO
"card_brand": "VISA"
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
El logotipo es el signo gráfico
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
}
El isotipo es el simbolo que
identifica a la marca.
}
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
}
+
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 12
c. Transacciones con tarjeta tokenizada
El API Transaccional permite el procesamiento de transacciones con tarjetas tokenizadas bajo
nuestro sistema.
Una tarjeta tokenizada es una tarjeta donde el comercio previamente nos comparte los datos
de la tarjeta y es almacenada de forma segura en nuestro sistema. En este proceso el comercio
obtiene un token que podrá usar posteriormente cuando requiera realizar transacciones sin
necesidad de volver a enviar los datos de la tarjeta. En su lugar enviará el token generado por
nuestro sistema. Para más información del proceso de tokenización consulte la documentación
del API Bóveda de clientes.
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
Cuando se usa un token, los parametros pan, exp_date y card_holder no serán necesarios. Sin
embargo se requiere el parámetro customer_token que tendrá como valor el token generado.
+ =
Cobalt
i. Ejemplo
{
"currency_code": "USD",
"amount": "98440",
"tax": 0,
1 2 3
"customer_token": "4pc3CiAj8ZTiUEYlq54JeVfvPX3crQSY",
3
"type": "sale",
LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
"tip": 0
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
}
identifica a la marca.
LA MARCA
ÁREA DE
SEGURIDAD
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
+
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 13
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
ii. Respuesta
{
"status": "ok",
"message": "success",
"data": {
"id": 280910,
"identifier": 130280910,
"service_id": 21,
"merchant_id": "123696969",
"terminal_id": "CNTRGEEK",
"processor": "simulator",
"type": "sale",
"status": "authorized",
"ballot": "00000008",
"pan": "449187******5094",
"exp_date": "2023-09-01T00:00:00.000000Z",
"currency_code": "840",
"card_holder": "MC",
+ =
Cobalt
"amount": 100,
"tax": 0,
"reversal_tx": null,
"adjustment_tx": null,
"response_code": "00",
"authorization_number": "765004",
"reference_number": "047894276372",
"brand_reference": null,
"processed_at": "2023-04-25 23:50:00",
"created_at": "2023-04-25T23:49:58.000000Z",
"updated_at": "2023-04-25T23:50:00.000000Z",
1 2 3
"metadatas": {
3
LOGOTIPO
"ip": "127.0.0.1",
LA MARCA
CORPORATIVO
"card_brand": "VISA"
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
El logotipo es el signo gráfico
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
}
El isotipo es el simbolo que
identifica a la marca.
}
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
}
+
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 14
d. Transacciones autenticadas
Es posible enviar una transacción autenticada por un proveedor ACS externo. Para ello el
comercio debe disponer de un servicio ACS para realizar dicha autenticación y posteriormente
enviar los datos generados por el autenticador. Estos datos se enviarán dentro de la matriz JSON
metas. Estos son los parámetros soportados:
Parámetro Tipo Descripción
3ds_transaction_id Opcional. Texto. Directory Server Transaction ID (DSTID) único generado por el servidor
comercial ACS para identificar la transacción.
3ds_authentication_value Opcional. Texto. Valor de CAVV (VISA) o UCAF (MASTERCARD) para transacciones
autenticadas.
3ds_eci_value 3ds_version Opcional. Texto. Indicador de Comercio Electrónico.
Opcional. Texto. Versión del protocolo 3DS usado. Ejemplo: 2.1.
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
i. Ejemplo
+ =
Cobalt
{
"currency_code": "USD",
"amount": "600",
"tax": "10",
"tip": "0",
"pan": "4111111111111111",
"exp_date": "02/24",
3
1 2 3
"card_holder": "PRUEBA MTB CONTACTLESS",
LOGOTIPO
CORPORATIVO
"cvv2": "838",
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
"metas": {
El isotipo es el simbolo que
identifica a la marca.
LA MARCA
ÁREA DE
SEGURIDAD
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
"3ds_transaction_id": "747ed243-8a88-4b69-aa3e-4033dd84e847",
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
+
"3ds_authentication_value": "Ir4gQbAe7MZbd1GYk3AsrQ==",
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
"3ds_eci_value": "05"
}
Isotipo
logotipo
}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 15
e. PreAutorización
i. Endpoint: ii. Método: POST
iii. Parámetros
{{host}}/api/v2/transactions/pre_auth
Parámetro Tipo Descripción
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
amount Requerido. Numérico. Monto a cobrar expresado en centavos de dólar.
pan Requerido. Texto. Numeración de la tarjeta.
exp_date Requerido. Fecha. Fecha de vencimiento de la tarjeta. Formato: MM/YY.
currency_code Requerido. Texto. Acrónimo de la moneda. Para dólar: USD.
cvv2 Opcional. Texto. Código de Verficación de la tarjeta.
card_holder Opcional Texto. Nombre del titular de la tarjeta.
tax Opcional. Numérico. Valor de ITBMS expresado en centavos de dólar.
tip Opcional. Numérico. Valor de propina expresado en centavos de dólar.
+ =
Cobalt
metas Opcional. Array. Matriz Clave-Valor de datos adicionales a enviar.
iv. Respuesta
{
"status": "ok",
"message": "success",
"data": {
3
1 2 3
"id": 9245,
LOGOTIPO
CORPORATIVO
"identifier": 130009245,
El logotipo es el signo gráfico
"service_id": 21,
LA MARCA
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
"merchant_id": "123696969",
identifica a la marca.
"terminal_id": "CNTRGEEK",
+
"processor": "simulator",
"type": "pre_auth",
"status": "authorized",
Isotipo
logotipo
"ballot": "00000008",
"pan": "449187******5094",
"exp_date": "2023-09-01T00:00:00.000000Z",
"currency_code": "840",
"card_holder": "MC",
"amount": 100,
"tax": 0,
"reversal_tx": null,
"adjustment_tx": null,
"response_code": "00",
"authorization_number": "880115",
"reference_number": "047894276372",
"brand_reference": null,
"processed_at": "2023-04-25 23:50:00",
"created_at": "2023-04-25T23:49:58.000000Z",
"updated_at": "2023-04-25T23:50:00.000000Z",
"metadatas": {
"ip": "127.0.0.1",
"card_brand": "VISA"
}
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
}
}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 16
f. Ajuste
i. Endpoint: ii. Método: GET
iii. Parámetros
{{host}}/api/v2/transactions/adjustment/{{transaction_id}}
Parámetro Tipo Descripción
amount Opcional. Numérico. Monto a reembolsar expresado en centavos de dólar.
iv. Respuesta
{
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
"status": "ok",
"message": "success",
"data": {
+ =
Cobalt
"id": 9247,
"identifier": 130009247,
"service_id": 21,
"merchant_id": "123696969",
"terminal_id": "CNTRGEEK",
"processor": "simulator",
"type": "adjustment",
"status": "authorized",
"ballot": "00000008",
"pan": "449187******5094",
"exp_date": "2023-09-01T00:00:00.000000Z",
1 2 3
"currency_code": "840",
3
"card_holder": "MC",
LOGOTIPO
LA MARCA
CORPORATIVO
"amount": 100,
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
El logotipo es el signo gráfico
identificador de la marca en todas
"tax": 0,
cualquier soporte.
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
"reversal_tx": null,
"adjustment_tx": null,
+
"response_code": "00",
"authorization_number": "880115",
"reference_number": "047894276372",
Isotipo
logotipo
"brand_reference": null,
"processed_at": "2023-04-25 23:50:00",
"created_at": "2023-04-25T23:49:58.000000Z",
"updated_at": "2023-04-25T23:50:00.000000Z",
"metadatas": {
"ip": "127.0.0.1",
"card_brand": "VISA"
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
}
}
}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 17
g. Reembolso
i. Endpoint: ii. Método: GET
iii. Parámetros
{{host}}/api/v2/transactions/refund/{{transaction_id}}
Parámetro Tipo Descripción
amount Opcional. Numérico. Monto a reembolsar expresado en centavos de dólar.
iv. Respuesta
{
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
"status": "ok",
"message": "success",
"data": {
"identifier": 130280911,
"service_id": 21,
+ =
Cobalt
"merchant_id": "123696969",
"terminal_id": "CNTRGEEK",
"processor": "simulator",
"type": "reversal",
"status": "authorized",
"ballot": "00000009",
"pan": "449187******5094",
"exp_date": "2023-09-01T00:00:00.000000Z",
"currency_code": "840",
"card_holder": "MC",
"amount": 100,
3
1 2 3
"tax": 0,
LOGOTIPO
"reversal_tx": null,
LA MARCA
CORPORATIVO
Estas son las 4 variedades de uso,
El logotipo es el signo gráfico
"adjustment_tx": null,
pudiéndose adaptar sin problema a
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
"response_code": "00",
identifica a la marca.
"authorization_number": "765004",
+
"reference_number": "047894276372",
"brand_reference": null,
"updated_at": "2023-04-26T00:24:14.000000Z",
Isotipo
logotipo
"created_at": "2023-04-26T00:24:14.000000Z",
"id": 280911,
"metadatas": {
"over_transaction": "280910",
"ip": "127.0.0.1",
"card_brand": "VISA"
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
}
}
}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 18
h. Consultar datos de una Transacción
{{transaction_id}} i. Endpoint: {{host}}/api/v2/transactions/{{transaction_id}}
ii. Método: GET
El parámetro de ruta corresponde al atributo de las solicitudes de Venta, PreAutorización, Ajuste y Reembolso.
iii. Respuesta
{
id recibido en la respuesta
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
"status": "ok",
"message": "success",
"data": {
"identifier": 130280911,
"service_id": 21,
"merchant_id": "123696969",
"terminal_id": "CNTRGEEK",
+ =
Cobalt
"processor": "simulator",
"type": "reversal",
"status": "authorized",
"ballot": "00000009",
"pan": "449187******5094",
"exp_date": "2023-09-01T00:00:00.000000Z",
"currency_code": "840",
"card_holder": "MC",
"amount": 100,
"tax": 0,
"reversal_tx": null,
1 2 3
"adjustment_tx": null,
3
"response_code": "00",
LOGOTIPO
LA MARCA
CORPORATIVO
"authorization_number": "765004",
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
"reference_number": "047894276372",
cualquier soporte.
El isotipo es el simbolo que
identifica a la marca.
"brand_reference": null,
"updated_at": "2023-04-26T00:24:14.000000Z",
+
"created_at": "2023-04-26T00:24:14.000000Z",
"id": 280911,
"metadatas": {
Isotipo
"over_transaction": "280910",
"ip": "127.0.0.1",
"card_brand": "VISA"
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
}
logotipo
}
}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 19
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
i. Parámetros 3DS
Los comercios pueden solicitar que una transacción se procese con una verificación
segura del tarjehabiente. Esto permite asegurar al comercio que la transacción no es
producto de un fraude, y en la mayoría de los casos no están sujetas a contracargos ya
que el tarjehabiente autorizó de foma segura e inequívoca el pago.
Para que un comercio pueda disponer de esta característica debe estar registrado como
comercio seguro en nuestro sistema y enviar los siguientes parámetros bajo la matriz
3ds_params. En la respuesta se devolverá los detalles de la transacción. Si el estado de la
transacción es authenticating, en los metadatos se encontrará 3ds_authentication_form.
Este metadato contiene la URL del challenge que debe pasar el tarjehabiente para
+ =
Cobalt
procesar la transacción.
Cuando el usuario complete el challenge, la transacción será procesada y se enviará el
resultado del procesamiento a la URL definida en el parámetro webhook.
Puede ocurrir que aunque se envien los parámetros para la autenticación, la
3
1 2 3
transacción se procese si necesidad de un challenge. Esto es debido a que el banco
LOGOTIPO
LA MARCA
CORPORATIVO
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
emisor de la tarjeta no requiere autenticación. De igual manera, la transacción se
El logotipo es el signo gráfico
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
procesará con el criptograma de autenticación, por lo que quedará autenticada ante la
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
+
marca.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Parámetro Isotipo
logotipo
Tipo Descripción
deviceChannel Requerido. Texto. Indica el tipo de interfaz de canal que se utiliza
para iniciar la transacción. Valores válidos: app,
browser.
email Opcional. Correo. Máx 254
caracteres.
Correo electrónico del tarjehabiente.
billAddrCity Opcional. Texto. Máx 50
caracteres.
La ciudad de la dirección de facturación del
titular de la tarjeta asociada con la tarjeta
utilizada para esta compra.
billAddrCountry Opcional. Texto. Máx 3
caracteres. ISO 3166-1
El país de la dirección de facturación del titular
de la tarjeta asociada con la tarjeta utilizada
para esta compra.
billAddrLine1 Opcional. Texto. Máx 50
caracteres.
Primera línea de la dirección de la calle o parte
local equivalente de la dirección de facturación
del titular de la tarjeta asociada con la tarjeta
utilizada para esta compra.
billAddrLine2 Opcional. Texto. Máx 50
caracteres.
Segunda línea de la dirección de la calle o
parte local equivalente de la dirección de
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 20
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
facturación del titular de la tarjeta asociada
con la tarjeta utilizada para esta compra.
billAddrLine3 Opcional. Texto. Máx 50
caracteres.
Tercera línea de la dirección de la calle o parte
local equivalente de la dirección de facturación
del titular de la tarjeta asociada con la tarjeta
utilizada para esta compra.
billAddrPostCode Opcional. Texto. Máx 16
caracteres.
Código postal u otro código postal de la
dirección de facturación del titular de la tarjeta
asociada con la tarjeta utilizada para esta
compra.
billAddrState Opcional. Texto. Máx 3
caracteres.
El estado o provincia de la dirección de
facturación del titular de la tarjeta asociada
con la tarjeta utilizada para esta compra. Debe
cumplir con ISO_3166-2 .
+ =
Cobalt
purchaseInstalData Opcional. Entero. Min 1
caracteres. Máx 3 caracteres.
Indica el número máximo de autorizaciones
permitidas para pagos fraccionados. (Pagos
parciales). Valor por defecto 10.
recurringFrequency Opcional. Entero. Máx 4
caracteres.
Numero de días transcurridos entre pagos
recurrentes. Valor por defecto cuando exista
recurrencia se calculará el valor según lo
enviado en los datos recurrentes.
3
1 2 3
recurringExpiry Opcional. Fecha. Fecha después de la cual no se realizarán más
LOGOTIPO
LA MARCA
CORPORATIVO
Estas son las 4 variedades de uso,
El logotipo es el signo gráfico
pagos recurrentes. Si la recurrencia es hasta
pudiéndose adaptar sin problema a
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
ser cancelada, se usará fecha 2030-12-31.
identifica a la marca.
Formato: YYYY-MM-DD.
+
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
transType Opcional. Texto. Identifica el tipo de venta que se realiza.
Valores aceptados: goods, check,
account_funding, quasi_cash, prepaid_activiation.
La ciudad de la dirección de envío del titular
de la tarjeta asociada con la tarjeta utilizada
para esta compra.
El país de la dirección de envío del titular de la
tarjeta asociada con la tarjeta utilizada para
esta compra. Debe cumplir con ISO_3166-1
Primera línea de la dirección de la calle o parte
local equivalente de la dirección de envío del
titular de la tarjeta asociada con la tarjeta
utilizada para esta compra.
Segunda línea de la dirección de la calle o
parte local equivalente de la dirección de
envío del titular de la tarjeta asociada con la
tarjeta utilizada para esta compra.
Tercera línea de la dirección de la calle o parte
local equivalente de la dirección de envío del
Isotipo
logotipo
shipAddrCity Opcional. Texto. Máx 50
caracteres
shipAddrCountry Opcional. Texto. Máx 3
caracteres.
shipAddrLine1 Opcional. Texto. Máx 50
caracteres.
shipAddrLine2 Opcional. Texto. Máx 50
caracteres.
shipAddrLine3 Opcional. Texto. Máx 50
caracteres.
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 21
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
titular de la tarjeta asociada con la tarjeta
utilizada para esta compra.
shipAddrPostCode Opcional. Texto. Máx 16
caracteres.
Código postal u otro código postal de la
dirección de envío del titular de la tarjeta
asociada con la tarjeta utilizada para esta
compra.
shipAddrState Opcional. Texto. Máx 3
caracteres.
El estado o provincia de la dirección de envío
del titular de la tarjeta asociada con la tarjeta
utilizada para esta compra. Debe cumplir con
ISO_3166-2 .
shipIndicator Opcional. Texto. + =
Cobalt
Indica el método de envío elegido para la
transacción. Valores aceptados:
ship_to_cardholder_billing_address,
ship_to_another_verified_address,
ship_to_address_diff_cardholder_billing_address,
ship_to_store, digital_goods.
deliveryTimeframe Opcional. Texto. Indica el plazo de entrega de la mercancía.
Valores aceptados: electronic, same_day,
overnight, two_day_or_more.
deliveryEmailAddress Opcional. Correo. Máx 254
Para envío electrónico, la dirección de correo
caracteres.
electrónico a la que se entregó la mercancía.
3
1 2 3
reorderItemsInd Opcional. Texto. Indica si el titular de la tarjeta está
LOGOTIPO
LA MARCA
CORPORATIVO
Estas son las 4 variedades de uso,
El logotipo es el signo gráfico
reordenando mercancía comprada
pudiéndose adaptar sin problema a
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
previamente. Valores aceptados:
identifica a la marca.
first_time_ordered, reordered.
+
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
preOrderPurchaseInd Opcional. Texto. Indica si el titular de la tarjeta está realizando
un pedido de mercancía con disponibilidad o
fecha de lanzamiento futura. Valores
aceptados: merchandise_available,
future_availability.
preOrderDate Requerido si
preOrderPurchaseInd está
presente. Fecha.
Para una compra con pedido anticipado, la
fecha prevista en que la mercancía estará
disponible. Formato: YYYY-MM-DD.
gitfCardAmount Opcional. Entero. Máx 15
caracteres.
Para compras con tarjeta prepago o de regalo,
el monto total de la compra con tarjeta
prepago o de regalo.
giftCardCurr Opcional. Texto. Máx 3
caracteres.
Por defecto valor de currency. Para compras
con tarjetas prepago o de regalo, el código de
moneda de la tarjeta. De cumplir con
ISO_4217 .
giftCardCount Opcional. Entero. 2 Dígitos. Para compras de tarjetas prepago o de regalo,
recuento total de tarjetas/códigos prepago o
de regalo individuales comprados.
browserIP IP del navegador del tarjehabiente.
Isotipo
logotipo
Requerido si deviceChannel = Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 22
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
browser.
browserJavaEnabled Requerido si deviceChannel =
browser.
Booleano.
browserJavascriptEnabled Requerido si deviceChannel =
browser.
Booleano.
browserLanguage Requerido si deviceChannel =
browser.
Texto. Min 1 carácter . Máx 8
caracteres.
browserColorDepth Requerido si deviceChannel =
browser.
Entero.
Booleano que indica si el navegador del
tarjehabiente soporta Java. Ver JS*
navigator.JavaEnabled.
Booleano que indica si el navegador del
tarjehabiente soporta Javascript.
Idioma del navegador del tarjehabiente. Ver
navigator.language.
+ =
Cobalt
Valor que indica la profundidad de bits de la
paleta de colores para mostrar imágenes, en
bits por pixeles. Ver JS* screen.colorDepth.
Valores aceptados: 1, 4, 8, 15, 16, 24, 32, 48.
browserScreenHeight Requerido si deviceChannel =
browser.
Entero.
Altura total en pixeles de la pantalla del
tarjehabiente. Ver JS* screen.height.
browserScreenWidth Requerido si deviceChannel =
browser
Anchura total en pixeles de la pantalla del
tarjehabiente. Ver JS* screen.width.
browserTZ Requerido si deviceChannel =
1 2 3
Diferencia de tiempo entre hora UTC y hora
3
LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
browser.
local del navegador del tarjetahabiente.
LA MARCA
Estas son las 4 variedades de uso,
Entero. Min 1 caracteres. Máx 5
pudiéndose adaptar sin problema a
Expresado en minutos.
cualquier soporte.
caracateres.
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
+
El tamaño mínimo al que el
browserUserAgent Requerido si deviceChannel =
Contenido exacto de la cabecera HTTP User-
logotipo puede ser reproducido es
a 15 mm de ancho.
browser.
Agent. Ver JS* navigator.userAgent.
Isotipo
logotipo
Texto. Min 1 caracteres. Máx
2048 caracteres.
challengeWindowSize Requerido si deviceChannel =
browser.
Entero.
Anchura total en pixeles de la pantalla del
tarjehabiente. Ver JS* screen.width.
*Valor obtenido de la ejecución en Javascript.
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 23
j. Ejemplo:
{
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
"currency_code": "USD",
"amount": 115,
"tax": "0",
"tip": "0",
"pan": "5281******0033",
"exp_date": "07/27",
"card_holder": "PRUEBA 3DS",
"cvv2": "111",
"3ds_params": {
"deviceChannel": "browser",
"browserIP": "127.0.1.1",
"browserJavaEnabled": false,
"browserJavascriptEnabled": true,
"browserLanguage": "es",
"browserColorDepth": 24,
"browserScreenHeight": 1080,
+ =
Cobalt
"browserScreenWidth": 1920,
"browserTZ": "1",
"browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/130.0.0.0 Safari/537.36",
"challengeWindowSize": 1920
},
"webhook": "https://webhook.site/152ab34c-700a-4973-a1b3-34f7fbedbc37"
}
3
1 2 3
LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
+
LA MARCA
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 24
k. Respuesta:
{
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
"status": "ok",
"message": "success",
"data": {
"id": 25776,
"identifier": 130025776,
"service_id": 54,
"settlement_id": null,
"merchant_id": "123000010",
"terminal_id": "METRO001",
"processor": "simulator",
"type": "sale",
"status": "authenticating",
"ballot": "84948640",
"pan": "528150******0033",
"exp_date": "2027-07-01 00:00:00",
"currency_code": "840",
+ =
Cobalt
"card_holder": "PRUEBA 3DS",
"amount": 115,
"tax": 0,
"reversal_tx": null,
"adjustment_tx": null,
"response_code": null,
"authorization_number": null,
"reference_number": null,
"brand_reference": null,
"processed_at": null,
"compensated_at": null,
3
1 2 3
"created_at": "2024-11-26T22:10:01.000000Z",
LOGOTIPO
"updated_at": "2024-11-26T22:10:03.000000Z",
LA MARCA
CORPORATIVO
Estas son las 4 variedades de uso,
El logotipo es el signo gráfico
"metadatas": {
pudiéndose adaptar sin problema a
cualquier soporte.
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
"_pos_data_attended": "0",
identifica a la marca.
"_pos_data_location": "1",
+
"_pos_data_cardholder_presence": "0",
"_pos_data_card_presence": "1",
"_pos_data_retention_capacity": "0",
Isotipo
logotipo
"_pos_data_transaction_status": "0",
"_pos_data_transaction_security": "0",
"_pos_data_terminal_level": "6",
"tip": "0",
"ip": "181.198.252.169",
"3ds_params":
"{\"deviceChannel\":\"browser\",\"browserIP\":\"127.0.1.1\",\"browserJavaEnabled\":false,\"browserJavascriptEnabled\":true,\
"browserLanguage\":\"es\",\"browserColorDepth\":24,\"browserScreenHeight\":1080,\"browserScreenWidth\":1920,\"browser
TZ\":\"1\",\"browserUserAgent\":\"Mozilla\\/5.0 (X11; Linux x86_64) AppleWebKit\\/537.36 (KHTML, like Gecko)
Chrome\\/130.0.0.0
Safari\\/537.36\",\"challengeWindowSize\":1920,\"purchaseDate\":\"24Nov26221101\",\"threeDSRequestorDecMaxTime\":10,
\"acquirerCountry\":\"PA\",\"purchaseAmount\":115,\"purchaseCurrency\":\"840\",\"cardHolderName\":\"PRUEBA
3DS\",\"acctNumber\":\"5281509242240033\",\"cardExpiryDate\":\"2707\"}",
"webhook": "https://webhook.site/152ab34c-700a-4973-a1b3-34f7fbedbc37",
"card_brand": "MASTERCARD",
"lock_hash": "dc3b67a054ea48d65e65e81de2f5644a66e2c8a7a212b7abc6cec547a1f42656",
"3ds_version": "2.2.0",
"3ds_authentication_form": "https://cbotest.cobalt.tech/3ds/authenticate/25776"
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
}
}
}
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 25
6. HISTORIAL DE VERSIONES
VERSIÓN FECHA CAMBIOS
V1.0.0 2023-06-07• Versión inicial
V1.0.1 2023-11-21• Añadido historial de versiones
V1.1.0 2024-02-21• Añadidas operaciones de Pre-autorización y Ajuste
V1.2.0 2024-06-01• Documentación para transacciones autenticadas
V1.3.0 2024-08-19• Añadido endpoint de consultas de transacciones
0
INSPIRACIÓN
COBALT se inspira en la
combinación de varios elementos
que y colores que definen a la
marca.
El cobalto es un elemento químico
con un color azúl caracteristico.
En la construcción de la marca se
ha sitetizado la letra "o" de la
palabra cobalto en una piedra de
cobalto.
En conjunto la marca usa una gama
de color azul cobalto como color
representativo de la marca.
V1.3.1 2024-09-17• Corrección de parámetros de autenticación 3DS.
V2.0.0 + =
Cobalt
2024-10-23• Corrección de parámetros de autenticación 3DS.
• Añadido sistema de autenticación Oauth2
• API v2
V2.0.1 2024-11-01• Añadido enpoint de autorización Oauth2
V2.1.0 2024-11-26• Añadida documentación de autenticación 3DS nativa
V2.1.1 2024-12-06• Añadia documentación del proceso de autorizacion con tarjetas
tokenizadas
3
1 2 3
LOGOTIPO
CORPORATIVO
El logotipo es el signo gráfico
identificador de la marca en todas
las aplicaciones.
El isotipo es el simbolo que
identifica a la marca.
+
LA MARCA
Estas son las 4 variedades de uso,
pudiéndose adaptar sin problema a
cualquier soporte.
ÁREA DE
SEGURIDAD
Para asegurar la óptima aplicación
y percepción del logotipo se ha
determinado un área de seguridad
que establece una distancia
mínima respecto a los textos y
elementos gráficos equivalente a
altura del propio logotipo.
El tamaño mínimo al que el
logotipo puede ser reproducido es
a 15 mm de ancho.
Isotipo
logotipo
Cobalt Tech | www.cobalt.tech | API Transaccional v2.1.1 | 26