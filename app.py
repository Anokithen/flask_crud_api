from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime, date

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



class Course(db.Model):
    __tablename__ = "courses"

    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_title     = db.Column(db.String(100), nullable=False, unique=True)
    course_fee       = db.Column(db.Float, nullable=False)
    duration_months  = db.Column(db.Integer, nullable=False)
    description      = db.Column(db.Text, nullable=True)
    is_available     = db.Column(db.Boolean, default=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":              self.id,
            "course_title":    self.course_title,
            "course_fee":      self.course_fee,
            "duration_months": self.duration_months,
            "description":     self.description,
            "is_available":    self.is_available,
            "created_at":      str(self.created_at),
        }


@app.route("/api/students", methods=["POST"])
def create_student():
    try:
        data = request.get_json()

       
        if not data.get("full_name"):
            return jsonify({"error": "full_name is required."}), 400
        if not data.get("email"):
            return jsonify({"error": "email is required."}), 400
        if not data.get("age"):
            return jsonify({"error": "age is required."}), 400
        if not data.get("joined_date"):
            return jsonify({"error": "joined_date is required."}), 400

        if int(data["age"]) <= 0:
            return jsonify({"error": "age must be a positive integer."}), 400

        

       
        student = Student(
            full_name   = data["full_name"],
            email       = data["email"],
            age         = int(data["age"]),
            cgpa        = data.get("cgpa", 0.0),
            is_active   = data.get("is_active", True),
            joined_date = date.fromisoformat(data["joined_date"]),
        )
        db.session.add(student)
        db.session.commit()

        return jsonify({
            "message": "Student created successfully.",
            "data": student.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


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

