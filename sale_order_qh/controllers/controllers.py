# -*- coding: utf-8 -*-
# from odoo import http


# class ImportExcel(http.Controller):
#     @http.route('/import_excel/import_excel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/import_excel/import_excel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('import_excel.listing', {
#             'root': '/import_excel/import_excel',
#             'objects': http.request.env['import_excel.import_excel'].search([]),
#         })

#     @http.route('/import_excel/import_excel/objects/<model("import_excel.import_excel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('import_excel.object', {
#             'object': obj
#         })
