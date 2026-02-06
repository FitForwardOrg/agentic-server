from click.testing import CliRunner
from src.main import main
from src.config import settings
import unittest.mock as mock


def test_serve_reload_flag():
    runner = CliRunner()

    # Reset settings.debug before test
    settings.debug = False

    # We need to mock web.start() and factory() to avoid actually starting the server
    with (
        mock.patch("src.main.factory") as mock_factory,
        mock.patch("src.main.create_web_server") as mock_create_web_server,
    ):
        mock_web = mock.MagicMock()
        mock_create_web_server.return_value = mock_web

        # Run the command with --reload
        result = runner.invoke(main, ["serve", "--reload"])

        assert result.exit_code == 0
        assert settings.debug is True
        mock_web.start.assert_called_once()


def test_serve_no_reload_flag():
    runner = CliRunner()

    # Reset settings.debug before test
    settings.debug = False

    with mock.patch("src.main.factory"), mock.patch("src.main.create_web_server") as mock_create_web_server:
        mock_web = mock.MagicMock()
        mock_create_web_server.return_value = mock_web

        # Run the command without --reload
        result = runner.invoke(main, ["serve"])

        assert result.exit_code == 0
        assert settings.debug is False
