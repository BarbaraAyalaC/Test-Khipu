import requests
from requests.auth import HTTPBasicAuth
import logging

# Configuración
KHIPU_API_URL = 'https://khipu.com/api/2.0/payments'
RECEIVER_ID = 'TU_RECEIVER_ID'  # Reemplaza con el número ID que da Khipu
SECRET = 'TU_SECRET'            # Reemplaza con tu clave secreta de la app

# Opcional
logging.basicConfig(level=logging.INFO)


def crear_pago_khipu(
    monto,
    descripcion,
    id_transaccion,
    email_cliente,
    return_url,
    cancel_url,
    notify_url
):
    """
    Crea un pago en Khipu usando el entorno de pruebas
    """
    payload = {
        'receiver_id': RECEIVER_ID,
        'subject': descripcion,
        'body': f'Cobro generado automáticamente para la transacción {id_transaccion}',
        'amount': monto,
        'currency': 'CLP',
        'transaction_id': id_transaccion,
        'payer_email': email_cliente,
        'return_url': return_url,
        'cancel_url': cancel_url,
        'notify_url': notify_url,
        'custom': 'datos personalizados si se necesitan',
    }

    try:
        response = requests.post(
            KHIPU_API_URL,
            data=payload,
            auth=HTTPBasicAuth(RECEIVER_ID, SECRET),
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al comunicarse con Khipu: {e}")
        return None

    data = response.json()
    logging.info(f"Pago creado exitosamente. URL de pago: {data.get('payment_url')}")
    return data.get('payment_url')


# Ejemplo de uso
if __name__ == '__main__':
    enlace_pago = crear_pago_khipu(
        monto=5000,
        descripcion='Prueba integración Khipu - DemoBank',
        id_transaccion='pedido-123',
        email_cliente='cliente@correo.cl',
        return_url='https://tusitio.cl/retorno',
        cancel_url='https://tusitio.cl/cancelado',
        notify_url='https://tusitio.cl/notificacion'
    )

    if enlace_pago:
        print("Enlace de pago generado:")
        print(enlace_pago)
    else:
        print("No se pudo generar el pago.")

