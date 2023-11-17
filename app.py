from flask import Flask, request, jsonify, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ma_base_de_donnees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Compte(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    favorite_recipes = db.relationship('FavoriteRecipe', backref='user', lazy='dynamic')
    user_ingredients = db.relationship('Ingredient', backref='user', lazy='dynamic')
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe_ingredients = db.relationship('RecipeIngredient', backref='ingredient', lazy='dynamic')

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))  # Chemin de l'image de la recette
    user_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    ingredients = db.relationship('Ingredient', secondary='recipe_ingredient', backref='recipes', lazy='dynamic')
    is_favorite = db.relationship('FavoriteRecipe', backref='recipe', lazy='dynamic')

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))

class FavoriteRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

# Créez la base de données 
with app.app_context():
    db.create_all()

# Ajoutez cette route pour la création de compte
@app.route('/create_account', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            compte = Compte(username=username, password=password)
            db.session.add(compte)

            try:
                # Listes de noms des ingrédients
                ingredient_data = [
                {
                    'name': 'Escalope de dinde ou de poulet ou de veau',
                },
                {
                    'name': 'Tranches de jambon blanc',
                },
                {
                    'name': 'Chapelure'
                },
                {
                    'name': 'Tomates',
                },
                {
                    'name': 'Oeufs',
                },
                {
                    'name': 'Olives noires',
                },
                {
                    'name': 'Thon',
                },
                {
                    'name': 'Anchois',
                },
                {
                    'name': 'Haricots verts',
                },
                {
                    'name': 'Poivron rouge',
                },
                {
                    'name': 'Roquette',
                },
                {
                    'name': 'Radis roses',
                },
                {
                    'name': 'Penne',
                },
                {
                    'name': 'Gorgonzola',
                },
                {
                    'name': 'Riz rond',
                },
                {
                    'name': 'Lait',
                },
                {
                    'name': 'Crème',
                },
                {
                    'name': 'Sucre',
                },
                {
                    'name': 'Vanille',
                },
                {
                    'name': 'Faisselle',
                },
                {
                    'name': 'Farine',
                },
                {
                    'name': 'Raisins',
                },
                {
                    'name': 'Beurre',
                },
                {
                    'name': 'Gousse de vanille',
                },
                {
                    'name': 'Pâtes',
                },
                {
                    'name': 'Oignons',
                },
                {
                    'name': 'Lardons',
                },
                {
                    'name': 'Crème fraîche',
                },
                {
                    'name': 'Œufs',
                },
                {
                    'name': 'Sel',
                },
                {
                    'name': 'Poivre',
                },
                {
                    'name': 'Pommes de terre',
                },
                {
                    'name': 'Lardons',
                },
                {
                    'name': 'Gruyère',
                },
                {
                    'name': 'Pâte',
                },
                {
                    'name': 'Chèvre',
                },
                {
                    'name': 'Lardons',
                },
                {
                    'name': 'Thym',
                },
                {
                    'name': 'Framboises',
                },
                {
                    'name': 'Mascarpone',
                },
                {
                    'name': 'Sucre',
                },
                {
                    'name': 'Crème fleurette',
                },
                {
                    'name': 'Gélatine',
                },
                {
                    'name': 'Beurre',
                },
                {
                    'name': "Poudre d'amandes",
                },
                {
                    'name': 'Vanille',
                },
                {
                    'name': 'Œuf',
                },
                {
                    'name': 'Biscuits cuillers',
                },
                {
                    'name': 'Café',
                },
                {
                    'name': "Jaunes d'œufs",
                },
                {
                    'name': 'Sucre',
                },
                {
                    'name': 'Amaretto',
                },
                {
                    'name': "Blancs d'œufs",
                },
                {
                    'name': 'Mascarpone',
                },
                {
                    'name': 'Cacao en poudre',
                }
            ]

                
                # Ajoutez chaque ingrédients à la base de données
                for ingredient_info in ingredient_data:
                    ingredient = Ingredient(
                        name=ingredient_info['name'],
                        user_id=compte.id,
                    )
                    db.session.add(ingredient)
                    
                db.session.commit()

                # Recherche les ingrédients spécifiques dans la base de données

                ingredient_dinde = Ingredient.query.filter_by(name='Escalope de dinde ou de poulet ou de veau').first()
                ingredient_jambon = Ingredient.query.filter_by(name='Tranches de jambon blanc').first()
                ingredient_chapelure = Ingredient.query.filter_by(name='Chapelure').first()

                ingredient_tomates = Ingredient.query.filter_by(name='Tomates').first()
                ingredient_oeufs = Ingredient.query.filter_by(name='Oeufs').first()
                ingredient_olives_noires = Ingredient.query.filter_by(name='Olives noires').first()
                ingredient_thon = Ingredient.query.filter_by(name='Thon').first()
                ingredient_anchois = Ingredient.query.filter_by(name='Anchois').first()
                ingredient_haricots_verts = Ingredient.query.filter_by(name='Haricots verts').first()
                ingredient_poivron_rouge = Ingredient.query.filter_by(name='Poivron rouge').first()
                ingredient_roquette = Ingredient.query.filter_by(name='Roquette').first()
                ingredient_radis_roses = Ingredient.query.filter_by(name='Radis roses').first()

                ingredient_penne = Ingredient.query.filter_by(name='Penne').first()
                ingredient_gorgonzola = Ingredient.query.filter_by(name='Gorgonzola').first()

                ingredient_riz_rond = Ingredient.query.filter_by(name='Riz rond').first()
                ingredient_lait = Ingredient.query.filter_by(name='Lait').first()
                ingredient_creme = Ingredient.query.filter_by(name='Crème').first()
                ingredient_sucre = Ingredient.query.filter_by(name='Sucre').first()
                ingredient_vanille = Ingredient.query.filter_by(name='Vanille').first()

                ingredient_faisselle = Ingredient.query.filter_by(name='Faisselle').first()
                ingredient_farine = Ingredient.query.filter_by(name='Farine').first()
                ingredient_raisins = Ingredient.query.filter_by(name='Raisins').first()
                ingredient_beurre = Ingredient.query.filter_by(name='Beurre').first()
                ingredient_gousse_vanille = Ingredient.query.filter_by(name='Gousse de vanille').first()

                ingredient_pates = Ingredient.query.filter_by(name='Pâtes').first()
                ingredient_oignons = Ingredient.query.filter_by(name='Oignons').first()
                ingredient_lardons = Ingredient.query.filter_by(name='Lardons').first()
                ingredient_creme_fraiche = Ingredient.query.filter_by(name='Crème fraîche').first()
                ingredient_oeufs = Ingredient.query.filter_by(name='Œufs').first()
                ingredient_sel = Ingredient.query.filter_by(name='Sel').first()
                ingredient_poivre = Ingredient.query.filter_by(name='Poivre').first()

                ingredient_pommes_de_terre = Ingredient.query.filter_by(name='Pommes de terre').first()
                ingredient_lardons_pommes_de_terre = Ingredient.query.filter_by(name='Lardons').first()
                ingredient_gruyere = Ingredient.query.filter_by(name='Gruyère').first()

                ingredient_pate = Ingredient.query.filter_by(name='Pâte').first()
                ingredient_chevre = Ingredient.query.filter_by(name='Chèvre').first()
                ingredient_lardons_quiche = Ingredient.query.filter_by(name='Lardons').first()
                ingredient_thym = Ingredient.query.filter_by(name='Thym').first()

                ingredient_framboises = Ingredient.query.filter_by(name='Framboises').first()
                ingredient_mascarpone = Ingredient.query.filter_by(name='Mascarpone').first()
                ingredient_sucre_tarte = Ingredient.query.filter_by(name='Sucre').first()
                ingredient_creme_fleurette = Ingredient.query.filter_by(name='Crème fleurette').first()
                ingredient_gelatine = Ingredient.query.filter_by(name='Gélatine').first()
                ingredient_beurre_tarte = Ingredient.query.filter_by(name='Beurre').first()
                ingredient_poudre_amandes = Ingredient.query.filter_by(name='Poudre d\'amandes').first()
                ingredient_vanille_tarte = Ingredient.query.filter_by(name='Vanille').first()
                ingredient_oeuf_tarte = Ingredient.query.filter_by(name='Œuf').first()

                ingredient_biscuits_cuillers = Ingredient.query.filter_by(name='Biscuits cuillers').first()
                ingredient_cafe = Ingredient.query.filter_by(name='Café').first()
                ingredient_jaunes_oeufs = Ingredient.query.filter_by(name='Jaunes d\'œufs').first()
                ingredient_sucre_tiramisu = Ingredient.query.filter_by(name='Sucre').first()
                ingredient_amaretto = Ingredient.query.filter_by(name='Amaretto').first()
                ingredient_blancs_oeufs = Ingredient.query.filter_by(name='Blancs d\'œufs').first()
                ingredient_mascarpone_tiramisu = Ingredient.query.filter_by(name='Mascarpone').first()
                ingredient_cacao_poudre = Ingredient.query.filter_by(name='Cacao en poudre').first()

                # Créez les recettes avec les ingrédients associés
                recipe_salade_nicoise = Recipe(
                    name='Salade Niçoise',
                    instructions='Instructions pour la Salade Niçoise',
                    user_id=compte.id
                )

                recipe_penne_gorgonzola_roquette = Recipe(
                    name='Penne Gorgonzola-Roquette',
                    instructions='Instructions pour les Penne Gorgonzola-Roquette',
                    user_id=compte.id
                )

                recipe_riz_au_lait = Recipe(
                    name='Riz au lait',
                    instructions='Instructions pour le Riz au lait',
                    user_id=compte.id
                )

                recipe_tarte_au_fromage_blanc = Recipe(
                    name='Tarte au fromage blanc',
                    instructions='Instructions pour la Tarte au fromage blanc',
                    user_id=compte.id
                )

                recipe_pates_carbonaras_a_la_francaise = Recipe(
                    name='Pates Carbonaras à la française',
                    instructions='Instructions pour les Pates Carbonaras à la française',
                    user_id=compte.id
                )

                recipe_oeuf_cocotte_en_pomme_de_terre = Recipe(
                    name='Oeuf cocotte en pomme de terre',
                    instructions='Instructions pour l\'Oeuf cocotte en pomme de terre',
                    user_id=compte.id
                )

                recipe_quiche_chevre_lardons = Recipe(
                    name='Quiche chèvre lardons',
                    instructions='Instructions pour la Quiche chèvre lardons',
                    user_id=compte.id
                )

                recipe_tarte_mousse_de_framboise = Recipe(
                    name='Tarte mousse de framboise',
                    instructions='Instructions pour la Tarte mousse de framboise',
                    user_id=compte.id
                )

                recipe_tiramisu = Recipe(
                    name='Tiramisù',
                    instructions='Instructions pour le Tiramisù',
                    user_id=compte.id
                )

                recipe_cordons_bleus = Recipe(
                    name='Cordons bleus',
                    instructions='Détaillez 175 g de comté ou d’emmental en fines lamelles à l’aide d’un économe. \n Coupez 2 fines tranches de jambon blanc en deux. Battez 1 œuf avec 2 c. à soupe de lait, du sel, du poivre et un peu de noix muscade râpée. \n Coupez 4 escalopes de dinde en deux, dans le sens de l’épaisseur, et aplatissez-les à l’aide d’un rouleau à pâtisserie. \n(Vous pouvez aussi demander à votre boucher d’effectuer cette opération.) Posez sur chaque escalope une demi-tranche de jambon, puis couvrez la moitié inférieure de lamelles de fromage, sans aller jusqu’au bord, afin d’éviter que le fromage ne s’échappe à la cuisson. \n Repliez vos escalopes en deux et roulez-les dans 2 c. à soupe de farine, en appuyant bien sur les bords, puis passez-les dans l’œuf battu et dans 100 g de chapelure. Faites chauffer 3 c. à soupe d’huile de friture dans une sauteuse et faites dorer les cordons bleus 2 mn de chaque côté. Baissez le feu et poursuivez la cuisson une dizaine de minutes, en les retournant très régulièrement pour leur éviter de brûler. \n (Vous pouvez également saisir les cordons bleus 2 mn à feu vif sur chaque face puis terminer leur cuisson au four, 20 mn à 180 °C, th. 6). \n Dégustez aussitôt.',
                    user_id=compte.id,
                )

                # Associez les ingrédients aux recettes
                recipe_cordons_bleus.ingredients.extend([ingredient_dinde, ingredient_jambon, ingredient_chapelure])
                recipe_salade_nicoise.ingredients.extend([ingredient_tomates, ingredient_oeufs, ingredient_olives_noires, ingredient_thon, ingredient_anchois, ingredient_haricots_verts, ingredient_poivron_rouge, ingredient_roquette, ingredient_radis_roses])
                recipe_penne_gorgonzola_roquette.ingredients.extend([ingredient_penne, ingredient_gorgonzola])
                recipe_riz_au_lait.ingredients.extend([ingredient_riz_rond, ingredient_lait, ingredient_creme, ingredient_sucre, ingredient_vanille])
                recipe_tarte_au_fromage_blanc.ingredients.extend([ingredient_faisselle, ingredient_farine, ingredient_raisins, ingredient_beurre, ingredient_gousse_vanille])
                recipe_pates_carbonaras_a_la_francaise.ingredients.extend([ingredient_pates, ingredient_oignons, ingredient_lardons, ingredient_creme_fraiche, ingredient_oeufs, ingredient_sel, ingredient_poivre])
                recipe_oeuf_cocotte_en_pomme_de_terre.ingredients.extend([ingredient_pommes_de_terre, ingredient_creme, ingredient_oeufs, ingredient_lardons_pommes_de_terre, ingredient_gruyere])
                recipe_quiche_chevre_lardons.ingredients.extend([ingredient_pate, ingredient_chevre, ingredient_lardons_quiche, ingredient_oeufs, ingredient_creme, ingredient_sel, ingredient_poivre, ingredient_thym])
                recipe_tarte_mousse_de_framboise.ingredients.extend([ingredient_framboises, ingredient_mascarpone, ingredient_sucre_tarte, ingredient_creme_fleurette, ingredient_gelatine, ingredient_beurre_tarte, ingredient_poudre_amandes, ingredient_vanille_tarte, ingredient_oeuf_tarte])
                recipe_tiramisu.ingredients.extend([ingredient_biscuits_cuillers, ingredient_cafe, ingredient_jaunes_oeufs, ingredient_sucre_tiramisu, ingredient_amaretto, ingredient_blancs_oeufs, ingredient_mascarpone_tiramisu, ingredient_cacao_poudre])

                # Ajoutez les recettes à la base de données
                db.session.add_all([
                    recipe_cordons_bleus,
                    recipe_salade_nicoise,
                    recipe_penne_gorgonzola_roquette,
                    recipe_riz_au_lait,
                    recipe_tarte_au_fromage_blanc,
                    recipe_pates_carbonaras_a_la_francaise,
                    recipe_oeuf_cocotte_en_pomme_de_terre,
                    recipe_quiche_chevre_lardons,
                    recipe_tarte_mousse_de_framboise,
                    recipe_tiramisu
                ])

                db.session.commit()
                return redirect(url_for('login'))

            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': 'Nom d\'utilisateur déjà utilisé'}), 400

        else:
            return jsonify({'message': 'Données manquantes'}), 400
    return render_template('creation.html')
    

# Ajoutez cette route pour supprimer un compte
from flask import redirect

@app.route('/delete_account', methods=['POST', 'GET'])
def delete_account():
    if request.method == 'POST':
        user_id = session.get('user_id')

        if user_id:
            compte = Compte.query.filter_by(id=user_id).first()

            if compte:
                # Supprimez toutes les recettes associées à ce compte
                Recipe.query.filter_by(user_id=user_id).delete()
                # Supprimez l'utilisateur
                db.session.delete(compte)
                db.session.commit()
                session.clear()  # Déconnectez l'utilisateur après la suppression du compte

                # Redirigez l'utilisateur vers la page de création de compte
                return redirect(url_for('create_account'))

        return jsonify({'message': 'La suppression du compte a échoué'}), 400

    return render_template('supression.html')  # Remplacez 'suppression.html' par le modèle approprié

# Ajoutez cette route pour se connecter
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        if 'username' in data and 'password' in data:
            username = data['username']
            password = data['password']

            compte = Compte.query.filter_by(username=username, password=password).first()

            if compte:
                session['user_id'] = compte.id
                session['username'] = username
                session.modified = True
                return redirect(url_for('menu'))
            else:
                return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}), 401
        else:
            return jsonify({'message': 'Données manquantes'}), 400

    return render_template('login.html')

@app.route('/menu')
def menu():
    user_id = session.get('user_id')

    if user_id:
        # Récupérez les recettes favorites de l'utilisateur actuellement connecté
        favorite_recipes = FavoriteRecipe.query.filter_by(user_id=user_id).all()
        favorite_recipe_ids = [favorite.recipe_id for favorite in favorite_recipes]

        # Récupérez toutes les recettes de l'utilisateur actuellement connecté
        recipes = Recipe.query.filter_by(user_id=user_id).all()

        # Triez les recettes pour placer les favorites en premier
        sorted_recipes = sorted(recipes, key=lambda recipe: recipe.id in favorite_recipe_ids, reverse=True)

        return render_template('menu.html', username=session['username'],user_id=user_id, recipes=sorted_recipes)
    else:
        return redirect(url_for('login'))



# Ajoutez ces routes pour créer et supprimer des ingrédients
@app.route('/create_ingredient', methods=['POST'])
def create_ingredient():
    name = request.form.get('name')
    user_id = session.get('user_id')

    if name and user_id:
        ingredient = Ingredient(name=name, user_id=user_id)
        db.session.add(ingredient)
        db.session.commit()
        return redirect(url_for('menu'))

    return jsonify({'message': 'Données manquantes'}), 400

# Ajoutez cette route pour gérer la déconnexion
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# Ajoutez cette route pour créer une recette
@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        user_id = session.get('user_id')

        if user_id:
            recipe_name = request.form.get('recipe_name')
            instructions = request.form.get('instructions')

            recipe = Recipe(name=recipe_name, instructions=instructions, user_id=user_id)
            db.session.add(recipe)
            db.session.commit()

            # Récupérez les ingrédients sélectionnés (par exemple, sous forme d'une liste d'IDs)
            selected_ingredient_ids = request.form.getlist('ingredient_ids')

            # Associez ces ingrédients à la recette en mettant à jour le champ recipe_id
            for ingredient_id in selected_ingredient_ids:
                ingredient = Ingredient.query.get(ingredient_id)
                if ingredient:
                    ingredient.recipe_id = recipe.id
                    db.session.add(ingredient)

            db.session.commit()

            return redirect(url_for('list_recipes'))
        else:
            return jsonify({'message': 'Non connecté'}), 401

    return render_template('create_recipe.html')


# Ajoutez cette route pour afficher la liste des recettes
@app.route('/list_recipes')
def list_recipes():
    user_id = session.get('user_id')

    if user_id:
        recipes = Recipe.query.filter_by(user_id=user_id).all()
        return render_template('list_recipes.html', recipes=recipes)
    else:
        return redirect(url_for('login'))
    
@app.route('/view_recipe/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    user_id = session.get('user_id')

    if user_id:
        recipe = Recipe.query.filter_by(id=recipe_id, user_id=user_id).first()

        if recipe:
            # Récupérez les ingrédients associés à cette recette
            ingredients = recipe.ingredients.all()

            return render_template('view_recipe.html', recipe=recipe, ingredients=ingredients)
        else:
            return jsonify({'message': 'Recette non trouvée'}), 404
    else:
        return redirect(url_for('login'))



@app.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    user_id = session.get('user_id')
    recipe_id = request.form.get('recipe_id')

    if user_id and recipe_id:
        favorite = FavoriteRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

        if favorite:
            db.session.delete(favorite)
        else:
            favorite = FavoriteRecipe(user_id=user_id, recipe_id=recipe_id)
            db.session.add(favorite)
            
        db.session.commit()

        response = jsonify({'success': True})
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response, 200
    else:
        return jsonify({'success': False, 'message': 'Non connecté ou données manquantes'}), 401

@app.route('/favorite_recipes', methods=['GET'])
def favorite_recipes():
    user_id = session.get('user_id')
    
    if user_id:
      
        favorite_recipes = FavoriteRecipe.query.filter_by(user_id=user_id).all()
        favorite_recipe_ids = [favorite.recipe_id for favorite in favorite_recipes]
        
        recipes = Recipe.query.filter(Recipe.id.in_(favorite_recipe_ids)).all()
        
        return render_template('favorite_recipes.html', recipes=recipes)
    else:
        return redirect(url_for('login'))
        
@app.route('/list_ingredients', methods=['GET'])
def list_ingredients():
    user_id = session.get('user_id')
    
    if user_id:
        
        user_ingredients = Ingredient.query.all()
        return render_template('list_ingredients.html', ingredients=user_ingredients)
    else:
        return redirect(url_for('login'))

  
@app.route('/')
def return_home():
    return redirect(url_for('create_account'))

@app.route('/filter_recipes', methods=['POST'])
def filter_recipes():
    selected_ingredients = request.form.getlist('ingredient_ids')
    
    # Filtrer les recettes en fonction des ingrédients sélectionnés
    filtered_recipes = Recipe.query.filter(Recipe.ingredients.any(Ingredient.id.in_(selected_ingredients))).all()
 
    return render_template('menu.html', recipes=filtered_recipes, ingredients=Ingredient)

if __name__ == '__main__':
    app.run(debug=True)
