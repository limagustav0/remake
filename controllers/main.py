# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import base64
from dataclasses import dataclass
from requests import post

class RequisicaoFachada(http.Controller):
    @http.route('/remake', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        users = http.request.env['res.users'].sudo().search([])
        partners = http.request.env['res.partner'].sudo().search([])
        facade_ad_type_ids = http.request.env['kami_sm.attendance.ad_type'].search([]),
        #partners = request.env['res.partner'].sudo().search([])
        
        return http.request.render('remake.remake', {
            'partners': partners,
            'users': users,
            'partners': partners,
            #'facade_ad_type_ids': facade_ad_type_ids
        })
    
    @http.route('/facades_request', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        facade_type = http.request.env.ref('kami_sm.facade').id
        date = str(post.get('data_vencimento')).replace('/', '-')
        attachment = http.request.params['task_attachment']

        description = f"""
          <strong>Endereço completo do salão:</strong> {post.get('saloon_address')}<br></br>
          <strong>Nome do Vendedor:</strong> {post.get('seller_name')}<br></br>
          <strong>Arte para fachada:</strong> {post.get('img')}<br></br>
          <strong>Tipo de Aplicação:</strong> {post.get('aplicationtypevalue')}<br></br>
          <strong>Tipos de aplicações adicionais:</strong> {post.get('aditionalapp')}<br></br>
          <strong>Regional solicitante RS?:</strong> {post.get('regional_name') if True else "Não"}
        """

        attendance_vals = {
            'client_id': post.get('saloon_name'),
            'backoffice_user_id': post.get('responsible'),
            'type_id': facade_type,
            'images_position': post.get('position'),
            'facade_width': post.get('width_facade').replace(',', '.'),
            'facade_height': post.get('height_facade').replace(',', '.'),
            'magazine_types': post.get('magazinetype'),
            'magazine_format': post.get('magazineformat'),
            'magazine_width': post.get('magazinewidht').replace(',', '.'),
            'magazine_height': post.get('magazineheight').replace(',', '.'),
            'facade_has_ad': post.get('anuncio_checkbox'),
            'facade_ad_type_id': post.get('ad_type'),
            'has_cutting_edge': post.get('sangria'),
            'cutting_edge_size': post.get('mmsangria').replace(',', '.'),
            'has_safe_margin': post.get('margem'),
            'safe_margin_size': post.get('mmmargem').replace(',', '.'),
            'installation_images': base64.b64encode(attachment.read()),
            'description': description
        }
        new_task = request.env['kami_sm.attendance'].sudo().create(attendance_vals)
        if 'aditional_images' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_images')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "imagens adicionais" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'kami_sm.attendance',
                    'res_id': new_task.id,
                })
        return http.request.render('kami_forms.forms_success_page')
