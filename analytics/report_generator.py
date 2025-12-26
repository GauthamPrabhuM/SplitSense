"""
Analytics Report Generator
Generates a visually appealing, modern analytics report with charts and colors.
"""
from typing import Dict, Any, List
from decimal import Decimal
from datetime import datetime
from io import BytesIO
import math

# PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Wedge
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF


# Modern color palette
class Colors:
    PRIMARY = colors.HexColor('#6366f1')
    PRIMARY_DARK = colors.HexColor('#4f46e5')
    SUCCESS = colors.HexColor('#10b981')
    WARNING = colors.HexColor('#f59e0b')
    DANGER = colors.HexColor('#ef4444')
    INFO = colors.HexColor('#3b82f6')
    
    TEXT_PRIMARY = colors.HexColor('#1f2937')
    TEXT_SECONDARY = colors.HexColor('#6b7280')
    TEXT_MUTED = colors.HexColor('#9ca3af')
    
    BG_LIGHT = colors.HexColor('#f9fafb')
    BG_CARD = colors.HexColor('#ffffff')
    BORDER = colors.HexColor('#e5e7eb')
    
    CHART_COLORS = [
        colors.HexColor('#6366f1'),
        colors.HexColor('#8b5cf6'),
        colors.HexColor('#ec4899'),
        colors.HexColor('#f43f5e'),
        colors.HexColor('#f97316'),
        colors.HexColor('#eab308'),
        colors.HexColor('#22c55e'),
        colors.HexColor('#14b8a6'),
    ]


class ReportGenerator:
    """Generates modern, visually appealing analytics reports"""
    
    PAGE_WIDTH, PAGE_HEIGHT = A4
    MARGIN = 1.5 * cm
    CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN
    
    def __init__(self):
        self.styles = self._create_styles()
    
    def _create_styles(self):
        return {
            'title': ParagraphStyle(
                'Title',
                fontName='Helvetica-Bold',
                fontSize=24,
                leading=28,
                alignment=TA_LEFT,
                textColor=Colors.TEXT_PRIMARY,
                spaceAfter=2*mm,
            ),
            'subtitle': ParagraphStyle(
                'Subtitle',
                fontName='Helvetica',
                fontSize=11,
                leading=14,
                alignment=TA_LEFT,
                textColor=Colors.TEXT_SECONDARY,
                spaceAfter=6*mm,
            ),
            'section_title': ParagraphStyle(
                'SectionTitle',
                fontName='Helvetica-Bold',
                fontSize=14,
                leading=18,
                alignment=TA_LEFT,
                textColor=Colors.PRIMARY_DARK,
                spaceBefore=8*mm,
                spaceAfter=4*mm,
            ),
            'card_title': ParagraphStyle(
                'CardTitle',
                fontName='Helvetica-Bold',
                fontSize=10,
                leading=12,
                alignment=TA_LEFT,
                textColor=Colors.TEXT_SECONDARY,
            ),
            'card_value': ParagraphStyle(
                'CardValue',
                fontName='Helvetica-Bold',
                fontSize=20,
                leading=24,
                alignment=TA_LEFT,
                textColor=Colors.TEXT_PRIMARY,
            ),
            'body': ParagraphStyle(
                'Body',
                fontName='Helvetica',
                fontSize=10,
                leading=14,
                alignment=TA_LEFT,
                textColor=Colors.TEXT_PRIMARY,
                spaceAfter=3*mm,
            ),
            'small': ParagraphStyle(
                'Small',
                fontName='Helvetica',
                fontSize=8,
                leading=10,
                alignment=TA_LEFT,
                textColor=Colors.TEXT_MUTED,
            ),
        }
    
    def _format_currency(self, amount, currency='INR'):
        symbols = {'INR': 'Rs.', 'USD': '$', 'EUR': 'E', 'GBP': 'L'}
        symbol = symbols.get(currency, currency + ' ')
        if abs(amount) >= 100000:
            return f"{symbol}{amount/100000:,.1f}L"
        elif abs(amount) >= 1000:
            return f"{symbol}{amount/1000:,.1f}K"
        return f"{symbol}{amount:,.0f}"
    
    def _create_stat_card(self, title, value, color=None, width=0):
        if color is None:
            color = Colors.PRIMARY
        card_width = width or (self.CONTENT_WIDTH / 4 - 3*mm)
        d = Drawing(card_width, 4)
        d.add(Rect(0, 0, card_width, 4, fillColor=color, strokeColor=None))
        card_data = [
            [d],
            [Paragraph(title, self.styles['card_title'])],
            [Paragraph(value, self.styles['card_value'])],
        ]
        card = Table(card_data, colWidths=[card_width])
        card.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), Colors.BG_CARD),
            ('BOX', (0, 0), (-1, -1), 0.5, Colors.BORDER),
            ('TOPPADDING', (0, 0), (-1, 0), 0),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
            ('LEFTPADDING', (0, 1), (-1, -1), 8),
            ('RIGHTPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, 1), 8),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        return card
    
    def _create_pie_chart(self, data, width=150, height=120):
        d = Drawing(width, height)
        if not data:
            return d
        pc = Pie()
        pc.x = width / 2 - 35
        pc.y = 10
        pc.width = 70
        pc.height = 70
        pc.data = [item.get('value', 0) for item in data[:6]]
        pc.labels = [item.get('label', '')[:12] for item in data[:6]]
        for i, clr in enumerate(Colors.CHART_COLORS[:len(pc.data)]):
            pc.slices[i].fillColor = clr
            pc.slices[i].strokeColor = colors.white
            pc.slices[i].strokeWidth = 1
        pc.slices.fontName = 'Helvetica'
        pc.slices.fontSize = 7
        pc.slices.labelRadius = 1.3
        d.add(pc)
        return d
    
    def _create_bar_chart(self, data, width=200, height=100):
        d = Drawing(width, height)
        if not data:
            return d
        sorted_months = sorted(data.keys())[-6:]
        values = [float(data.get(m, 0)) for m in sorted_months]
        labels = [m[-5:] for m in sorted_months]
        if not values or max(values) == 0:
            return d
        bc = VerticalBarChart()
        bc.x = 30
        bc.y = 20
        bc.width = width - 50
        bc.height = height - 35
        bc.data = [values]
        bc.categoryAxis.categoryNames = labels
        bc.categoryAxis.labels.fontName = 'Helvetica'
        bc.categoryAxis.labels.fontSize = 7
        bc.valueAxis.labels.fontName = 'Helvetica'
        bc.valueAxis.labels.fontSize = 7
        bc.bars[0].fillColor = Colors.PRIMARY
        bc.bars[0].strokeColor = None
        bc.barWidth = 12
        d.add(bc)
        return d
    
    def _create_progress_bar(self, value, max_value, width=100, color=None):
        if color is None:
            color = Colors.PRIMARY
        d = Drawing(width, 8)
        d.add(Rect(0, 2, width, 4, fillColor=Colors.BG_LIGHT, strokeColor=None))
        fill_width = min((value / max_value) * width, width) if max_value > 0 else 0
        if fill_width > 0:
            d.add(Rect(0, 2, fill_width, 4, fillColor=color, strokeColor=None))
        return d
    
    def _generate_narrative(self, insights, friends):
        currency = insights.get('data_summary', {}).get('original_currency', 'INR')
        spending = insights.get('spending', {})
        balance = insights.get('balance', {})
        categories = insights.get('categories', {})
        groups = insights.get('groups', {})
        anomalies = insights.get('anomalies', {}).get('anomalies', [])
        
        total_spending = float(spending.get('total_spending', 0))
        monthly_avg = float(spending.get('monthly_average', 0)) if spending.get('monthly_average') else 0
        net_balance = float(balance.get('net_balance', 0))
        
        date_range = insights.get('data_summary', {}).get('date_range', {})
        earliest_raw = date_range.get('earliest')
        latest_raw = date_range.get('latest')
        
        def format_date(d):
            if d is None:
                return 'N/A'
            if isinstance(d, datetime):
                return d.strftime('%b %Y')
            if isinstance(d, str):
                try:
                    dt = datetime.fromisoformat(d.replace('Z', '+00:00'))
                    return dt.strftime('%b %Y')
                except:
                    return d[:7]
            return str(d)[:7]
        
        people_owe_you = [f for f in friends if f.get('balance', 0) > 0]
        you_owe_people = [f for f in friends if f.get('balance', 0) < 0]
        total_owed_to_you = sum(f.get('balance', 0) for f in people_owe_you)
        total_you_owe = abs(sum(f.get('balance', 0) for f in you_owe_people))
        
        top_categories = categories.get('top_categories', [])
        category_data = [
            {'label': cat.get('category', 'Other'), 'value': float(cat.get('amount', 0))}
            for cat in top_categories[:6]
        ]
        
        monthly_breakdown = spending.get('monthly_breakdown', {})
        top_groups = groups.get('top_groups', [])[:3]
        
        return {
            'currency': currency,
            'date_range': f"{format_date(earliest_raw)} - {format_date(latest_raw)}",
            'total_expenses': insights.get('data_summary', {}).get('total_expenses', 0),
            'total_spending': total_spending,
            'monthly_avg': monthly_avg,
            'net_balance': net_balance,
            'total_owed_to_you': total_owed_to_you,
            'total_you_owe': total_you_owe,
            'spending_trend': spending.get('spending_trend', 'stable'),
            'peak_month': spending.get('peak_month', 'N/A'),
            'peak_amount': float(spending.get('peak_amount', 0)) if spending.get('peak_amount') else 0,
            'category_data': category_data,
            'monthly_breakdown': monthly_breakdown,
            'top_groups': top_groups,
            'people_owe_you': sorted(people_owe_you, key=lambda x: -x.get('balance', 0))[:5],
            'you_owe_people': sorted(you_owe_people, key=lambda x: x.get('balance', 0))[:3],
            'anomaly_count': len(anomalies),
            'friend_count': len(friends),
        }
    
    def generate_pdf(self, insights, friends):
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=self.MARGIN,
            rightMargin=self.MARGIN,
            topMargin=self.MARGIN,
            bottomMargin=self.MARGIN,
        )
        
        data = self._generate_narrative(insights, friends)
        currency = data['currency']
        story = []
        
        # Header
        header_drawing = Drawing(self.CONTENT_WIDTH, 35)
        header_drawing.add(Rect(0, 0, self.CONTENT_WIDTH, 35, fillColor=Colors.PRIMARY, strokeColor=None))
        header_drawing.add(String(15, 12, "SPLITSENSE", fontName='Helvetica-Bold', fontSize=18, fillColor=colors.white))
        header_drawing.add(String(self.CONTENT_WIDTH - 100, 12, "Analytics Report", fontName='Helvetica', fontSize=10, fillColor=colors.white))
        story.append(header_drawing)
        story.append(Spacer(1, 4*mm))
        
        story.append(Paragraph(
            f"<b>{data['total_expenses']}</b> transactions analyzed - {data['date_range']}",
            self.styles['subtitle']
        ))
        
        # Stat cards
        card_width = (self.CONTENT_WIDTH - 9*mm) / 4
        cards_row = Table([[
            self._create_stat_card("Total Spending", self._format_currency(data['total_spending'], currency), Colors.PRIMARY, card_width),
            self._create_stat_card("Monthly Avg", self._format_currency(data['monthly_avg'], currency), Colors.INFO, card_width),
            self._create_stat_card("Owed to You", self._format_currency(data['total_owed_to_you'], currency), Colors.SUCCESS, card_width),
            self._create_stat_card("You Owe", self._format_currency(data['total_you_owe'], currency), Colors.DANGER, card_width),
        ]], colWidths=[card_width + 3*mm] * 4)
        cards_row.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(cards_row)
        story.append(Spacer(1, 6*mm))
        
        # Two columns
        left_col_width = self.CONTENT_WIDTH * 0.55
        right_col_width = self.CONTENT_WIDTH * 0.42
        
        left_content = []
        left_content.append(Paragraph("Monthly Spending Trend", self.styles['section_title']))
        if data['monthly_breakdown']:
            chart = self._create_bar_chart(data['monthly_breakdown'], width=left_col_width - 10, height=100)
            left_content.append(chart)
        
        trend_text = f"Spending is <b>{data['spending_trend']}</b> - Peak: {data['peak_month']} ({self._format_currency(data['peak_amount'], currency)})"
        left_content.append(Spacer(1, 3*mm))
        left_content.append(Paragraph(trend_text, self.styles['small']))
        
        right_content = []
        right_content.append(Paragraph("Spending by Category", self.styles['section_title']))
        if data['category_data']:
            pie = self._create_pie_chart(data['category_data'], width=right_col_width - 10, height=110)
            right_content.append(pie)
        
        for i, cat in enumerate(data['category_data'][:4]):
            clr = Colors.CHART_COLORS[i]
            right_content.append(Paragraph(
                f"<font color='#{clr.hexval()[2:]}'>*</font> {cat['label']}: {self._format_currency(cat['value'], currency)}",
                self.styles['small']
            ))
        
        two_col = Table([[left_content, right_content]], colWidths=[left_col_width, right_col_width])
        two_col.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(two_col)
        story.append(Spacer(1, 6*mm))
        
        # Balances
        story.append(Paragraph("Outstanding Balances", self.styles['section_title']))
        balance_data = []
        
        for person in data['people_owe_you'][:4]:
            name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
            amount = person.get('balance', 0)
            max_balance = data['total_owed_to_you'] if data['total_owed_to_you'] > 0 else 1
            progress = self._create_progress_bar(amount, max_balance, width=80, color=Colors.SUCCESS)
            balance_data.append([
                Paragraph(f"<font color='#10b981'>+</font> {name}", self.styles['body']),
                progress,
                Paragraph(f"<b>{self._format_currency(amount, currency)}</b>", self.styles['body']),
            ])
        
        for person in data['you_owe_people'][:2]:
            name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
            amount = abs(person.get('balance', 0))
            max_balance = data['total_you_owe'] if data['total_you_owe'] > 0 else 1
            progress = self._create_progress_bar(amount, max_balance, width=80, color=Colors.DANGER)
            balance_data.append([
                Paragraph(f"<font color='#ef4444'>-</font> {name}", self.styles['body']),
                progress,
                Paragraph(f"<b>-{self._format_currency(amount, currency)}</b>", self.styles['body']),
            ])
        
        if balance_data:
            balance_table = Table(balance_data, colWidths=[self.CONTENT_WIDTH * 0.45, 90, self.CONTENT_WIDTH * 0.25])
            balance_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            story.append(balance_table)
        
        story.append(Spacer(1, 6*mm))
        
        # Groups
        if data['top_groups']:
            story.append(Paragraph("Top Groups", self.styles['section_title']))
            group_data = []
            for i, group in enumerate(data['top_groups']):
                clr = Colors.CHART_COLORS[i]
                group_data.append([
                    Paragraph(f"<font color='#{clr.hexval()[2:]}'>*</font> {group.get('name', 'Unknown')}", self.styles['body']),
                    Paragraph(f"{group.get('expense_count', 0)} expenses", self.styles['small']),
                    Paragraph(f"<b>{self._format_currency(float(group.get('total_spending', 0)), currency)}</b>", self.styles['body']),
                ])
            group_table = Table(group_data, colWidths=[self.CONTENT_WIDTH * 0.45, self.CONTENT_WIDTH * 0.25, self.CONTENT_WIDTH * 0.25])
            group_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('LINEBELOW', (0, 0), (-1, -2), 0.5, Colors.BORDER),
            ]))
            story.append(group_table)
        
        # Footer
        story.append(Spacer(1, 10*mm))
        footer_drawing = Drawing(self.CONTENT_WIDTH, 25)
        footer_drawing.add(Line(0, 20, self.CONTENT_WIDTH, 20, strokeColor=Colors.BORDER, strokeWidth=0.5))
        footer_drawing.add(String(0, 5, f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}", fontName='Helvetica', fontSize=8, fillColor=Colors.TEXT_MUTED))
        footer_drawing.add(String(self.CONTENT_WIDTH - 80, 5, "splitsense.app", fontName='Helvetica-Bold', fontSize=8, fillColor=Colors.PRIMARY))
        story.append(footer_drawing)
        
        doc.build(story)
        buffer.seek(0)
        return buffer
