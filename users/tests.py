from common.tests import CommonAPITestCase


class RegisterAPITestCase(CommonAPITestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_register(self):
        self.assertEqual(self.register_response.status_code, 201)
