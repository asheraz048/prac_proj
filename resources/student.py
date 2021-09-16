from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, jwt_optional, fresh_jwt_required
from models.student import StudentModel


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('grade',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('fee',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required
    def get(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            return student.json()
        return {'message': 'Student not found'}, 404


    @fresh_jwt_required
    def post(self, name):
        if StudentModel.find_by_name(name):
            return {'message': "A student with name '{}' already exists.".format(name)}, 400

        data = Student.parser.parse_args()

        student = StudentModel(name, **data)

        try:
            student.save_to_db()
        except:
            return {"message": "An error occurred inserting the student."}, 500

        return student.json(), 201

    @jwt_required
    def delete(self, name):

        claims= get_jwt_claims()
        if not claims ['is_admin']:
            return {"Message":"Admin privelage required"} , 401

        student = StudentModel.find_by_name(name)
        if student:
            student.delete_from_db()
            return {'message': 'Student deleted.'}
        return {'message': 'Student not found.'}, 404

    def put(self, name):
        data = Student.parser.parse_args()

        student = StudentModel.find_by_name(name)

        if student:
            student.grade = data['grade']
            student.fee = data['fee']
        else:
            student = StudentModel(name, **data)

        student.save_to_db()

        return student.json()


class StudentList(Resource):
    @jwt_optional
    def get(self):
        user_id=get_jwt_identity()
        students = [student.json() for student in StudentModel.query.all()]
        if user_id:
            return  {'students':students}

        return {
            'students': [student['name'] for student in students],
             'Message':'If you need more information , please login .'
            }

