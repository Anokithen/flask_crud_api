from datetime import date
from flask import request, jsonify
from app import db
from app.models.student_model import Student


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

        existing = Student.query.filter_by(email=data["email"]).first()
        if existing:
            return jsonify({"error": "Email address already exists."}), 400

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

        return jsonify({"message": "Student created successfully.", "data": student.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def get_students():
    try:
        students = Student.query.all()
        return jsonify({"message": "Success", "count": len(students), "data": [s.to_dict() for s in students]}), 200
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def get_student(id):
    try:
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": f"Student with id {id} not found."}), 404
        return jsonify({"message": "Success", "data": student.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def update_student(id):
    try:
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": f"Student with id {id} not found."}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided in request body."}), 400

        if "age" in data and int(data["age"]) <= 0:
            return jsonify({"error": "age must be a positive integer."}), 400

        if "email" in data:
            existing = Student.query.filter_by(email=data["email"]).first()
            if existing and existing.id != id:
                return jsonify({"error": "Email address already exists."}), 400

        if "full_name"   in data: student.full_name   = data["full_name"]
        if "email"       in data: student.email       = data["email"]
        if "age"         in data: student.age         = int(data["age"])
        if "cgpa"        in data: student.cgpa        = data["cgpa"]
        if "is_active"   in data: student.is_active   = data["is_active"]
        if "joined_date" in data: student.joined_date = date.fromisoformat(data["joined_date"])

        db.session.commit()
        return jsonify({"message": "Student updated successfully.", "data": student.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def delete_student(id):
    try:
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": f"Student with id {id} not found."}), 404

        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"Student '{student.full_name}' deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
