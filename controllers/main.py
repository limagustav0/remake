# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import base64
from dataclasses import dataclass

class remake(http.Controller):
    @http.route('/remake', auth='public', csrf=False)
    def index(self, **kw):
        return http.request.render('novo_modulo.remake', {
        })

    # @http.route('/remake', auth='public', type="http", website=True, methods=['post'], csrf=False)
    # def create(self, **post):
    #     #project_id = request.env.ref('kami_forms.digital_invite_project').id
        
    #     http.request.env["project.task"].sudo().create(new_task)
    #     return http.request.render('kami_forms.forms_success_page', {})