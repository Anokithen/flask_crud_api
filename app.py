from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root123@localhost/flask_crud_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = "students"

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name   = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(120), nullable=False, unique=True)
    age         = db.Column(db.Integer, nullable=False)
    cgpa        = db.Column(db.Float, default=0.0)
    is_active   = db.Column(db.Boolean, default=True)
    joined_date = db.Column(db.Date, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "full_name":   self.full_name,
            "email":       self.email,
            "age":         self.age,
            "cgpa":        self.cgpa,
            "is_active":   self.is_active,
            "joined_date": str(self.joined_date),
            "created_at":  str(self.created_at),
        }





if __name__ == "__main__":
    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            print("SUCCESS: Database connected!")
            db.create_all()
            print("SUCCESS: Tables created!")
    except Exception as e:
        print(f"ERROR: {e}")
    app.run(debug=True)

