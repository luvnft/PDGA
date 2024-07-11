# history/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .forms import PlayerNumberForm
import requests_mock

class IndexViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history/index.html')

    @requests_mock.Mocker()
    def test_valid_player_number_form(self, mock_request):
        form_data = {'player_number': '236811'}
        form = PlayerNumberForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Mock the requests.get call to return a predefined response for testing
        mock_html = """
        <html>
        <body>
            <h1>John Doe #236811</h1>
            <table id="player-results-history">
                <tbody>
                    <tr>
                        <td class="date">10-Jul-2024</td>
                        <td class="player-rating">850</td>
                        <td class="round">1</td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
        """
        mock_request.get('https://www.pdga.com/player/236811/history', text=mock_html)

        response = self.client.post(reverse('index'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '236811')
        self.assertContains(response, 'John Doe #236811')
        self.assertContains(response, '850')
