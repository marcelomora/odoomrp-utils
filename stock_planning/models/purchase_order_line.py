# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    def _find_purchase_lines_from_stock_planning(
            self, company, to_date, product, warehouse, location,
            from_date=None):
        cond = [('company_id', '=', company.id),
                ('product_id', '=', product.id),
                ('date_planned', '<=', to_date),
                ('state', '!=', 'cancel')]
        if from_date:
            cond.append(('date_planned', '=>', from_date))
        purchase_lines = self.search(cond)
        purchase_lines = purchase_lines.filtered(
            lambda x: x.order_id.state not in ('cancel', 'except_picking',
                                               'except_invoice', 'done',
                                               'approved'))
        purchase_lines = purchase_lines.filtered(
            lambda x: x.order_id.picking_type_id.warehouse_id.id ==
            warehouse.id)
        purchase_lines = purchase_lines.filtered(
            lambda x: x.order_id.location_id.id == location.id)
        lines = self.env['purchase.order.line']
        for purchase_line in purchase_lines:
            if not purchase_line.procurement_ids:
                lines |= purchase_line
        return lines
