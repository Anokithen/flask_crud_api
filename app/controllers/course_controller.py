from flask import request, jsonify
from app import db
from app.models.course_model import Course


def create_course():
    try:
        data = request.get_json(force=True)

        if not data.get("course_title"):
            return jsonify({"error": "course_title is required."}), 400
        if not data.get("course_fee"):
            return jsonify({"error": "course_fee is required."}), 400
        if not data.get("duration_months"):
            return jsonify({"error": "duration_months is required."}), 400
        if float(data["course_fee"]) <= 0:
            return jsonify({"error": "course_fee must be a positive number."}), 400
        if int(data["duration_months"]) <= 0:
            return jsonify({"error": "duration_months must be a positive integer."}), 400

        existing = Course.query.filter_by(course_title=data["course_title"]).first()
        if existing:
            return jsonify({"error": "Course title already exists."}), 400

        course = Course(
            course_title    = data["course_title"],
            course_fee      = float(data["course_fee"]),
            duration_months = int(data["duration_months"]),
            description     = data.get("description"),
            is_available    = data.get("is_available", True),
        )
        db.session.add(course)
        db.session.commit()
        return jsonify({"message": "Course created successfully.", "data": course.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def get_courses():
    try:
        courses = Course.query.all()
        return jsonify({"message": "Success", "count": len(courses), "data": [c.to_dict() for c in courses]}), 200
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def get_course(id):
    try:
        course = Course.query.get(id)
        if not course:
            return jsonify({"error": f"Course with id {id} not found."}), 404
        return jsonify({"message": "Success", "data": course.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def update_course(id):
    try:
        course = Course.query.get(id)
        if not course:
            return jsonify({"error": f"Course with id {id} not found."}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided in request body."}), 400

        if "course_fee" in data and float(data["course_fee"]) <= 0:
            return jsonify({"error": "course_fee must be a positive number."}), 400
        if "duration_months" in data and int(data["duration_months"]) <= 0:
            return jsonify({"error": "duration_months must be a positive integer."}), 400
        if "course_title" in data:
            existing = Course.query.filter_by(course_title=data["course_title"]).first()
            if existing and existing.id != id:
                return jsonify({"error": "Course title already exists."}), 400

        if "course_title"    in data: course.course_title    = data["course_title"]
        if "course_fee"      in data: course.course_fee      = float(data["course_fee"])
        if "duration_months" in data: course.duration_months = int(data["duration_months"])
        if "description"     in data: course.description     = data["description"]
        if "is_available"    in data: course.is_available    = data["is_available"]

        db.session.commit()
        return jsonify({"message": "Course updated successfully.", "data": course.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def delete_course(id):
    try:
        course = Course.query.get(id)
        if not course:
            return jsonify({"error": f"Course with id {id} not found."}), 404

        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": f"Course '{course.course_title}' deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
