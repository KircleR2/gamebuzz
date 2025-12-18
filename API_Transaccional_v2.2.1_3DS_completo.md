# API Transaccional (v2.2.1) — 3DS (Autenticación 3-D Secure)

> Extracto completo y “limpio” de la sección **Parámetros 3DS** del PDF *API Transaccional v2.2.1* (NeoPayment).  
> Incluye explicación, lista completa de parámetros, ejemplo y respuesta.

---

## ¿Qué es 3DS en este API?
Los comercios pueden solicitar que una transacción se procese con una verificación segura del tarjehabiente (3DS). Esto:
- Ayuda a asegurar al comercio que la transacción no es producto de fraude.
- En la mayoría de los casos reduce la exposición a contracargos, ya que el tarjehabiente autorizó el pago de forma segura e inequívoca.

Para usar 3DS:
1. El comercio debe estar registrado como **comercio seguro** en el sistema.
2. Debe enviar los parámetros dentro de la matriz **`3ds_params`**.
3. Si la transacción queda en estado **`authenticating`**, en los metadatos vendrá **`3ds_authentication_form`** con la URL del challenge.
4. Cuando el usuario complete el challenge, la transacción se procesa y el resultado se envía a la URL definida en **`webhook`**.
5. Opcionalmente se puede enviar **`return_url`** para redirigir al usuario al finalizar el flujo.

Notas importantes:
- Puede ocurrir que, aunque se envíen parámetros para autenticación, la transacción se procese **sin challenge** (dependiendo del banco emisor).
- Aun así, la transacción se procesa con el criptograma, por lo que queda autenticada ante la marca.

---

## Reglas rápidas (requisitos)
- `3ds_params.deviceChannel` **Requerido**: `app` o `browser`.
- Si `3ds_params` está presente, **`webhook` es requerido**.
- Si `deviceChannel = "browser"`, hay un conjunto de campos **requeridos** (IP, userAgent, etc.).
- `preOrderDate` es **requerido** si `preOrderPurchaseInd` está presente.

---

## Parámetros soportados en `3ds_params`

### 1) Canal / contexto general
| Parámetro | Requerido | Tipo | Restricciones / Valores | Descripción |
|---|---:|---|---|---|
| `deviceChannel` | Sí | Texto | `app`, `browser` | Tipo de interfaz/canal usado para iniciar la transacción. |
| `email` | No | Correo | Máx 254 caracteres | Correo del tarjehabiente. |
| `transType` | No | Texto | `goods`, `check`, `account_funding`, `quasi_cash`, `prepaid_activiation` | Tipo de venta. |

### 2) Dirección de facturación (Billing)
| Parámetro | Requerido | Tipo | Restricciones | Descripción |
|---|---:|---|---|---|
| `billAddrCity` | No | Texto | Máx 50 | Ciudad de la dirección de facturación del titular. |
| `billAddrCountry` | No | Texto | Máx 3 (ISO 3166-1) | País de la dirección de facturación del titular. |
| `billAddrLine1` | No | Texto | Máx 50 | Línea 1 de la dirección de facturación. |
| `billAddrLine2` | No | Texto | Máx 50 | Línea 2 de la dirección de facturación. |
| `billAddrLine3` | No | Texto | Máx 50 | Línea 3 de la dirección de facturación. |
| `billAddrPostCode` | No | Texto | Máx 16 | Código postal (u otro) de la dirección de facturación. |
| `billAddrState` | No | Texto | Máx 3 (ISO 3166-2) | Estado/provincia de la dirección de facturación. |

### 3) Dirección de envío (Shipping)
| Parámetro | Requerido | Tipo | Restricciones | Descripción |
|---|---:|---|---|---|
| `shipAddrCity` | No | Texto | Máx 50 | Ciudad de la dirección de envío. |
| `shipAddrCountry` | No | Texto | Máx 3 (ISO 3166-1) | País de la dirección de envío. |
| `shipAddrLine1` | No | Texto | Máx 50 | Línea 1 de la dirección de envío. |
| `shipAddrLine2` | No | Texto | Máx 50 | Línea 2 de la dirección de envío. |
| `shipAddrLine3` | No | Texto | Máx 50 | Línea 3 de la dirección de envío. |
| `shipAddrPostCode` | No | Texto | Máx 16 | Código postal (u otro) de la dirección de envío. |
| `shipAddrState` | No | Texto | Máx 3 (ISO 3166-2) | Estado/provincia de la dirección de envío. |

### 4) Indicadores de envío / entrega
| Parámetro | Requerido | Tipo | Valores | Descripción |
|---|---:|---|---|---|
| `shipIndicator` | No | Texto | `ship_to_cardholder_billing_address`, `ship_to_another_verified_address`, `ship_to_address_diff_cardholder_billing_address`, `ship_to_store`, `digital_goods` | Método de envío elegido para la transacción. |
| `deliveryTimeframe` | No | Texto | `electronic`, `same_day`, `overnight`, `two_day_or_more` | Plazo de entrega de la mercancía. |
| `deliveryEmailAddress` | No | Correo | Máx 254 | Para envío electrónico: correo al que se entregó la mercancía. |
| `reorderItemsInd` | No | Texto | `first_time_ordered`, `reordered` | Indica si el titular reordena mercancía comprada previamente. |

### 5) Preorden
| Parámetro | Requerido | Tipo | Valores / Formato | Descripción |
|---|---:|---|---|---|
| `preOrderPurchaseInd` | No | Texto | `merchandise_available`, `future_availability` | Si la compra es un pedido con disponibilidad/lanzamiento futuro. |
| `preOrderDate` | Condicional | Fecha | `YYYY-MM-DD` | **Requerido si `preOrderPurchaseInd` está presente.** Fecha prevista de disponibilidad. |

### 6) Pagos fraccionados / recurrencia
| Parámetro | Requerido | Tipo | Restricciones / Formato | Descripción |
|---|---:|---|---|---|
| `purchaseInstalData` | No | Entero | Min 1, Máx 3 caracteres | Número máximo de autorizaciones para pagos fraccionados. Por defecto 10. |
| `recurringFrequency` | No | Entero | Máx 4 caracteres | Días entre pagos recurrentes. Por defecto, se calcula según datos recurrentes enviados. |
| `recurringExpiry` | No | Fecha | `YYYY-MM-DD` | Fecha después de la cual no se realizan más pagos recurrentes. Si es “hasta cancelar”, se usa `2030-12-31`. |

### 7) Tarjetas prepago / gift card
| Parámetro | Requerido | Tipo | Restricciones | Descripción |
|---|---:|---|---|---|
| `gitfCardAmount` | No | Entero | Máx 15 caracteres | Para compras con tarjeta prepago/de regalo: monto total. |
| `giftCardCurr` | No | Texto | Máx 3 (ISO 4217) | Por defecto toma `currency`. Código de moneda de la tarjeta. |
| `giftCardCount` | No | Entero | 2 dígitos | Recuento total de tarjetas/códigos individuales comprados. |

---

## Parámetros requeridos cuando `deviceChannel = "browser"`
> “*Valor obtenido de la ejecución en Javascript.*” (según doc)

| Parámetro | Requerido | Tipo | Restricciones / Valores | Descripción |
|---|---:|---|---|---|
| `browserIP` | Sí (browser) | Texto/IP | — | IP del navegador del tarjehabiente. |
| `browserJavaEnabled` | Sí (browser) | Booleano | — | Si el navegador soporta Java (`navigator.javaEnabled`). |
| `browserJavascriptEnabled` | Sí (browser) | Booleano | — | Si el navegador soporta Javascript. |
| `browserLanguage` | Sí (browser) | Texto | Min 1, Máx 8 | Idioma del navegador (`navigator.language`). |
| `browserColorDepth` | Sí (browser) | Entero | `1, 4, 8, 15, 16, 24, 32, 48` | Profundidad de color (`screen.colorDepth`). |
| `browserScreenHeight` | Sí (browser) | Entero | — | Altura total en pixeles (`screen.height`). |
| `browserScreenWidth` | Sí (browser) | Entero | — | Anchura total en pixeles (`screen.width`). |
| `browserTZ` | Sí (browser) | Entero | Min 1, Máx 5 | Diferencia UTC vs hora local en minutos. |
| `browserUserAgent` | Sí (browser) | Texto | Min 1, Máx 2048 | Contenido exacto del header HTTP User-Agent (`navigator.userAgent`). |
| `challengeWindowSize` | Sí (browser) | Entero | — | Tamaño de ventana del challenge. |

---

## Ejemplo completo (Venta con 3DS nativo)
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
    "browserUserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "challengeWindowSize": 1920
  },
  "webhook": "https://webhook.site/152ab34c-700a-4973-a1b3-34f7fbedbc37",
  "return_url": "https://my.web.site/order/xxxx"
}
```

---

## Respuesta de ejemplo (cuando queda en `authenticating`)
Puntos clave a notar:
- `status` de la transacción: `authenticating`
- En `metadatas` aparecen: `3ds_version` y `3ds_authentication_form` (URL del challenge)

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
      "tip": "0",
      "ip": "181.198.252.169",
      "webhook": "https://webhook.site/152ab34c-700a-4973-a1b3-34f7fbedbc37",
      "card_brand": "MASTERCARD",
      "lock_hash": "dc3b67a054ea48d65e65e81de2f5644a66e2c8a7a212b7abc6cec547a1f42656",
      "3ds_version": "2.2.0",
      "3ds_authentication_form": "https://cbotest.cobalt.tech/3ds/authenticate/25776",
      "3ds_params": "{"deviceChannel":"browser","browserIP":"127.0.1.1","browserJavaEnabled":false,"browserJavascriptEnabled":true,"browserLanguage":"es","browserColorDepth":24,"browserScreenHeight":1080,"browserScreenWidth":1920,"browserTZ":"1","browserUserAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36","challengeWindowSize":1920}"
    }
  }
}
```

---

## Implementación típica del flujo (resumen práctico)
1. Envías la **venta** con `3ds_params` + `webhook` (+ `return_url` si quieres redirect).
2. Si recibes `status = "authenticating"`, renderizas/abres la URL `metadatas.3ds_authentication_form`.
3. El usuario completa el challenge.
4. NeoPayment procesa la transacción y te envía el resultado al `webhook`.
5. Si configuraste `return_url`, puedes redirigir al usuario al final del flujo.

---

**Fuente:** API Transaccional v2.2.1 (NeoPayment), sección “Parámetros 3DS”.
