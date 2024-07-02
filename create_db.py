from website import app, db  # Ensure the correct import

with app.app_context():
    db.create_all()
    db.session.commit()
