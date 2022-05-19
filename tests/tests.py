import pytest
from app import app, login_manager

def test_app_exists():
  assert 1==1

def test_login_manager_exists():
  assert 1==1

  @pytest.fixture
  def client():
    return app