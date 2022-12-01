# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import base64
import io
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas

def _fix_image_transparency(image):
    """ Modify image transparency to minimize issue of grey bar artefact.

    When an image has a transparent pixel zone next to white pixel zone on a
    white background, this may cause on some renderer grey line artefacts at
    the edge between white and transparent.

    This method sets transparent pixel to white transparent pixel which solves
    the issue for the most probable case. With this the issue happen for a
    black zone on black background but this is less likely to happen.
    """
    pixels = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if pixels[x, y] == (0, 0, 0, 0):
                pixels[x, y] = (255, 255, 255, 0)

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        # Check for reports only available for invoices.
        res = super(IrActionsReport, self)._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)
        result = res[0]
        company_id = self.env.user.company_id
        report_sudo = self.sudo()._get_report(report_ref)
        if company_id and company_id.related_model_ids and self.env.user.has_group('add_attachment_to_report.group_attachment_in_print_manager'):
            if report_sudo.model in [related_model_id.model for related_model_id in company_id.related_model_ids]:
                def close_streams(streams):
                    for stream in streams:
                        try:
                            stream.close()
                        except Exception:
                            pass

                # Transform the bytes to streams
                streams = [io.BytesIO(res[0])]
                # Get the modul ids
                record_ids = self.env[report_sudo.model].browse([res_id for res_id in res_ids if res_id])
                # Get related attachment ids
                attachment_ids = self.env['ir.attachment'].search(
                    [('res_id', 'in', record_ids.ids), ('res_model', '=', report_sudo.model)])
                if attachment_ids:
                    for attachment_id in attachment_ids:
                        packet = io.BytesIO()
                        can = canvas.Canvas(packet)
                        if attachment_id.mimetype.endswith('application/pdf'):
                            try:
                                # Decode PDF files to bytes
                                file_decode = base64.b64decode(attachment_id.datas)
                                # Convert to stream
                                pdf_content_stream = io.BytesIO(file_decode)
                            except Exception:
                                continue
                            streams.append(pdf_content_stream)
                        elif attachment_id.mimetype.startswith('image'):
                            try:
                                image_reader = ImageReader(io.BytesIO(base64.b64decode(attachment_id.datas)))
                                _fix_image_transparency(image_reader._image)
                                writer = PdfFileWriter()
                            except:
                                continue
                            can.drawImage(image_reader, 70, 200, 460, 460, 'auto', True)
                            can.showPage()
                            can.save()
                            _pdf = PdfFileReader(packet, overwriteWarnings=False)
                            writer.addPage(_pdf.getPage(0))
                            output = io.BytesIO()
                            writer.write(output)
                            streams.append(output)

                if len(streams) == 1:
                    result = streams[0].getvalue()
                else:
                    with self._merge_pdfs(streams) as pdf_merged_stream:
                        result = pdf_merged_stream.getvalue()
                close_streams(streams)
        return [result, res[1]]
