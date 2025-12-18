"""
Cobalt Payment Gateway Integration
API Documentation: Cobalt Tech API Transaccional v2.1.1
Supports VISA and Mastercard transactions
"""

import requests
import logging
from datetime import datetime, timedelta
from django.conf import settings

logger = logging.getLogger(__name__)


class CobaltPaymentError(Exception):
    """Custom exception for Cobalt payment errors"""
    def __init__(self, message, error_code=None, response_data=None):
        self.message = message
        self.error_code = error_code
        self.response_data = response_data
        super().__init__(self.message)


class CobaltPaymentGateway:
    """
    Cobalt Payment Gateway Client
    
    Usage:
        gateway = CobaltPaymentGateway()
        
        # Process a sale
        result = gateway.process_sale(
            amount=1000,  # $10.00 in cents
            pan="4111111111111111",
            exp_date="12/25",
            cvv2="123",
            card_holder="John Doe"
        )
        
        if result['status'] == 'authorized':
            print("Payment successful!")
    """
    
    # Token cache
    _access_token = None
    _token_expires_at = None
    
    def __init__(self):
        self.host = settings.COBALT_HOST
        self.client_id = settings.COBALT_CLIENT_ID
        self.client_secret = settings.COBALT_CLIENT_SECRET
        
    def _get_access_token(self):
        """
        Get OAuth2 access token from Cobalt API.
        Caches the token until it expires.
        """
        # Check if we have a valid cached token
        if (CobaltPaymentGateway._access_token and 
            CobaltPaymentGateway._token_expires_at and 
            datetime.now() < CobaltPaymentGateway._token_expires_at):
            return CobaltPaymentGateway._access_token
        
        # Request new token
        url = f"{self.host}/oauth/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Cache the token
            CobaltPaymentGateway._access_token = data['access_token']
            expires_in = data.get('expires_in', 86400)  # Default 24 hours
            CobaltPaymentGateway._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            
            logger.info("Cobalt OAuth token obtained successfully")
            return CobaltPaymentGateway._access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to obtain Cobalt OAuth token: {e}")
            raise CobaltPaymentError(
                message="Error de autenticación con el procesador de pagos",
                error_code="auth_failed"
            )
    
    def _get_headers(self):
        """Get headers with authorization token"""
        token = self._get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def process_sale(
        self,
        amount,
        pan,
        exp_date,
        cvv2=None,
        card_holder=None,
        tax=0,
        tip=0,
        metas=None,
        currency_code="USD",
        three_ds_params=None,
        webhook=None,
        return_url=None,
    ):
        """
        Process a sale transaction.
        
        Args:
            amount: Amount in cents (e.g., 1000 = $10.00)
            pan: Card number (16 digits)
            exp_date: Expiration date in MM/YY format
            cvv2: Card verification code (optional but recommended)
            card_holder: Name on card (optional)
            tax: Tax amount in cents (optional)
            tip: Tip amount in cents (optional)
            metas: Additional metadata dict (optional)
            currency_code: Currency code (default: USD)
            
        Returns:
            dict with transaction result including:
            - id: Transaction ID
            - identifier: Full identifier
            - status: Transaction status (authorized, denied, etc.)
            - authorization_number: Auth code if approved
            - response_code: Response code
            - pan: Masked card number
        """
        url = f"{self.host}/api/v2/transactions/sale"
        
        payload = {
            "currency_code": currency_code,
            "amount": str(amount),
            "tax": str(tax),
            "tip": str(tip),
            "pan": pan,
            "exp_date": exp_date,
        }
        
        if cvv2:
            payload["cvv2"] = cvv2
        if card_holder:
            payload["card_holder"] = card_holder
        if metas:
            payload["metas"] = metas

        # 3DS (Native 3-D Secure)
        # Per API docs: if 3ds_params is present, webhook is required.
        if three_ds_params is not None:
            payload["3ds_params"] = three_ds_params
            if not webhook:
                raise CobaltPaymentError(
                    message="Configuración incompleta: webhook requerido para 3DS",
                    error_code="3ds_webhook_required",
                )
            payload["webhook"] = webhook
            if return_url:
                payload["return_url"] = return_url
            
        try:
            logger.info(f"Processing Cobalt sale: amount={amount} cents")
            response = requests.post(
                url, 
                json=payload, 
                headers=self._get_headers(),
                timeout=60  # Longer timeout for payment processing
            )
            
            data = response.json()
            
            if response.status_code == 200 and data.get('status') == 'ok':
                transaction = data.get('data', {})
                tx_status = transaction.get('status')
                metadatas = transaction.get('metadatas', {}) or {}
                
                logger.info(
                    f"Cobalt transaction {transaction.get('id')}: "
                    f"status={tx_status}, auth={transaction.get('authorization_number')}"
                )

                requires_3ds = tx_status == 'authenticating'
                
                return {
                    'success': tx_status == 'authorized',
                    'requires_3ds': requires_3ds,
                    'id': transaction.get('id'),
                    'identifier': transaction.get('identifier'),
                    'status': tx_status,
                    'authorization_number': transaction.get('authorization_number'),
                    'reference_number': transaction.get('reference_number'),
                    'response_code': transaction.get('response_code'),
                    'pan': transaction.get('pan'),  # Masked
                    'card_brand': metadatas.get('card_brand'),
                    'processed_at': transaction.get('processed_at'),
                    '3ds_authentication_form': metadatas.get('3ds_authentication_form'),
                    '3ds_version': metadatas.get('3ds_version'),
                    'raw_response': transaction
                }
            else:
                # Handle API error
                error_msg = data.get('message', 'Error procesando pago')
                error_code = data.get('error', 'unknown_error')
                
                logger.warning(f"Cobalt payment failed: {error_code} - {error_msg}")
                
                return {
                    'success': False,
                    'status': 'error',
                    'error_code': error_code,
                    'message': error_msg,
                    'details': data.get('data', {})
                }
                
        except requests.exceptions.Timeout:
            logger.error("Cobalt payment timeout")
            raise CobaltPaymentError(
                message="El procesador de pagos no respondió a tiempo. Por favor intenta de nuevo.",
                error_code="timeout"
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Cobalt payment request failed: {e}")
            raise CobaltPaymentError(
                message="Error de conexión con el procesador de pagos",
                error_code="connection_error"
            )
    
    def get_transaction(self, transaction_id):
        """
        Get transaction details by ID.
        
        Args:
            transaction_id: The transaction ID from Cobalt
            
        Returns:
            dict with transaction details
        """
        url = f"{self.host}/api/v2/transactions/{transaction_id}"
        
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            data = response.json()
            
            if response.status_code == 200 and data.get('status') == 'ok':
                return data.get('data', {})
            else:
                raise CobaltPaymentError(
                    message="No se pudo obtener información de la transacción",
                    error_code="not_found",
                    response_data=data
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get transaction {transaction_id}: {e}")
            raise CobaltPaymentError(
                message="Error consultando transacción",
                error_code="connection_error"
            )
    
    def refund(self, transaction_id, amount=None):
        """
        Process a refund/reversal for a transaction.
        
        Args:
            transaction_id: Original transaction ID to refund
            amount: Amount in cents to refund (optional, full refund if not specified)
            
        Returns:
            dict with refund transaction result
        """
        url = f"{self.host}/api/v2/transactions/refund/{transaction_id}"
        
        params = {}
        if amount is not None:
            params['amount'] = str(amount)
        
        try:
            response = requests.get(
                url, 
                params=params,
                headers=self._get_headers(), 
                timeout=60
            )
            data = response.json()
            
            if response.status_code == 200 and data.get('status') == 'ok':
                transaction = data.get('data', {})
                return {
                    'success': transaction.get('status') == 'authorized',
                    'id': transaction.get('id'),
                    'status': transaction.get('status'),
                    'authorization_number': transaction.get('authorization_number'),
                    'raw_response': transaction
                }
            else:
                return {
                    'success': False,
                    'status': 'error',
                    'message': data.get('message', 'Error procesando reembolso')
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Cobalt refund failed for {transaction_id}: {e}")
            raise CobaltPaymentError(
                message="Error procesando reembolso",
                error_code="connection_error"
            )


# Convenience function for quick access
def process_payment(amount, pan, exp_date, cvv2=None, card_holder=None):
    """
    Convenience function to process a payment.
    
    Args:
        amount: Amount in cents
        pan: Card number
        exp_date: Expiration MM/YY
        cvv2: CVV code
        card_holder: Name on card
        
    Returns:
        dict with payment result
    """
    gateway = CobaltPaymentGateway()
    return gateway.process_sale(
        amount=amount,
        pan=pan,
        exp_date=exp_date,
        cvv2=cvv2,
        card_holder=card_holder
    )

