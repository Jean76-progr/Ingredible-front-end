import unittest
from app import app, db, Compte, Ingredient, Recipe, RecipeIngredient, FavoriteRecipe

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_account(self):
        # Testez la création de compte avec des données valides
        response = self.app.post('/create_account', data=dict(username='test_user', password='test_password'))
        self.assertEqual(response.status_code, 302)  # Vérifiez si la redirection a eu lieu

        # Testez la création de compte avec des données manquantes
        response = self.app.post('/create_account', data=dict(username='test_user'))
        self.assertEqual(response.status_code, 400)

    def test_delete_account(self):
        # Créez un compte de test
        user = Compte(username='test_user', password='test_password')
        db.session.add(user)
        db.session.commit()

        # Connectez-vous avec le compte de test
        with self.app.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['username'] = user.username

        # Testez la suppression de compte
        response = self.app.post('/delete_account')
        self.assertEqual(response.status_code, 302)  # Vérifiez si la redirection a eu lieu

        # Vérifiez que le compte et les recettes associées ont été supprimés
        self.assertIsNone(Compte.query.get(user.id))
        self.assertEqual(len(Recipe.query.filter_by(user_id=user.id).all()), 0)

    def test_login(self):
        # Créez un compte de test
        user = Compte(username='test_user', password='test_password')
        db.session.add(user)
        db.session.commit()

        # Testez la connexion avec des données valides
        response = self.app.post('/login', data=dict(username='test_user', password='test_password'))
        self.assertEqual(response.status_code, 302)  # Vérifiez si la redirection a eu lieu

        # Testez la connexion avec des données incorrectes
        response = self.app.post('/login', data=dict(username='test_user', password='wrong_password'))
        self.assertEqual(response.status_code, 401)

    # Ajoutez d'autres tests pour les différentes fonctionnalités de votre application

if __name__ == '__main__':
    unittest.main()
