import os
from config import db
from models import Development
from app import connex_app

# Data to initialize database with
MILESTONES = [
    {'name': 'Analisis Kebutuhan', 'city': 'Medan', 'description': 'Menyelesaikan analisis kebutuhan pengguna'},
    {'name': 'Desain Antarmuka', 'city': 'Medan', 'description': 'Menyelesaikan desain antarmuka pengguna'},
    {'name': 'Pengembangan Fitur Inti', 'city': 'Medan', 'description': 'Menyelesaikan pengembangan fitur inti aplikasi'},
    {'name': 'Uji Beta Aplikasi', 'city': 'Medan', 'description': 'Melakukan uji beta untuk mendapatkan umpan balik pengguna'},
    {'name': 'Peluncuran Resmi', 'city': 'Medan', 'description': 'Meluncurkan aplikasi secara resmi di platform terkait'}
]
    # {'fname': 'Rizky', 'lname': 'Akbar'},
    # {'fname': 'Rinintha', 'lname': 'Anggie'},
    # {'fname': 'Safran','lname': 'Wijaya'}

# Delete database file if it exists currently
if os.path.exists('milestones.db'):
    os.remove('milestones.db')

# Create the database
with connex_app.app.app_context():
    db.create_all()

    # Iterate over the MILESTONES structure and populate the database
    for development in MILESTONES:
        p = Development(name=development['name'], city=development['city'], description=development['description'])
        db.session.add(p)

    db.session.commit()
