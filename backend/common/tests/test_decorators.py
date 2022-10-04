from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from common.decorators import disable_for_loaddata


@patch("inspect.getmodulename")
class TestDisableForLoadData(SimpleTestCase):
    def setUp(self):
        self.mock_handler_inner = MagicMock()

        @disable_for_loaddata
        def mock_handler():
            self.mock_handler_inner()

        self.mock_handler = mock_handler

    def test_disable_for_load_data_disables(self, mock_getmodulename):
        mock_getmodulename.return_value = "loaddata"
        self.mock_handler()
        self.mock_handler_inner.assert_not_called()

    def test_disable_for_load_data_does_not_disable(self, mock_getmodulename):
        mock_getmodulename.return_value = ""
        self.mock_handler()
        self.mock_handler_inner.assert_called_once()
