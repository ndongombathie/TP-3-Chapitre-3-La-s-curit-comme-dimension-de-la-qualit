from django.test import TestCase
from django.contrib.auth.models import User
from personnel.services import LoginThrottle

# TODO (TP3, partie sécurité) : une fois le throttle de connexion ajouté
# dans services.py, écrivez ici un test qui prouve qu'après N tentatives
# échouées, la Nème+1 est bloquée même avec le bon mot de passe. Comparez
# avec solution/personnel/tests.py une fois votre correctif terminé.

class LoginThrottleTest(TestCase):
    def test_login_throttle(self):
        throttle = LoginThrottle(max_attempts=3)
        username = "testuser"

        # Simulate failed login attempts
        for _ in range(3):
            throttle.enregistrer_tentative(username)

        # The next attempt should be blocked
        self.assertTrue(throttle.est_bloque(username))

        # Reset attempts and check that the user is no longer blocked
        throttle.reinitialiser_tentatives(username)
        self.assertFalse(throttle.est_bloque(username))
        
        
class LoginThrottleTestView(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="correctpassword")
        
    def test_login_view_throttle(self):
        from django.urls import reverse
        
        # Simulate failed login attempts
        for _ in range(6):
            response = self.client.post(reverse('personnel:connexion'), {
                'username': 'testuser',
                'password': 'wrongpassword'
            })
            self.assertEqual(response.status_code, 302)  # Redirect after failed login

        # The next attempt should be blocked
        response = self.client.post(reverse('personnel:connexion'), {
            'username': 'testuser',
            'password': 'correctpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        
        # Et surtout : l'utilisateur ne doit PAS être connecté
        self.assertFalse(response.wsgi_request.user.is_authenticated)

