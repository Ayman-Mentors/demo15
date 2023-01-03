# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class StockLocation(models.Model):
    _inherit = 'stock.location'

    location_name = fields.Selection(string="Location Name",
                                     selection=[('cairo', 'Cairo'), ('alex', 'Alex'), ('mina', 'Mina'), ],
                                     required=False, )
    reserved_location = fields.Boolean(string="Is Reserved Location ")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_name = fields.Char("Project Name")
    quotation_type = fields.Selection([('tender', 'Tender'), ('inhand', 'IN Hand')], string="Quotation Type")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    cairo_hand = fields.Float("Cairo Free", compute="compute_quantity")
    cairo_re = fields.Float("Cairo R", compute="compute_quantity")
    alex_hand = fields.Float("Alex Free", compute="compute_quantity")
    alex_re = fields.Float("Alex R", compute="compute_quantity")
    mina_hand = fields.Float("Mina Free", compute="compute_quantity")
    mine_res = fields.Float("Mina R", compute="compute_quantity")
    reminder_alex = fields.Char('Reminder Alex')
    reminder_mina = fields.Char('Reminder Mina')

    def compute_quantity(self):
        for rec in self:
            quantity_c = 0.0
            quantity_a = 0.0
            quantity_m = 0.0
            free_c = 0.0
            free_a = 0.0
            free_m = 0.0
            stock_quant = self.env['stock.quant'].search([('product_id', '=', rec.product_id.id)])
            for stock in stock_quant:
                if not stock.location_id.reserved_location:

                    if stock.location_id.location_name == 'cairo':
                        quantity_c += stock.quantity
                    if stock.location_id.location_name == 'alex':
                        quantity_a += stock.quantity
                    if stock.location_id.location_name == 'mina':
                        quantity_m += stock.quantity
                else:
                    if stock.location_id.location_name == 'cairo':
                        free_c += stock.quantity
                    if stock.location_id.location_name == 'alex':
                        free_a += stock.quantity
                    if stock.location_id.location_name == 'mina':
                        free_m += stock.quantity

            rec.cairo_hand = quantity_c
            rec.alex_hand = quantity_a
            rec.mina_hand = quantity_m

            if rec.order_id.stock_reservation:
                reserve = self.env['reserved.stock'].search([('sale_order', '=', rec.order_id.id),
                                                             ('state', '=', 'reserved')])
                if reserve:
                    for res in reserve:
                        if res.location_id.location_name == 'cairo':
                            rec.cairo_re = res.reserve_qty - rec.qty_delivered
                        else:
                            rec.cairo_re = 0.0
                        if res.location_id.location_name == 'alex':
                            rec.alex_re = res.reserve_qty - rec.qty_delivered
                        else:
                            rec.alex_re = 0.0
                        if res.location_id.location_name == 'mina':
                            rec.mine_res = res.reserve_qty - rec.qty_delivered
                        else:
                            rec.mine_res = 0.0
                else:
                    rec.cairo_re = 0.0
                    rec.alex_re = 0.0
                    rec.mine_res = 0.0
            else:
                rec.cairo_re = 0.0
                rec.alex_re = 0.0
                rec.mine_res = 0.0

    # quantity_forcasted_stock = fields.Char("Qty forecasted", compute="compute_n_quantity")
    #
    # def compute_n_quantity(self):
    #     for rec in self:
    #         name = ''
    #         stock_quant = self.env['stock.quant'].search([('product_id', '=', rec.product_id.id)])
    #         for stock in stock_quant:
    #             if stock.location_id.location_name == 'cairo':
    #                 quantity_c += stock.quantity
    #             if stock.location_id.location_name == 'alex':
    #                 quantity_a += stock.quantity
    #             if stock.location_id.location_name == 'mina':
    #                 quantity_m += stock.quantity
    #         rec.cairo_hand = quantity_c
    #         rec.alex_hand = quantity_a
    #         rec.mina_hand = quantity_m

    remainder_quantity = fields.Float("Remaining Qty", compute="compute_remainder")

    def compute_remainder(self):
        for rec in self:
            remainder = 0.0
            # if rec.qty_delivered < 0:
            remainder = rec.product_uom_qty - rec.qty_delivered
            rec.remainder_quantity = remainder
