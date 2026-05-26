# tests/conftest.py
import pytest
import sys
from unittest.mock import MagicMock

# Мокаем тяжелые зависимости до того, как pytest начнет импортировать app.py
sys.modules['kafka'] = MagicMock()

@pytest.fixture(autouse=True)
def mock_vault_and_db(monster_mock=None):
    """Автоматически подменяет вызовы к Vault и Postgres для тестов"""
    import src.database
    import src.vault_client
    
    # Подменяем функцию получения кредов из Vault
    src.vault_client.get_db_credentials = MagicMock(return_value={
        "user": "test_user", "password": "test_password", "dbname": "test_db"
    })
    
    # Подменяем само подключение к базе данных, возвращая фейковый курсор
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [] # Возвращаем пустую историю для GET /history
    mock_conn.cursor.return_value = mock_cursor
    
    src.database.get_db_connection = MagicMock(return_value=mock_conn)