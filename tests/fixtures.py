import pytest
from tests.certificate_testset_builder import CertificateTestSetBuilder


@pytest.fixture
def test_data_path(request):
    # provide test_data_path to all tests
    return request.config.rootpath / "tests/data"


@pytest.fixture(scope="session", autouse=True)
def generate_test_certificates():
    # Generate test certificates before all tests
    CertificateTestSetBuilder().generate_certificate_sets()
