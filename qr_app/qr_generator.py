import qrcode
from qrcode.constants import ERROR_CORRECT_Q
from pathlib import Path


def generate_qr(data: str, output_path: str) -> None:
    """
    Génère un QR Code et l'enregistre en PNG.
    """
    qr = qrcode.QRCode(
        version=None,  # Auto-optimal
        error_correction=ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
