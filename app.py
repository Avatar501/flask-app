from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Nécessaire pour flash()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['test']  # Database name
collection = db['employe']  # Collection name

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/add-employe', methods=['POST'])
def add_employe():
    # Get form data
    nom = request.form['nom']
    departement = request.form['departement']
    salaire = int(request.form['salaire'])
    date_embauche = request.form['dateEmbauche']

    # Get the current maximum _id in the collection
    max_id_doc = collection.find_one(sort=[('_id', -1)])  # Find the document with the largest _id
    new_id = max_id_doc['_id'] + 1 if max_id_doc else 1  # Increment _id, or start with 1 if collection is empty

    # Create the new document
    new_employe = {
        '_id': new_id,
        'nom': nom,
        'departement': departement,
        'salaire': salaire,
        'dateEmbauche': date_embauche
    }

    # Insert into MongoDB
    collection.insert_one(new_employe)
    flash('L\'employé a été ajouté avec succès!', 'success')

    return redirect(url_for('index'))  # Redirect to the home page or another page

if __name__ == '__main__':
    app.run(debug=True)

