from odoo import http


# create a new controller that will contain the endpoint
class TestApi(http.Controller):

    #  create a new endpoint that will return a simple string "Hello world, Eslam Mohamed Junior Odoo Developer"
    @http.route('/test/api', methods=["GET"], type='http', auth='none', csrf=False)
    # http://localhost:8069/test/api -> Hello, world Eslam Mohamed Junior Odoo Developer
    def test_endpoint(self, **kw):
        print("Hello world, Eslam Mohamed Junior Odoo Developer")
