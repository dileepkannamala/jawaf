
def test_send_text_mail(test_project, waf):
    email_data = {
        'subject': 'test',
        'message': 'Test!',
        'from_address': 'jawaf@example.com',
        'to': 'test@example.com'
    }
    request, response = waf.server.test_client.post(
        '/test_app/email/', json=email_data)
    assert response.status == 200


def test_send_html_mail(test_project, waf):
    email_data = {
        'subject': 'test',
        'message': 'HTML Test!',
        'from_address': 'jawaf@example.com',
        'to': 'html@example.com',
        'bcc': ['a@example.com', 'b@example.com'],
        'html_message': '<body><strong>WOW</strong></body>',
    }
    request, response = waf.server.test_client.post(
        '/test_app/email/', json=email_data)
    assert response.status == 200
