import json
import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request, Response

from odoo.odoo.osv.expression import is_false


# create a helper function that will return a valid response
def valid_response(data, status, pagination_info):
    reponse_body = {
        "message": "Successful",
        "data": data,
    }
    if pagination_info:
        reponse_body["pagination_info"] = pagination_info
    return Response(json.dumps(reponse_body), content_type='application/json', status=status)


# create a helper function that will return a valid response
def invalid_response(error, status):
    reponse_body = {
        "error": error,
    }
    return Response(json.dumps(reponse_body), content_type='application/json', status=status)


# create a new controller that will contain the endpoint
class SchoolStudentApi(http.Controller):
    ############ uses ORM methods to create, read, update, and delete records in the database ########################

    # 1- method ( Creation ) json response (http)
    # create a new endpoint that will return a simple string "Hello world, Eslam Mohamed Junior Odoo Developer"
    # decorate the method with the route decorator to define the endpoint
    @http.route("/v1/school.student", methods=["POST"], type='http', auth='none', csrf=False)
    # define the method that will be executed when the endpoint
    def post_school_student(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                "message": "Name is required!",
            }, status=400)

        try:
            res = request.env['school.student'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": "student has been created Success ",
                    "id": res.id,
                    "name": res.name,
                }, status=201)
        except Exception as Error:
            return request.make_json_response({
                "message": Error,
            }, status=400)  # Bad Request

        # # 1- method  ( Creation ) json response (json)
        # @http.route("/v1/school.student/json", methods=["POST"], type='json', auth='none', csrf=False)
        # # define the method that will be executed when the endpoint
        # def post_school_student_json(self):
        #     args = request.httprequest.data.decode()  # get user data the request body from the request
        #     vals = json.loads(args)  # convert the request body from json to a dictionary
        #     # check if the name key exists in the dictionary
        #     if not vals.get('name'):
        #         return {
        #             "message": "Name is required!",
        #         }
        #     # try to create a new student record in the database using the create method of the ORM
        #     try:
        #         res = request.env['school.student'].sudo().create(vals)
        #         # check if the student record has been created successfully
        #         if res:
        #             return {
        #                 "message": "student has been created successfully ",
        #                 "id": res.id,
        #                 "name": res.name,
        #             }
        #     except Exception as Error:
        #         return {
        #             "message": Error
        #         }  # Bad Request

    # 1- method  ( Creation ) json response (json) ( Using SQL Query ) ( Faster ) ( Better Performance )
    @http.route("/v1/school.student/json", methods=["POST"], type='json', auth='none', csrf=False)
    # define the method that will be executed when the endpoint
    def post_school_student_json(self):
        args = request.httprequest.data.decode()  # get user data the request body from the request
        vals = json.loads(args)  # convert the request body from json to a dictionary
        # check if the name key exists in the dictionary
        if not vals.get('name'):
            return {
                "message": "Name is required!",
            }
        # try to create a new student record in the database using the create method of the ORM
        try:
            # res = request.env['school.student'].sudo().create(vals)

            cr = request.env.cr  # get the cursor object from the request
            columns = ', '.join(
                vals.keys())  # 'name, age, student_id .......' # get the columns names from the dictionary keys
            values = ', '.join(
                ['%s'] * len(vals))  # '%s, %s, %s .......' # get the values placeholders from the dictionary values
            query = f"""INSERT INTO school_student ({columns})
            VALUES ({values}) RETURNING id, name, age, student_id"""  # create the insert query
            cr.execute(query, tuple(
                vals.values()))  # execute the insert query with the values placeholders and the values tuple
            res = cr.fetchone()  # get the inserted record from the database using the fetchone method of the cursor object
            print(res)  # print the inserted record to the console

            # check if the student record has been created successfully
            if res:
                return {
                    "message": "student has been created successfully ",
                    "id": res[0],
                    "name": res[1],
                    "age": res[2],
                    "student_id": res[3],
                }
        except Exception as Error:
            return {
                "message": Error
            }  # Bad Request

    #######################################################################################################

    # 2- method ( Update )
    # create a new endpoint that will update the student record
    # decorate the method with the route decorator to define the endpoint and pass the student id as a parameter to the endpoint
    @http.route("/v1/school.student/<int:school_student_id>", methods=["PUT"], type='json', auth='none', csrf=False)
    # define the method that will be executed when the endpoint
    def update_school_student(self, school_student_id):
        try:
            school_student_id = request.env['school.student'].sudo().search([('id', '=', school_student_id)])
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            if not school_student_id:
                return {
                    "message": " ID does not exist!",
                }
            school_student_id.write(vals)
            # return a simple string "student has been updated Success"
            return {
                "message": "student has been updated Success ",
                "id": school_student_id.id,
                "name": school_student_id.name,
            }
        except Exception as Error:
            return {
                "message": Error
            }  # Bad Request

    #######################################################################################################

    # 3- method (  Read = Get  )
    # create a new endpoint that will return the single student record
    # decorate the method with the route decorator to define the endpoint and pass the student id as a parameter to the endpoint
    @http.route("/v1/school.student/<int:school_student_id>", methods=["GET"], type='http', auth='none', csrf=False)
    # define the method that will be executed when the endpoint
    def get_school_student(self, school_student_id):
        try:
            # search for the student record by id in the database using the search method of the ORM
            school_student_id = request.env['school.student'].sudo().search([('id', '=', school_student_id)])
            if not school_student_id:
                return invalid_response("ID does not exist!", status=400)
            # return a simple json object that contains the single student
            return valid_response({
                "id": school_student_id.id,
                "name": school_student_id.name,
                "gender": school_student_id.gender,
                "age": school_student_id.age,
            }, status=200)
        except Exception as Error:
            return Response(json.dumps({
                "error": str(Error)
            }), content_type='application/json', status=400)

    #######################################################################################################

    # 4- method ( Delete )
    # create a new endpoint that will delete the student record
    # decorate the method with the route decorator to define the endpoint and pass the student id as a parameter to the endpoint
    @http.route("/v1/school.student/<int:school_student_id>", methods=["DELETE"], type='http', auth='none', csrf=False)
    # define the method that will be executed when the endpoint
    def delete_school_student(self, school_student_id):
        try:
            # search for the student record by id and delete it if it exists in the database using the unlink method of the ORM
            school_student_id = request.env['school.student'].sudo().search([('id', '=', school_student_id)])
            if not school_student_id:
                return Response(json.dumps({
                    "error": " ID does not exist!",
                }), content_type='application/json', status=400)
            school_student_id.unlink()
            # return a simple string "student has been deleted Success"
            return Response(json.dumps({
                "message": "student has been deleted Success",
            }), content_type='application/json', status=200)
        except Exception as Error:
            return Response(json.dumps({
                "error": str(Error)
            }), content_type='application/json', status=400)

    #######################################################################################################
    # 5- method ( Read All = Get All )
    # create a new endpoint that will return all the student records in the database with filtration
    # decorate the method with the route decorator to define the endpoint
    @http.route("/v1/school.students", methods=["GET"], type='http', auth='none', csrf=False)
    # define the method that will be executed when the endpoint
    def get_school_student_list(self):
        try:
            # get the query string parameters from the request for [ filtration ]
            params = parse_qs(request.httprequest.query_string.decode("utf-8"))
            print(params)
            # create an empty list that will contain the domain list
            school_student_domain = []
            # create three variables that will contain the offset and limit and page values for pagination [ offset, limit , page ]
            page = offset = None
            limit = 2
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])
            if page:
                offset = (page * limit) - limit
            print(limit)
            print(page)
            print(offset)
            # check if the name parameter exists in the query string parameters
            if params.get('age'):
                # add the state parameter to the domain list
                school_student_domain += [('age', '=', int(params.get('age')[0]))]
                print(school_student_domain)

            # check if the gender parameter exists in the query string parameters
            if params.get('gender'):
                # add the gender parameter to the domain list
                school_student_domain += [('gender', '=', params.get('gender')[0])]

            # search for all the student records in the database using the search method of the ORM
            # ( Pagination )
            school_student_ids = request.env['school.student'].sudo().search(school_student_domain,
                                                                             offset=offset,
                                                                             limit=limit,
                                                                             order='id desc')  # school_student_domain
            print(school_student_ids)
            school_student_count = request.env['school.student'].sudo().search_count(school_student_domain, )
            print(school_student_count)
            # check if there are no records in the database
            if not school_student_ids:
                return invalid_response("There is are not records!", status=400)

            # return a simple json list that contains the dictanory students
            return valid_response([
                {
                    "id": school_student_id.id,
                    "name": school_student_id.name,
                    "gender": school_student_id.gender,
                    "age": school_student_id.age,
                }
                for school_student_id in school_student_ids
            ], pagination_info={  # Pagination Info ( Meta Data ) [ page, limit, pages, count_records ]
                "page": page if page else 1,
                "limit": limit,
                "pages": math.ceil(school_student_count / limit) if limit else 1,
                "count_records": school_student_count,
            }, status=200)

        except Exception as Error:
            return Response(json.dumps({
                "error": str(Error)
            }), content_type='application/json', status=400)
    #######################################################################################################
