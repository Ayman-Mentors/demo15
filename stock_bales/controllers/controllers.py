# -*- coding: utf-8 -*-
# from odoo import http


# class StockBales(http.Controller):
#     @http.route('/stock_bales/stock_bales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_bales/stock_bales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_bales.listing', {
#             'root': '/stock_bales/stock_bales',
#             'objects': http.request.env['stock_bales.stock_bales'].search([]),
#         })

#     @http.route('/stock_bales/stock_bales/objects/<model("stock_bales.stock_bales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_bales.object', {
#             'object': obj
#         })
