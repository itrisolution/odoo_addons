# -*- coding: utf-8 -*-

from PyPDF2 import utils
from odoo.exceptions import UserError
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

    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        result = super(IrActionsReport, self)._post_pdf(save_in_attachment, pdf_content, res_ids)
        company_id = self.env.user.company_id
        if company_id and company_id.related_model_ids and self.env.user.has_group('add_attachment_to_report.group_attachment_in_print_manager'):
            if self.model in [related_model_id.model for related_model_id in company_id.related_model_ids]:
                def close_streams(streams):
                    for stream in streams:
                        try:
                            stream.close()
                        except Exception:
                            pass

                # Transform the bytes to streams
                streams = [io.BytesIO(result)]
                # Get the modul ids
                record_ids = self.env[self.model].browse([res_id for res_id in res_ids if res_id])
                # Get related attachment ids
                attachment_ids = self.env['ir.attachment'].search(
                    [('res_id', 'in', record_ids.ids), ('res_model', '=', self.model)])
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
                    try:
                        result = self._merge_pdfs(streams)
                    except utils.PdfReadError:
                        raise UserError(_("File is encrypted"))

                close_streams(streams)
        return result
