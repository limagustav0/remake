# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import base64
from dataclasses import dataclass
from requests import post
from datetime import datetime

class RequisicaoFachada(http.Controller):
    @http.route('/fachada', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        users = http.request.env['res.users'].sudo().search([])
        partners = http.request.env['res.partner'].sudo().search([])
        facade_ad_type_ids = http.request.env['kami_sm.attendance.ad_type'].sudo().search([])
        partners = request.env['res.partner'].sudo().search([])
        
        return http.request.render('remake.fachada', {
            'partners': partners,
            'users': users,
            'partners': partners,
            'facade_ad_type_ids': facade_ad_type_ids,
        })
    
    @http.route('/fachada', type='http', auth='public', website=True, methods=['POST'], csrf=False)
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
        return http.request.render('remake.forms_success_page')

class AudioVisual(http.Controller):
    @http.route('/audiovisual', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        return http.request.render('remake.audiovisual', {
        })

    @http.route('/audiovisual', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):

        quadrado = post.get('quadrado')
        vertical = post.get('vertical')
        horizontal = post.get('horizontal')
        ig = post.get('ig')

        youtube = post.get('Youtube')
        facebook = post.get('Facebook')
        instagram = post.get('Instagram')
        whatsapp = post.get('WhatsApp')
        stories = post.get('Stories')
        linkedin = post.get('LinkedIn')
        reels = post.get('Reels')

        quadrado = quadrado if quadrado == 'Quadrado 1:1 (1080x1080)' else ''
        vertical = vertical if vertical == 'Vertical 9:16 (1080x1920)' else ''
        horizontal = horizontal if horizontal == 'Horizontal 16:9 (1920x1080)' else ''
        ig = ig if ig == 'IG 4:5 (1080x1350)' else ''

        youtube = youtube if youtube == 'Youtube' else ''
        facebook = facebook if facebook == 'Facebook' else ''
        instagram = instagram if instagram == 'Instagram' else ''
        whatsapp = whatsapp if whatsapp == 'WhatsApp' else ''
        stories = stories if stories == 'Stories' else ''
        linkedin = linkedin if linkedin == 'LinkedIn' else ''
        reels = reels if reels == 'Reels' else ''

        project_id = request.env.ref('remake.audiovisual').id
        description = f"""
            Seu nome:{post.get('nome')}<br></br>
            Departamento:{post.get('departamento')}<br></br>
            Título da solicitação:{post.get('tituloSolicitacao')}<br></br>
            Demanda:{post.get('demanda')}<br></br>
            Data da captação:{post.get('dataCaptacao')}<br></br>
            Precisa de fotos:{post.get('precisaFoto')}<br></br>
            Resolução:{post.get('resolucao')}<br></br>
            Refere a empresa KAMI:{post.get('referenteKami')}<br></br>
            Proporção do arquivo:{quadrado, vertical, horizontal, ig}<br></br>
            Tempo de vídeo estimado:{post.get('tamanhoVideo')}<br></br>
            Onde deseja compartilhá-la:{youtube, facebook, instagram, whatsapp, stories, linkedin, reels}  -  Quais outros locais:{post.get('outrosLocais')}<br></br>
            Trilha ou referência de trilha:{post.get('trilhaReferencia')}<br></br>
            Lettering/GC:{post.get('lettering')} -- O que?{post.get('oQue')}<br></br>
            Incluir logotipo:{post.get('incluiLogotipo')} -- {post.get('logotipoLocal')}<br></br>
            Animação:{post.get('animacao')}<br></br>
            Referência:{post.get('referencia')}<br></br>
            Detalhes da solicitação:{post.get('detalhesSolicitacao')}<br></br>
            Briefing/Roteiro:{post.get('briefing')}<br></br>
            Prazo de entrega estimado:{post.get('prazoEntrega')}<br></br>
        """
        task_vals = {
            'name': f"{post.get('nome')}-{post.get('departamento')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = request.env["project.task"].sudo().create(task_vals)

        if 'task_attachment' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('task_attachment')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,

                })
        return http.request.render('remake.forms_success_page')
    
class HelpdeskTicket(http.Controller):
    @http.route('/helpdeskticket', auth='public', csrf=False, website=True)
    def index(self, **kw):
        types = http.request.env['helpdesk.ticket.type']
        categories = http.request.env['helpdesk.ticket.category']
        priorities = {
            0: _('Baixa'),
            1: _('Média'),
            2: _('Alta'),
            3: _('Urgente')
        }
        return http.request.render('remake.helpdesk_ticket', {
            'types': types.sudo().search([]),
            'categories': categories.sudo().search([]),
            'priorities': priorities
        })

    @http.route('/helpdeskticket', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        ticket_vals = {
            'name': f"{post.get('subject')}",
            'type_id': int(post.get('type')),
            'category_id': int(post.get('category')),
            'description': post.get('description'),
            'priority': post.get('priority')
        }

        new_ticket = http.request.env["helpdesk.ticket"].sudo().create(
            ticket_vals)
        if 'attachment' in http.request.params:
            attached_files = http.request.httprequest.files.getlist(
                'attachment')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'helpdesk.ticket',
                    'res_id': new_ticket.id,
                })
        return http.request.render('remake.forms_success_page')
    
class MalaTecnica(http.Controller):
    @http.route('/malatecnica', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        users = http.request.env['res.users']
        return http.request.render('remake.mala_tecnica', {
            'users': users.sudo().search([]),
        })

    @http.route('/malatecnica', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.mala_tecnica_project').id
        description = f"""
                Departamento:{post.get('department')} <br></br>
                Solicitação:{post.get('solicitation')} <br></br>
                Responsavel:{post.get('responsible')} <br></br>
                Observações / Solicitação:{post.get('comments')}
        """
        new_task = {
            'name': f"{post.get('department')}-{post.get('solicitation')}",
            'project_id': project_id,
            'user_id': int(post.get('responsible')),
            'description': description,
        }
        http.request.env["project.task"].sudo().create(new_task)
        return http.request.render('remake.forms_success_page', {})
    
class PlanejamentoCampanhaMarketing(http.Controller): 
    @http.route('/planejamentocampanhamarketing', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        return http.request.render('remake.planejamentocampanhamarketing', {
        })

    @http.route('/planejamentocampanhamarketing', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.digital_invite_project').id
        description = f"""
            Nome da campanha:{post.get('nomeCampanha')}<br></br>
            Tipos de Campanha:{post.get('tipoCampanha')}<br></br>
            Ano:{post.get('ano')}<br></br>
            Briefing da campanha:{post.get('briefing')}<br></br>
            periodo:{post.get('periodo')}<br></br>
            Vencimento do Planejamento:{post.get('dataVencimento')}<br></br>
        """
        new_task = {
            'name': f"{post.get('nomeCampanha')}-{post.get('tipoCampanha')}-{post.get('ano')}",
            'project_id': project_id,
            'description': description,
        }
        http.request.env["project.task"].sudo().create(new_task)
        return http.request.render('remake.forms_success_page', {})
    
class ControleRomaneio(http.Controller): 
    @http.route('/romaneio', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        companyes = http.request.env['res.company'].sudo().search([])
        return http.request.render('remake.romaneio', {
            'companyes' : companyes,
        })
    
    @http.route('/romaneio', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.controle_romaneio').id
        description = f"""
            Empresa: {post.get('company_name')}<br><br/>
            Número do Romaneio: {post.get('number_romaneio')}<br><br/>
            Data de Saída: {post.get('exit_date')}<br><br/>

        """
        new_task = {
            'name': {post.get('company_name')},
            'project_id': project_id,
            'description': description,
        }
        http.request.env["project.task"].sudo().create(new_task)
        return http.request.render('remake.forms_success_page', {})
    
class GerenciamentoInvasaoTruss(http.Controller): 
    @http.route('/invasaotruss', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):

        return http.request.render('remake.invasaotruss', {

        })
    
    @http.route('/invasaotruss', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.invasao_truss').id

        data_recebimento = datetime.strptime(post.get('dataRecebimento'), '%Y-%m-%dT%H:%M')
        data_recebimento_formatada = data_recebimento.strftime('%d/%m/%Y - %H:%M')

        description = f"""
            Tipo Notificação: {post.get('region_invasion') if post.get('region_invasion') else " "}     {post.get('invalid_sell') if post.get('invalid_sell') else " "}<br><br/>
            Data de Recebimento: {data_recebimento_formatada}<br><br/>
            Empresa Notificada: {post.get('Movement') if post.get('Movement') else " "}     {post.get('NewHauss') if post.get('NewHauss') else " "}     {post.get('RiodeJaneiro') if post.get('RiodeJaneiro') else " "}<br><br/>
            Prazo de Resposta: {post.get('Prazo')}<br><br/>
            Número ''OCTADESK: {post.get('octadesk_number')}<br><br/>
            Local onde o produto foi encontrado: {post.get('found_location')}<br><br/>
            Nome do Cliente: {post.get('client_name')}<br><br/>
            Prioridade: {post.get('priority')}<br><br/>
        """
        new_task = {
            'name': f"Notificações TRUSS - {post.get('priority')} PRIORIDADE",
            'project_id': project_id,
            'description': description,
        }
        new_task = http.request.env["project.task"].sudo().create(new_task)
        if 'aditional_archives' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('remake.forms_success_page')

class CriativoKamico(http.Controller): 
    @http.route('/criativo', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        return http.request.render('remake.criativo')
    
    @http.route('/criativo', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.criativo_kami').id


        data_prazo = datetime.strptime(post.get('data_prazo'), '%Y-%m-%dT%H:%M')
        data_prazo_formatada = data_prazo.strftime('%d/%m/%Y - %H:%M')


        description = f"""
            Título da solicitação: {post.get('notification_title')}<br/><br/>
            Essa solicitação se refere a qual empresa KAMI?: {post.get('solicitation')}<br/><br/>

            Tipo da solicitação: {post.get('notification_type')}<br/><br/>

            Onde deseja compartilhá-la?: {post.get('Email') if post.get('Email') else " "}<br/>
                                 {post.get('Mídiassociais') if post.get('Mídiassociais') else " "}<br/>
                                 {post.get('Youtube') if post.get('Youtube') else " "}<br/>
                                 {post.get('WhatsApp') if post.get('WhatsApp') else " "}<br/>
                                 {post.get('Stories') if post.get('Stories') else " "}<br/>
                                 {post.get('Materialimpresso') if post.get('Materialimpresso') else " "}<br/>
                                 {post.get('Workplace') if post.get('Workplace') else " "}<br/>
                                 {post.get('LinkedIn') if post.get('LinkedIn') else " "}<br/>
                                 {post.get('Outroslocais') if post.get('Outroslocais') else " "}<br/><br/><br/>

            Inserir Logotipo: {post.get('KAMICO') if post.get('KAMICO') else ""}<br/>
                              {post.get('SBMP') if post.get('SBMP') else ""}<br/>
                              {post.get('TRUSSHair') if post.get('TRUSSHair') else ""}<br/>
                              {post.get('HairSPA') if post.get('HairSPA') else ""}<br/>
                              {post.get('HairPro') if post.get('HairPro') else ""}<br/>
                              {post.get('LogodoCliente') if post.get('LogodoCliente') else ""}<br/>
                              {post.get('Outros') if post.get('Outros') else ""}<br/>
                              {post.get('SemLogo') if post.get('SemLogo') else ""}<br/><br/><br/>
            
            
            Detalhes da solicitação: {post.get('solicitation_detail')}<br/><br/><br/>

            Prazo de entrega estimado: {data_prazo_formatada}<br/><br/><br/>

            Seu nome: {post.get('yourname')}<br/><br/><br/>

            Seu e-mail: {post.get('yourmail')}<br/><br/><br/>

            Whatsapp: {post.get('celular')}<br/><br/><br/>

            Por onde você deseja receber o arquivo final?: {post.get('email')} {post.get('whatsapp')}<br/><br/><br/>
        """
        new_task = {
            'name': f"Criativo - {post.get('solicitation')}",
            'project_id': project_id,
            'description': description,
        }
        new_task = http.request.env["project.task"].sudo().create(new_task)
        if 'aditional_archives' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('remake.forms_success_page')

class LancamentoEducacionalMvp(http.Controller):
    @http.route('/educacionalmvp', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        users = http.request.env['res.users']
        return http.request.render('remake.educacionalmvp', {
            'users': users.search([])
        })

    @http.route('/educacionalmvp', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.lancamento_educacional_mvp').id
        description = f"""
                Atividade:{post.get('atividade')}<br></br>
                Descrição da atividade:{post.get('descricaoAtividade')}<br></br>
                Data preferida para entrega:{post.get('dataEntrega')}<br></br>
                Prioridade:{post.get('priority')}<br></br>
                Responsável pela atividade:{post.get('responsavel')}<br></br>
        """
        new_task = {
            'name': f"{post.get('atividade')}-{post.get('responsavel')}-{post.get('priority')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = http.request.env["project.task"].sudo().create(new_task)
        if 'anexo' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('anexo')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('remake.forms_success_page')
    
class PromotoriaFreelancer(http.Controller):
    @http.route('/promotoriafreelancer', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        partners = http.request.env['res.partner'].sudo().search([])
        users = http.request.env['res.users'].sudo().search([])
        return http.request.render('remake.promotoriafreelancer', {
            'partners' : partners,
            'users' : users,
        })

    # @http.route('/promotoriafreelancer', auth='public', type="http", website=True, methods=['post'], csrf=False)
    # def create(self, **post):
    #     #project_id = request.env.ref('remake.digital_invite_project').id
    #     description = f"""
    #             Nome do vendedor:{post.get('nomeVendedor')}<br></br>
    #             Email do vendedor:{post.get('emailVendedor')}<br></br>
    #             Nome da Loja:{post.get('nomeLoja')}<br></br>
    #             Código do cliente:{post.get('codCliente')}<br></br>
    #             Data da atividade:{post.get('dataAtividade')}<br></br>
    #             Horário do Evento:{post.get('horarioEvento')}<br></br>
    #             Endereço completo da Loja:{post.get('enderecoLoja')}<br></br>
    #             Tipo de atendimento:{post.get('tipoAtendimento')}<br></br>
    #             Observações do cliente:{post.get('observacoesImportantes')}<br></br>
    #     """
    #     new_task = {
    #         'name': f"{post.get('nomeVendedor')}-{post.get('nomeLoja')}-{post.get('codCliente')}",
    #         'description': description,
    #     }
    #     http.request.env["project.task"].sudo().create(new_task)
    #     return http.request.render('kami_forms.forms_success_page', {})

class CampanhaMKT(http.Controller):
    @http.route('/campanhamkt', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        return http.request.render('remake.campanhamkt')
    
    @http.route('/campanhamkt', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.campanhas_mkt').id

        data_inicio = datetime.strptime(post.get('data_inicio'), '%Y-%m-%dT%H:%M')
        data_inicio_formatada = data_inicio.strftime('%d/%m/%Y - %H:%M')

        data_vencimento = datetime.strptime(post.get('data_vencimento'), '%Y-%m-%dT%H:%M')
        data_vencimento_formatada = data_vencimento.strftime('%d/%m/%Y - %H:%M')

        description = f"""
                <strong>Empresa:</strong> {post.get('empresa')}<br></br>
                <strong>Ano:</strong> {post.get('ano')}<br></br>
                <strong>Periodo:</strong> {post.get('trimestre')}<br></br>
                <strong>Início:</strong> {data_inicio_formatada}<br></br>
                <strong>Vencimento do Planejamento:</strong> {data_vencimento_formatada}<br></br>
                <strong>Tipos de Campanha:</strong><br></br>
                                   {post.get('lancamento') if post.get('lancamento') else " "}<br></br>
                                   {post.get('branding') if post.get('lancamento') else " "}<br></br>
                                   {post.get('comercial') if post.get('lancamento') else " "}<br></br>
                                   {post.get('fluxo') if post.get('lancamento') else " "}<br></br>
                                   {post.get('encantamento') if post.get('lancamento') else " "}<br></br>
                                   {post.get('reativacao') if post.get('lancamento') else " "}<br></br>

        """
        new_task = {
            'name': f"Campannha - {post.get('empresa')} - {post.get('ano')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = http.request.env["project.task"].sudo().create(new_task)
        return http.request.render('remake.forms_success_page')
    
class SolicitacaoRedeSocial(http.Controller):
    @http.route('/solicitacaoredesocial', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        return http.request.render('remake.solicitacaoredesocial')
    
    @http.route('/solicitacaoredesocial', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.solicitacao_redes_sociais').id
        description = f"""
                <strong>Assunto:</strong> {post.get('subject')}<br></br>
                <strong>Onde será publicado?:</strong> {post.get('publi')}<br></br>
                <strong>Briefing:</strong> {post.get('briefing')}<br></br>
                <strong>Legenda:</strong> {post.get('legenda')}<br></br>
                <strong>Data da Publicação:</strong> {post.get('pud_date')}<br></br>
        """
        new_task = {
            'name': f"Social Mídia - {post.get('subject')} - {post.get('publi')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = http.request.env["project.task"].sudo().create(new_task)
        if 'aditional_archives_reference' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives_reference')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "REFERÊNCIAS" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task', 
                    'res_id': new_task.id,
                })

        if 'aditional_archives_layout' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives_layout')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "LAYOUT" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task', 
                    'res_id': new_task.id,
                })

        if 'aditional_archives_story' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives_story')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "STORY" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',  
                    'res_id': new_task.id,
                })
        return http.request.render('remake.forms_success_page')

class CursosKamico(http.Controller):
    @http.route('/cursoskamico', auth='public', csrf=False, website='True')
    def index(self, **kw): 
         return http.request.render('remake.cursoskamico', {
         })

    @http.route('/cursoskamico', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.cursos_kamico_project').id
        description = f"""
            Nome do Vendedor:{post.get('nomeVendedor')}<br></br>
            Nome completo do Aluno:{post.get('nomeAluno')}<br></br>
            WhatsApp do Aluno:{post.get('whatsappAluno')}<br></br>
            Email do Aluno:{post.get('emallAluno')}<br></br>
            Classificação do aluno:{post.get('classificacaoAluno')}<br></br>
            Nome do salão que o aluno trabalha:{post.get('salaoAluno')}<br></br>
            Região do salão:{post.get('regiaoSalao')}<br></br>
            Código do cliente no UNO:{post.get('codClientUno')}<br></br>
            Código do pedido do cliente no UNO:{post.get('codPedidoUno')}<br></br>
            Forma de pagamento:{post.get('formaPagamento')}<br></br>
            Referente ao curso:{post.get('cursoReferencia')}<br></br>
            Observações:{post.get('observacao')}<br></br>
        
        """
        task_vals = {
            'name': f"{post.get('nomeVendedor')}-{post.get('nomeAluno')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = request.env["project.task"].sudo().create(task_vals)

        if 'task_attachment'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('task_attachment')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,

                })
        return http.request.render('remake.forms_success_page')
    
class FormularioRH(http.Controller):
    @http.route('/formulariorh', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        return http.request.render('remake.formulariorh')

    @http.route('/formulariorh', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('remake.solicitacao_rh_project').id
        description = f"""
                NOME COMPLETO: {post.get('nomeCompleto')}<br></br>
                NOME SOCIAL: {post.get('nomeSocial')}<br></br>
                CNPJ: {post.get('cnpj')}<br></br>
                NOME PAI: {post.get('nomePai')}<br></br>
                NOME MÃE: {post.get('nomeMae')}<br></br>
                DATA NASCIMENTO: {post.get('dataNascimento')}<br></br>
                MUNICIPIO DE NASCIMENTO: {post.get('municipioNascimeno')}<br></br>
                UF: {post.get('uf')}<br></br>
                PAÍS DE NASCIMENTO: {post.get('paisNascimento')}<br></br>
                GÊNERO: {post.get('genero')}<br></br>
                ESTADO CIVIL: {post.get('estadoCivil')}<br></br>
                ENDEREÇO RESIDENCIAL: {post.get('enderecoResidencial')}<br></br>
                BAIRRO: {post.get('bairro')}<br></br>
                CEP: {post.get('cep')}<br></br>
                ESTADO: {post.get('estado')}<br></br>
                EMAIL PESSOAL: {post.get('emailPessoal')}<br></br>
                TAMANHO DA ROUPA: {post.get('tamanhoRoupa')}<br></br>
                TAMANHO DO SAPATO: {post.get('tamanhoSapato')}<br></br>
                BANCO: {post.get('banco')}<br></br>
                AGÊNCIA: {post.get('agencia')}<br></br>
                NÚMERO DA CONTA: {post.get('numeroConta')}<br></br>
                TIPO DE CONTA: {post.get('tipoConta')}<br></br>
                PIX: {post.get('pix')}<br></br>
                NÚMERO DO RG: {post.get('numeroRg')}<br></br>
                ORGÃO EMISSOR: {post.get('orgaoEmissor')}<br></br>
                DATA DA EXPEDIÇÃO: {post.get('dataExpedicao')}<br></br>
                NUMERO DO CPF: {post.get('numeroCpf')}<br></br>
                PERIODO DA PRESTAÇÃO DE SERVIÇO (DATA INICIO): {post.get('prestacaoServicoInicio')}<br></br>
                PERIODO DA PRESTAÇÃO DE SERVIÇO (DATA FINAL): {post.get('prestacaoServicoFim')}<br></br>
                FUNÇÃO: {post.get('funcao')}<br></br>
                VALOR DO PAGAMENTO: {post.get('valorPagamento')}<br></br>
                AJUDA DE CUSTO: {post.get('ajudaCusto')}<br></br>
                OUTROS: {post.get('outros')}<br></br>
        """
        task_vals = {
            'name': f"{post.get('nomeCompleto')}-{post.get('funcao')}",
            'project_id': project_id,
            'description': description,
        }
        new_task = request.env["project.task"].sudo().create(task_vals)
        if 'anexo'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('anexo')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('remake.forms_success_page')
    
class EducacionalContent(http.Controller):
    @http.route('/educacionalcontent', auth='public', csrf=False, website='True')
    def index(self, **kw):
        return http.request.render('remake.educacionalcontent', {
        })

    @http.route('/educacionalcontent', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref("remake.educacional_content_project").id
        description = f"""
                Capa (HEADLINE):{post.get('capaHeadline')}<br></br>
                Onde será publicado:{post.get('pulicacao')}<br></br>
                Formato:{post.get('formato')}<br></br>
                Selo:{post.get('selo')}<br></br>
                Referências:{post.get('referencia')}<br></br>
                Briefing Tema:{post.get('briefingTema')}<br></br>
                Legenda:{post.get('legenda')}<br></br>
                Briefing do Criativo:{post.get('briefingCriativo')}<br></br>
                Data da Publicação:{post.get('dataPublicacao')}<br></br>
        """
        task_vals = {
            'name': f"{post.get('capaHeadline')}-{post.get('pulicacao')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = request.env["project.task"].sudo().create(task_vals)

        if 'task_attachment_referencias'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('task_attachment_referencias')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "REFERENCIAS" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        if 'task_attachment_layout'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('task_attachment_layout')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "LAYOUT" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        
        if 'story_task_attachment'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('story_task_attachment')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "STORY" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('remake.forms_success_page')
  

class NovoProduto(http.Controller): 
    @http.route('/novoproduto', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        users = http.request.env['res.users'].sudo().search([])
        return http.request.render('remake.novoproduto', {
            'users': users,
        })
    
    # @http.route('/novoproduto', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    # def create(self, **post):
        
    #     description = f"""
    #         Empresa: {post.get('company_name')}<br><br/>
    #         Número do Romaneio: {post.get('number_romaneio')}<br><br/>
    #         Data de Saída: {post.get('exit_date')}<br><br/>

    #     """
    #     new_task = {
    #         'name': {post.get('company_name')},
    #         'project_id': project_id,
    #         'description': description,
    #     }
    #     http.request.env["project.task"].sudo().create(new_task)
    #     return http.request.render('remake.forms_success_page', {})

class TradeMarketing(http.Controller):
    @http.route('/trademarketing', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        users = http.request.env['res.users'].sudo().search([])
        partners = http.request.env['res.partner'].sudo().search([])
        facade_ad_type_ids = http.request.env['kami_sm.attendance.ad_type'].sudo().search([])
        partners = request.env['res.partner'].sudo().search([])
        
        return http.request.render('remake.trademarketing', {
            'partners': partners,
            'users': users,
        })

