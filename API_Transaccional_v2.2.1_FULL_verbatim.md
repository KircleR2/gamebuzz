# API Transaccional — v2.2.1
**Documentación para VISA y Mastercard**  
**NeoPayment | neopayment.com**

> Exportado desde el PDF: *API Transaccional - V2.2.1.pdf* (27 páginas).  
> Nota: La portada contiene una imagen de fondo; el resto del contenido es texto/tablas/JSON.

---

## Página 1
API Transaccional  
Documentación para VISA y Mastercard  
NeoPayment | neopayment.com

---

## Página 2 — TABLA DE CONTENIDOS
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
Generación de token........................................................................................................................7  
TRANSACCIONES...................................................................................................................................9  
Lista de Transacciones......................................................................................................................9  
Venta..............................................................................................................................................11  
Transacciones con tarjeta tokenizada............................................................................................13  
Transacciones autenticadas...........................................................................................................15  
Facilitadores de Pago y Marketplace.............................................................................................16  
PreAutorización..............................................................................................................................17  
Ajuste.............................................................................................................................................18  
Reembolso.....................................................................................................................................19  
Consultar datos de una Transacción..............................................................................................20  
Parámetros 3DS..............................................................................................................................21  
HISTORIAL DE VERSIONES...................................................................................................................27  

neopayment | neopayment.com | API Transaccional v2.2.1 | 2

---

## Página 3 — 1. INTRODUCCIÓN
El API Transaccional permite procesar una transacción directamente desde API sin  
necesidad de una interfaz gráfica. Esta API está diseñada para comercios que manejen un  
gran volumen de transacciones y necesiten administrar de su lado los datos del cada  
cliente.  

Esta API actualmente soporta transacciones con tarjetas VISA y Mastercad. Para el  
procesamiento de tarjetas Clave solicite el servicio Checkout.  

Esta API soporta respuestas en formato JSON y formato XML según desee el desarrollador.  
Para dichos formatos será necesario enviar en el header Accept los valores application/json o  
application/xml respectivamente.  

neopayment | neopayment.com | API Transaccional v2.2.1 | 3

---

## Página 4 — 2. CONSIDERACIONES GENERALES
a. Tipos de Transacciones  
Existen diferentes tipos de transacciones. Esta API soporta transacciones de Ventas,  
Preautorizaciones, Ajustes, transacciones de Crédito y Reversa.  

Para realizar la reversa de una transacción es necesario indicar cuál es la transacción que se  
desea reversar (o anular) . Esta transacción debe de haber sido autorizada en el mismo día que  
se realiza la reversa. Si se desea reversar una transacción de días anteriores es necesario realizar  
una transacción de Crédito.  

b. Definición de claves  
i. {{host}}: URL proporcionada por la entidad.  
ii. {{client_id}}: ClientId entregado por la entidad.  
iii. {{client_secret}}: ClientSecret entregado por la entidad.  
iv. {{access_token}}: Token de acceso.  
v. {{transaction_id}}: ID de la transacción en el sistema CBO.  

c. Headers  
Para todas las llamadas es necesario enviar los siguientes headers:  

Header | Valor  
---|---  
Authorization | Bearer {{access_token}}  

neopayment | neopayment.com | API Transaccional v2.2.1 | 4

---

## Página 5 — 3. ERRORES Y ESTADOS
a. Composición de mensajes de error  

b. Códigos de error  

Código | Error | Descripción  
---|---|---  
400 | invalid_parameter | Ha fallado la validación de algún parámetro.  
401 | unauthorized_access | La autenticación proporcionada no es correcta. Revise las credenciales otorgadas.  

c. Estados de una transacción  
Una transacción puede tener varios estados durante el procesamiento.  

Estado | Descripción  
---|---  
pending | Estado inicial de una transacción. Indica que todavía está pendiente de ser procesada.  
authenticating | La transacción se encuentra pendiente de autenticación 3DS por parte del tarjehabiente.  
processing | La transacción se encuentra en procesamiento. La duración este estado puede ser de hasta 30 segundos.  
orphan | La transacción se envió a procesar pero no se obtuvo ningún tipo de respuesta.  
authorized | La transacción se ha procesado y el cobro fue autorizado por el banco emisor de la tarjeta.  
denied | La transacción se ha procesado pero el cobro fue denegado por el banco emisor de la tarjeta. Revise la razón en el valor response_code.  
refused | La transacción ha sido rechazada por el sistema y no se ha procesado debido a algún tipo de incumplimiento comercial.  

```json
{
 "status": "error",
 "message": "Invalid parameters",
 "data": {
  "amount": [
   "El parámetro amount es requerido"
  ]
 },
 "error": "invalid_parameter"
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 5

---

## Página 6
neopayment | neopayment.com | API Transaccional v2.2.1 | 6

---

## Página 7 — 4. AUTORIZACIÓN
Esta API utiliza el estandar OAuth2 para la autorización segura del uso de los endpoints  
expuestos. El proceso de autorización se compone de un client_id y un client_secret. Estos  
elementos se envían en una petición POST para obtener un token de autorización válido  
para ser usado en cualquiera de los enpoints. Se debe tener en cuenta que este token tiene  
un tiempo de expiración y serán necesario volver a generar uno nuevo cuando este haya  
expirado.  

a. Generación de token  
i. Endpoint: {{host}}/oauth/token  
ii. Método: POST  

iii. Parámetros  

Parámetro | Tipo | Descripción  
---|---|---  
grant_type | Requerido. Texto. | Valor fijo: client_credentials.  
client_id | Requerido. Texto. | Cliend ID generado para el servicio comercial.  
client_secret | Requerido. Texto. | Client Secret generado para el servicio comercial.  

b. Ejemplo  

```json
{
 "grant_type": "client_credentials",
 "client_id": "9d44c02a-ea81-4e9a-bacb-10c68fcdf776",
 "client_secret": "1L0EAhrQklxe9gQ43G4rynwIzaptwSDkrH4Yg1gG"
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 7

---

## Página 8 — c. Respuesta

```json
{
 "token_type": "Bearer",
 "expires_in": 86400,
 "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZDQ0YzAyYS1lYTgxLTRlOWEtYmFjYi0xMG
M2OGZjZGY3NzYiLCJqdGkiOiI5ODAyNzMxOTk4YzM4NDdiNjljNDE4OGZlMGEyOTBjYzViYTY4YzkyM
DA0MjNlYzAzNmY0YzgxYmE3OWI2MDZmMjRhYTVhN2IxNTM5YzNkNyIsImlhdCI6MTcyOTI2MTA5N
y40NTYyOTUsIm5iZiI6MTcyOTI2MTA5Ny40NTYyOTgsImV4cCI6MTcyOTM0NzQ5Ny40NTI1NTQsInN
1YiI6IiIsInNjb3BlcyI6W119.fqkSmSrrG6xaY4yXXm1nhUoL86kIf5s1Nfn1brMDVPueB_NmC0GWVWx
DyXLYbiuiIV9X5em_Y-lSCWBIcg89yfB￾KgMtohYWroSRdKJi1EHX5GwVecKrzQ1fwHF06IHjnJMC4rTlYDkqLGOKwarLBywWreu4GNscihNq4u
RIbSX8b7C6sB2TQeBiTiB84O5FWhNEhueHVtZiDIsMzWV7xfeea64-jfPQT3b2-
wkR4PJ_3sxMnp_E83DcrQR_ujConIdYblZSrhd6p2ks3n7faQWyNI6gOHHdVFleV7nr5jkhRX_LFAUo1
hovwryr1cUQEHjHmmxni4vGqY9c1mgXca_oCVX5El90z-tTxwRJSc35qMpZ86wO-W7-
8ONRXx8Fz0oUgfvsFQnQCkvc8cHocm8wkLSjvDKRMgjCQ9jvEynil0000Q3_vbhSWKkPUihelD_78yK
03bY8LmiqilbHuBDNFD74ZocwfB5v4oKf5rBzv47r7pm8E5W0-
7jW1QlKF1lrIvrCLPwUzdXNJ6lGEH4LgLCWI7hGvPi__qBJepOtypYKFgkNWp6HwTxagDm4zJlxSrsaPp
0dSpbywlSZQuKfHa8EhkVSvwycgxHQ1lM5NjUNTxXQpzOJT_ryvyNfv3yR7vWqabDxIzB40JPi0jHYP
W0Vi9R1SGfBdXoumQI"
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 8

---

## Página 9 — 5. TRANSACCIONES
a. Lista de Transacciones  
i. Endpoint: {{host}}/api/v2/transactions  
ii. Método: GET  

iii. Parámetros  

Parámetro | Tipo | Descripción  
---|---|---  
limit | Opcional. Numérico. | Límite máximo de transacciones a devolver. Por defecto 20.  
page | Opcional. Numérico. | Página de la lista transacciones. Por defecto 1.  
start_date | Opcional. Fecha. | Fecha inicial del rango que comprenderá la lista de los resultados devueltos. Formato: YYYY-MM-DD.  
end_date | Opcional. Fecha. | Fecha final del rango que comprenderá la lista de los resultados devueltos. Formato: YYYY-MM-DD.  

neopayment | neopayment.com | API Transaccional v2.2.1 | 9

---

## Página 10 — iv. Respuesta

```json
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
    "updated_at": "2023-04-25T13:10:10.000000Z",
    "metadatas": {
     "ip": "127.0.0.1",
     "card_brand": "VISA"
    }
   }
  ],
  "first_page_url": "http://cbo.local/api/transactions?limit=1&page=1",
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
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 10

---

## Página 11 — b. Venta
i. Endpoint: {{host}}/api/v2/transactions/sale  
ii. Método: POST  

iii. Parámetros  

Parámetro | Tipo | Descripción  
---|---|---  
amount | Requerido. Numérico. | Monto a cobrar expresado en centavos de dólar.  
pan | Requerido. Texto. | Numeración de la tarjeta.  
exp_date | Requerido. Fecha. | Fecha de vencimiento de la tarjeta. Formato: MM/YY.  
currency_code | Requerido. Texto. | Acrónimo de la moneda. Para dólar: USD.  
cvv2 | Opcional. Texto. | Código de Verficación de la tarjeta.  
card_holder | Opcional Texto. | Nombre del titular de la tarjeta.  
tax | Opcional. Numérico. | Valor de ITBMS expresado en centavos de dólar.  
tip | Opcional. Numérico. | Valor de propina expresado en centavos de dólar.  
metas | Opcional. Array. | Matriz Clave-Valor de datos adicionales a enviar.  
3ds_params | Opcional. Array. | Matriz Clave-Valor de datos para la autenticación 3DS. Ver sección Parámetros 3DS.  
webhook | Requerido si 3ds_params está presente. | URL del comercio donde se enviará el resultado de la transacción.  

iv. Ejemplo  

```json
{
 "currency_code": "USD",
 "amount": "100",
 "tax": "0",
 "tip": "0",
 "pan": "4491870000005094",
 "exp_date": "09/23",
 "card_holder": "MC"
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 11

---

## Página 12 — v. Respuesta

```json
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
  "metadatas": {
   "ip": "127.0.0.1",
   "card_brand": "VISA"
  }
 }
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 12

---

## Página 13 — c. Transacciones con tarjeta tokenizada
El API Transaccional permite el procesamiento de transacciones con tarjetas tokenizadas bajo  
nuestro sistema.  

Una tarjeta tokenizada es una tarjeta donde el comercio previamente nos comparte los datos  
de la tarjeta y es almacenada de forma segura en nuestro sistema. En este proceso el comercio  
obtiene un token que podrá usar posteriormente cuando requiera realizar transacciones sin  
necesidad de volver a enviar los datos de la tarjeta. En su lugar enviará el token generado por  
nuestro sistema. Para más información del proceso de tokenización consulte la documentación  
del API Bóveda de clientes.  

Cuando se usa un token, los parametros pan, exp_date y card_holder no serán necesarios. Sin  
embargo se requiere el parámetro customer_token que tendrá como valor el token generado.  

i. Ejemplo  

```json
{
 "currency_code": "USD",
 "amount": "98440",
 "tax": 0,
 "customer_token": "4pc3CiAj8ZTiUEYlq54JeVfvPX3crQSY",
 "type": "sale",
 "tip": 0
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 13

---

## Página 14 — ii. Respuesta

```json
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
  "metadatas": {
   "ip": "127.0.0.1",
   "card_brand": "VISA"
  }
 }
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 14

---

## Página 15 — d. Transacciones autenticadas
Es posible enviar una transacción autenticada por un proveedor ACS externo. Para ello el  
comercio debe disponer de un servicio ACS para realizar dicha autenticación y posteriormente  
enviar los datos generados por el autenticador. Estos datos se enviarán dentro de la matriz JSON  
metas. Estos son los parámetros soportados:  

Parámetro | Tipo | Descripción  
---|---|---  
3ds_transaction_id | Opcional. Texto. | Directory Server Transaction ID (DSTID) único generado por el servidor comercial ACS para identificar la transacción.  
3ds_authentication_value | Opcional. Texto. | Valor de CAVV (VISA) o UCAF (MASTERCARD) para transacciones autenticadas.  
3ds_eci_value | Opcional. Texto. | Indicador de Comercio Electrónico.  
3ds_version | Opcional. Texto. | Versión del protocolo 3DS usado. Ejemplo: 2.1.  

i. Ejemplo  

```json
{
 "currency_code": "USD",
 "amount": "600",
 "tax": "10",
 "tip": "0",
 "pan": "4111111111111111",
 "exp_date": "02/24",
 "card_holder": "PRUEBA MTB CONTACTLESS",
 "cvv2": "838",
 "metas": {
  "3ds_transaction_id": "747ed243-8a88-4b69-aa3e-4033dd84e847",
  "3ds_authentication_value": "Ir4gQbAe7MZbd1GYk3AsrQ==",
  "3ds_eci_value": "05"
 }
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 15

---

## Página 16 — e. Facilitadores de Pago y Marketplace
Nuestra API soporta el procesamiento de transacciones para facilitadores de pago y  
marketplace. Antes de procesar este tipo de transacciones necesitará comunicarlo a su entidad  
colaboradora, la cual indicará como proceder. Tenga en cuenta que el facilitador de pagos  
deberá estar debidamente registrado en las marcas soportadas.  

Los datos de procesamiento a través de un facilitador de pagos se enviarán bajo el parámetro  
payment_facilitator_data. Estos son los datos admitidos:  

Parámetro | Tipo | Descripción  
---|---|---  
payment_facilitator_id | Opcional. Texto. | Identificador del facilitador de pago registrado.  
descriptor | Opcional. Texto. | Nombre abreviado del facilitador de pago y el comercio patrocinado.  
sales_org_id | Opcional. Texto. | Identificación de la Organización Independiente de Ventas registrado. Requerido para Mastercard.  
sub_merchant_id | Opcional. Texto. | Identificación del comercio patrocinado.  
sub_merchant_city | Opcional. Texto. | Nombre de la ciudad del comercio patrocinado.  
sub_merchant_country | Opcional. Texto. | Código número ISO 3166-1 del país de origen del comercio patrocinado.  

i. Ejemplo  

```json
{
 "currency_code": "USD",
 "amount": 120,
 "tax": "0",
 "tip": "0",
 "pan": "4111111111111111",
 "exp_date": "07/26",
 "cvv2": "543",
 "card_holder": "Pruebas 3DS",
 "webhook": "https://webhook.site/a034b6ae-a71f-4972-a097-3c724425dce5",
 "payment_facilitator_data": {
  "payment_facilitator_id": "987654321",
  "descriptor": "HG*DUCROS, S.L.",
  "sub_merchant_city": "DAULE",
  "sub_merchant_country": "591",
  "sub_merchant_id": "0123456789"
 }
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 16

---

## Página 17 — f. PreAutorización
i. Endpoint: {{host}}/api/v2/transactions/pre_auth  
ii. Método: POST  

iii. Parámetros  

Parámetro | Tipo | Descripción  
---|---|---  
amount | Requerido. Numérico. | Monto a cobrar expresado en centavos de dólar.  
pan | Requerido. Texto. | Numeración de la tarjeta.  
exp_date | Requerido. Fecha. | Fecha de vencimiento de la tarjeta. Formato: MM/YY.  
currency_code | Requerido. Texto. | Acrónimo de la moneda. Para dólar: USD.  
cvv2 | Opcional. Texto. | Código de Verficación de la tarjeta.  
card_holder | Opcional Texto. | Nombre del titular de la tarjeta.  
tax | Opcional. Numérico. | Valor de ITBMS expresado en centavos de dólar.  
tip | Opcional. Numérico. | Valor de propina expresado en centavos de dólar.  
metas | Opcional. Array. | Matriz Clave-Valor de datos adicionales a enviar.  

iv. Respuesta  

```json
{
 "status": "ok",
 "message": "success",
 "data": {
  "id": 9245,
  "identifier": 130009245,
  "service_id": 21,
  "merchant_id": "123696969",
  "terminal_id": "CNTRGEEK",
  "processor": "simulator",
  "type": "pre_auth",
  "status": "authorized",
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
 }
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 17

---

## Página 18 — g. Ajuste
i. Endpoint: {{host}}/api/v2/transactions/adjustment/{{transaction_id}}  
ii. Método: GET  

iii. Parámetros  

Parámetro | Tipo | Descripción  
---|---|---  
amount | Opcional. Numérico. | Monto a reembolsar expresado en centavos de dólar.  

iv. Respuesta  

```json
{
 "status": "ok",
 "message": "success",
 "data": {
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
 }
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 18

---

## Página 19 — h. Reembolso
i. Endpoint: {{host}}/api/v2/transactions/refund/{{transaction_id}}  
ii. Método: GET  

iii. Parámetros  

Parámetro | Tipo | Descripción  
---|---|---  
amount | Opcional. Numérico. | Monto a reembolsar expresado en centavos de dólar.  

iv. Respuesta  

```json
{
 "status": "ok",
 "message": "success",
 "data": {
  "identifier": 130280911,
  "service_id": 21,
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
  "tax": 0,
  "reversal_tx": null,
  "adjustment_tx": null,
  "response_code": "00",
  "authorization_number": "765004",
  "reference_number": "047894276372",
  "brand_reference": null,
  "updated_at": "2023-04-26T00:24:14.000000Z",
  "created_at": "2023-04-26T00:24:14.000000Z",
  "id": 280911,
  "metadatas": {
   "over_transaction": "280910",
   "ip": "127.0.0.1",
   "card_brand": "VISA"
  }
 }
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 19

---

## Página 20 — i. Consultar datos de una Transacción
i. Endpoint: {{host}}/api/v2/transactions/{{transaction_id}}  
ii. Método: GET  

El parámetro de ruta {{transaction_id}} corresponde al atributo id recibido en la respuesta  
de las solicitudes de Venta, PreAutorización, Ajuste y Reembolso.  

iii. Respuesta  

```json
{
 "status": "ok",
 "message": "success",
 "data": {
  "identifier": 130280911,
  "service_id": 21,
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
  "tax": 0,
  "reversal_tx": null,
  "adjustment_tx": null,
  "response_code": "00",
  "authorization_number": "765004",
  "reference_number": "047894276372",
  "brand_reference": null,
  "updated_at": "2023-04-26T00:24:14.000000Z",
  "created_at": "2023-04-26T00:24:14.000000Z",
  "id": 280911,
  "metadatas": {
   "over_transaction": "280910",
   "ip": "127.0.0.1",
   "card_brand": "VISA"
  }
 }
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 20

---

## Página 21 — j. Parámetros 3DS
Los comercios pueden solicitar que una transacción se procese con una verificación  
segura del tarjehabiente. Esto permite asegurar al comercio que la transacción no es  
producto de un fraude, y en la mayoría de los casos no están sujetas a contracargos ya  
que el tarjehabiente autorizó de foma segura e inequívoca el pago.  

Para que un comercio pueda disponer de esta característica debe estar registrado como  
comercio seguro en nuestro sistema y enviar los siguientes parámetros bajo la matriz  
3ds_params. En la respuesta se devolverá los detalles de la transacción. Si el estado de la  
transacción es authenticating, en los metadatos se encontrará 3ds_authentication_form.  
Este metadato contiene la URL del challenge que debe pasar el tarjehabiente para  
procesar la transacción.  

Cuando el usuario complete el challenge, la transacción será procesada y se enviará el  
resultado del procesamiento a la URL definida en el parámetro webhook. Adicional se  
puede enviar el parámetro return_url, el se entiende como una URL para la redirección  
del usuario al finalizar el flujo.  

Puede ocurrir que aunque se envien los parámetros para la autenticación, la  
transacción se procese si necesidad de un challenge. Esto es debido a que el banco  
emisor de la tarjeta no requiere autenticación. De igual manera, la transacción se  
procesará con el criptograma de autenticación, por lo que quedará autenticada ante la  
marca.  

Parámetro | Tipo | Descripción  
---|---|---  
deviceChannel | Requerido. Texto. | Indica el tipo de interfaz de canal que se utiliza para iniciar la transacción. Valores válidos: app, browser.  
email | Opcional. Correo. Máx 254 caracteres. | Correo electrónico del tarjehabiente.  
billAddrCity | Opcional. Texto. Máx 50 caracteres. | La ciudad de la dirección de facturación del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  
billAddrCountry | Opcional. Texto. Máx 3 caracteres. ISO 3166-1 | El país de la dirección de facturación del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  
billAddrLine1 | Opcional. Texto. Máx 50 caracteres. | Primera línea de la dirección de la calle o parte local equivalente de la dirección de facturación del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  

neopayment | neopayment.com | API Transaccional v2.2.1 | 21

---

## Página 22 — Parámetros 3DS (continuación)
billAddrLine2 Opcional. Texto. Máx 50 caracteres. Segunda línea de la dirección de la calle o parte local equivalente de la dirección de facturación del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  
billAddrLine3 Opcional. Texto. Máx 50 caracteres. Tercera línea de la dirección de la calle o parte local equivalente de la dirección de facturación del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  
billAddrPostCode Opcional. Texto. Máx 16 caracteres. Código postal u otro código postal de la dirección de facturación del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  
billAddrState Opcional. Texto. Máx 3 caracteres. El estado o provincia de la dirección de facturación del titular de la tarjeta asociada con la tarjeta utilizada para esta compra. Debe cumplir con ISO_3166-2 .  
purchaseInstalData Opcional. Entero. Min 1 caracteres. Máx 3 caracteres. Indica el número máximo de autorizaciones permitidas para pagos fraccionados. (Pagos parciales). Valor por defecto 10.  
recurringFrequency Opcional. Entero. Máx 4 caracteres. Numero de días transcurridos entre pagos recurrentes. Valor por defecto cuando exista recurrencia se calculará el valor según lo enviado en los datos recurrentes.  
recurringExpiry Opcional. Fecha. Fecha después de la cual no se realizarán más pagos recurrentes. Si la recurrencia es hasta ser cancelada, se usará fecha 2030-12-31. Formato: YYYY-MM-DD.  
transType Opcional. Texto. Identifica el tipo de venta que se realiza. Valores aceptados: goods, check, account_funding, quasi_cash, prepaid_activiation.  
shipAddrCity Opcional. Texto. Máx 50 caracteres La ciudad de la dirección de envío del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  
shipAddrCountry Opcional. Texto. Máx 3 caracteres. El país de la dirección de envío del titular de la tarjeta asociada con la tarjeta utilizada para esta compra. Debe cumplir con ISO_3166-1  
shipAddrLine1 Opcional. Texto. Máx 50 caracteres. Primera línea de la dirección de la calle o parte local equivalente de la dirección de envío del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  
shipAddrLine2 Opcional. Texto. Máx 50 caracteres. Segunda línea de la dirección de la calle o parte local equivalente de la dirección de envío del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  

neopayment | neopayment.com | API Transaccional v2.2.1 | 22

---

## Página 23 — Parámetros 3DS (continuación)
shipAddrLine3 Opcional. Texto. Máx 50 caracteres. Tercera línea de la dirección de la calle o parte local equivalente de la dirección de envío del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  
shipAddrPostCode Opcional. Texto. Máx 16 caracteres. Código postal u otro código postal de la dirección de envío del titular de la tarjeta asociada con la tarjeta utilizada para esta compra.  
shipAddrState Opcional. Texto. Máx 3 caracteres. El estado o provincia de la dirección de envío del titular de la tarjeta asociada con la tarjeta utilizada para esta compra. Debe cumplir con ISO_3166-2 .  
shipIndicator Opcional. Texto. Indica el método de envío elegido para la transacción. Valores aceptados: ship_to_cardholder_billing_address, ship_to_another_verified_address, ship_to_address_diff_cardholder_billing_address, ship_to_store, digital_goods.  
deliveryTimeframe Opcional. Texto. Indica el plazo de entrega de la mercancía. Valores aceptados: electronic, same_day, overnight, two_day_or_more.  
deliveryEmailAddress Opcional. Correo. Máx 254 caracteres. Para envío electrónico, la dirección de correo electrónico a la que se entregó la mercancía.  
reorderItemsInd Opcional. Texto. Indica si el titular de la tarjeta está reordenando mercancía comprada previamente. Valores aceptados: first_time_ordered, reordered.  
preOrderPurchaseInd Opcional. Texto. Indica si el titular de la tarjeta está realizando un pedido de mercancía con disponibilidad o fecha de lanzamiento futura. Valores aceptados: merchandise_available, future_availability.  
preOrderDate Requerido si preOrderPurchaseInd está presente. Fecha. Para una compra con pedido anticipado, la fecha prevista en que la mercancía estará disponible. Formato: YYYY-MM-DD.  
gitfCardAmount Opcional. Entero. Máx 15 caracteres. Para compras con tarjeta prepago o de regalo, el monto total de la compra con tarjeta prepago o de regalo.  
giftCardCurr Opcional. Texto. Máx 3 caracteres. Por defecto valor de currency. Para compras con tarjetas prepago o de regalo, el código de moneda de la tarjeta. De cumplir con ISO_4217 .  
giftCardCount Opcional. Entero. 2 Dígitos. Para compras de tarjetas prepago o de regalo, recuento total de tarjetas/códigos prepago o de regalo individuales comprados.  

neopayment | neopayment.com | API Transaccional v2.2.1 | 23

---

## Página 24 — Parámetros 3DS (browser)
browserIP Requerido si deviceChannel = browser. IP del navegador del tarjehabiente.  
browserJavaEnabled Requerido si deviceChannel = browser. Booleano. Booleano que indica si el navegador del tarjehabiente soporta Java. Ver JS* navigator.JavaEnabled.  
browserJavascriptEnabled Requerido si deviceChannel = browser. Booleano. Booleano que indica si el navegador del tarjehabiente soporta Javascript.  
browserLanguage Requerido si deviceChannel = browser. Texto. Min 1 carácter . Máx 8 caracteres. Idioma del navegador del tarjehabiente. Ver navigator.language.  
browserColorDepth Requerido si deviceChannel = browser. Entero. Valor que indica la profundidad de bits de la paleta de colores para mostrar imágenes, en bits por pixeles. Ver JS* screen.colorDepth. Valores aceptados: 1, 4, 8, 15, 16, 24, 32, 48.  
browserScreenHeight Requerido si deviceChannel = browser. Entero. Altura total en pixeles de la pantalla del tarjehabiente. Ver JS* screen.height.  
browserScreenWidth Requerido si deviceChannel = browser Anchura total en pixeles de la pantalla del tarjehabiente. Ver JS* screen.width.  
browserTZ Requerido si deviceChannel = browser. Entero. Min 1 caracteres. Máx 5 caracateres. Diferencia de tiempo entre hora UTC y hora local del navegador del tarjetahabiente. Expresado en minutos.  
browserUserAgent Requerido si deviceChannel = browser. Texto. Min 1 caracteres. Máx 2048 caracteres. Contenido exacto de la cabecera HTTP User-Agent. Ver JS* navigator.userAgent.  
challengeWindowSize Requerido si deviceChannel = browser. Entero. Anchura total en pixeles de la pantalla del tarjehabiente. Ver JS* screen.width.  
*Valor obtenido de la ejecución en Javascript.  

neopayment | neopayment.com | API Transaccional v2.2.1 | 24

---

## Página 25 — k. Ejemplo
```json
{
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
  "browserScreenWidth": 1920,
  "browserTZ": "1",
  "browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) 
Chrome/130.0.0.0 Safari/537.36",
  "challengeWindowSize": 1920
 },
 "webhook": "https://webhook.site/152ab34c-700a-4973-a1b3-34f7fbedbc37",
 "return_url": "https://my.web.site/order/xxxx"
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 25

---

## Página 26 — l. Respuesta
```json
{
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
  "created_at": "2024-11-26T22:10:01.000000Z",
  "updated_at": "2024-11-26T22:10:03.000000Z",
  "metadatas": {
   "_pos_data_attended": "0",
   "_pos_data_location": "1",
   "_pos_data_cardholder_presence": "0",
   "_pos_data_card_presence": "1",
   "_pos_data_retention_capacity": "0",
   "_pos_data_transaction_status": "0",
   "_pos_data_transaction_security": "0",
   "_pos_data_terminal_level": "6",
   "tip": "0",
   "ip": "181.198.252.169",
   "3ds_params": 
"{\"deviceChannel\":\"browser\",\"browserIP\":\"127.0.1.1\",\"browserJavaEnabled\":false,\\"browserJavascriptEnabled\":true,\
\"browserLanguage\":\"es\",\"browserColorDepth\":24,\\"browserScreenHeight\":1080,\\"browserScreenWidth\":1920,\\"browser
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
  }
 }
}
```

neopayment | neopayment.com | API Transaccional v2.2.1 | 26

---

## Página 27 — 6. HISTORIAL DE VERSIONES
VERSIÓN | FECHA | CAMBIOS  
---|---|---  
V1.0.0 | 2023-06-07 | • Versión inicial  
V1.0.1 | 2023-11-21 | • Añadido historial de versiones  
V1.1.0 | 2024-02-21 | • Añadidas operaciones de Pre-autorización y Ajuste  
V1.2.0 | 2024-06-01 | • Documentación para transacciones autenticadas  
V1.3.0 | 2024-08-19 | • Añadido endpoint de consultas de transacciones  
V1.3.1 | 2024-09-17 | • Corrección de parámetros de autenticación 3DS.  
V2.0.0 | 2024-10-23 | • Corrección de parámetros de autenticación 3DS. • Añadido sistema de autenticación Oauth2 • API v2  
V2.0.1 | 2024-11-01 | • Añadido enpoint de autorización Oauth2  
V2.1.0 | 2024-11-26 | • Añadida documentación de autenticación 3DS nativa  
V2.1.1 | 2024-12-06 | • Añadia documentación del proceso de autorizacion con tarjetas tokenizadas  
V2.2.0 | 2024-12-13 | • Añadido soporte para facilitadores de pago y marketplaces.  
V2.2.1 | 2025-01-15 | • Añadido parámetro return_url en uso para escenario 3DS.  

neopayment | neopayment.com | API Transaccional v2.2.1 | 27
