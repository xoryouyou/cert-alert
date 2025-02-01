from datetime import datetime, timezone, timedelta
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import logging
import coloredlogs


class CertificateTestSetBuilder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Started")
        self.key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        self.subject = self.issuer = x509.Name(
            [
                x509.NameAttribute(
                    NameOID.COMMON_NAME, "cert-alert-test-certificate"
                ),
            ]
        )

    def generate_certificate_sets(self):
        now = datetime.now(timezone.utc)
        # valid for 1 year
        not_valid_before = now
        self.generate_test_certificate(
            not_valid_before=not_valid_before,
            valid_for_days=timedelta(days=365),
            filename="tests/data/certificates/dynamic/valid_365days.pem",
        )
        # valid for 30 days
        self.generate_test_certificate(
            not_valid_before=not_valid_before,
            valid_for_days=timedelta(days=30),
            filename="tests/data/certificates/dynamic/valid_30days.pem",
        )

        # expired 30 days ago
        not_valid_before = now - timedelta(days=60)
        self.generate_test_certificate(
            not_valid_before=not_valid_before,
            valid_for_days=timedelta(days=30),
            filename="tests/data/certificates/dynamic/expired_30days_ago.pem",
        )
        # expired 1 year ago
        not_valid_before = now - timedelta(days=730)
        self.generate_test_certificate(
            not_valid_before=not_valid_before,
            valid_for_days=timedelta(days=365),
            filename="tests/data/certificates/dynamic/expired_365days_ago.pem",
        )

    def generate_test_certificate(
        self, filename: str, not_valid_before: datetime, valid_for_days: timedelta
    ):
        if filename is None:
            raise Exception("Filename not provided")

        cert = (
            x509.CertificateBuilder()
            .subject_name(self.subject)
            .issuer_name(self.issuer)
            .public_key(self.key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(not_valid_before)
            .not_valid_after(not_valid_before + valid_for_days)
            .sign(self.key, hashes.SHA256())
        )

        try:
            f = open(filename, "wb")
            self.logger.info(f"Writing certificate to {filename}")
            f.write(cert.public_bytes(serialization.Encoding.PEM))
            self.logger.info(f"✔️  Certificate written to {filename}")
        except Exception as e:
            self.logger.error(f"❌  Failed to write certificate to {filename} : {e}")
            raise Exception(f"Failed to write certificate to {filename} : {e}")


if __name__ == "__main__":
    coloredlogs.install()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    CertificateTestSetBuilder().generate_certificate_sets()
