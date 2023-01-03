# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Bales(models.Model):
    _name = 'stock.bale'

    name = fields.Char("Bale Number")
    origin = fields.Char('Source Document')
    bales_line = fields.One2many('stock.bale.line', 'bale', string="Bale Details")


class BalesLine(models.Model):
    _name = 'stock.bale.line'

    bale = fields.Many2one("stock.bale")
    product_id = fields.Many2one('product.product', string="Product")
    code = fields.Char('Code')
    label = fields.Char('label')
    quantity = fields.Float('Quantity')
    unit = fields.Many2one('uom.uom', string="Uom")

    @api.onchange('product_id')
    def onchange_product(self):
        for rec in self:
            if rec.product_id:
                rec.code = rec.product_id.default_code
                rec.label = rec.product_id.name
                rec.unit = rec.product_id.uom_id.id


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def load_bales(self):
        for line in self.move_ids_without_package:
            if line.bale and not line.flag:
                line.flag = True
                for rec in line.bale.bales_line[1:]:
                    lines = {
                        'name': rec.product_id.name,
                        'product_id': rec.product_id.id,
                        'product_uom_qty': rec.quantity,
                        'product_uom': rec.unit.id,
                        'location_id': self.picking_type_id.default_location_src_id.id,
                        'location_dest_id': self.picking_type_id.default_location_dest_id.id,
                    }
                    self.write({'move_ids_without_package': [(0, 0, lines)]})


class StockLine(models.Model):
    _inherit = 'stock.move'

    bale = fields.Many2one('stock.bale', string="Bale")
    flag = fields.Boolean('Flag')
    # display_type = fields.Selection([
    #     ('line_section', "Section"),
    #     ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    @api.depends('bale')
    def get_product_from_bale(self):
        self.product_id = self.bale.bales_line[0].product_id.id
        self.product_uom_qty = self.bale.bales_line[0].quantity

    @api.onchange('bale')
    def onchange_bale(self):
        if self.bale:
            self.product_id = self.bale.bales_line[0].product_id.id
            self.product_uom_qty = self.bale.bales_line[0].quantity
