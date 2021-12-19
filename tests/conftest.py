import pytest
from weather import weather

@pytest.fixture
def app():
    app = weather()
    return app