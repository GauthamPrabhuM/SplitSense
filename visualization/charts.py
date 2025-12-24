"""
Chart generation using Plotly.
"""
from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from models.schemas import AllInsights


class ChartGenerator:
    """Generate interactive charts from insights"""
    
    @staticmethod
    def spending_trend_chart(insights: AllInsights) -> str:
        """Generate spending trend chart (HTML)"""
        spending = insights.spending
        
        fig = go.Figure()
        
        # Monthly breakdown
        months = list(spending.monthly_breakdown.keys())
        amounts = [float(v) for v in spending.monthly_breakdown.values()]
        
        fig.add_trace(go.Scatter(
            x=months,
            y=amounts,
            mode='lines+markers',
            name='Monthly Spending',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Spending Trend Over Time',
            xaxis_title='Month',
            yaxis_title=f'Amount ({spending.currency_code})',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='spending-trend')
    
    @staticmethod
    def balance_trend_chart(insights: AllInsights) -> str:
        """Generate balance trend chart (HTML)"""
        balance = insights.balance
        
        fig = go.Figure()
        
        months = list(balance.trend_over_time.keys())
        amounts = [float(v) for v in balance.trend_over_time.values()]
        
        # Color based on positive/negative
        colors = ['green' if a >= 0 else 'red' for a in amounts]
        
        fig.add_trace(go.Scatter(
            x=months,
            y=amounts,
            mode='lines+markers',
            name='Net Balance',
            line=dict(color='#2ca02c', width=2),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(44, 160, 44, 0.2)'
        ))
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.update_layout(
            title='Net Balance Trend',
            xaxis_title='Month',
            yaxis_title=f'Net Balance ({balance.currency_code})',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='balance-trend')
    
    @staticmethod
    def category_pie_chart(insights: AllInsights) -> str:
        """Generate category breakdown pie chart (HTML)"""
        categories = insights.categories
        
        top_cats = categories.top_categories[:10]
        labels = [cat['category'] for cat in top_cats]
        values = [cat['amount'] for cat in top_cats]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title='Spending by Category (Top 10)',
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='category-pie')
    
    @staticmethod
    def group_bar_chart(insights: AllInsights) -> str:
        """Generate group spending bar chart (HTML)"""
        groups = insights.groups
        
        top_groups = groups.top_groups[:10]
        group_names = [g['name'] for g in top_groups]
        amounts = [g['total_spending'] for g in top_groups]
        
        fig = go.Figure(data=[go.Bar(
            x=group_names,
            y=amounts,
            marker_color='#ff7f0e',
            text=[f"{a:,.0f}" for a in amounts],
            textposition='outside'
        )])
        
        fig.update_layout(
            title='Spending by Group (Top 10)',
            xaxis_title='Group',
            yaxis_title=f'Total Spending ({groups.currency_code})',
            xaxis_tickangle=-45,
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='group-bar')
    
    @staticmethod
    def anomaly_chart(insights: AllInsights) -> str:
        """Generate anomaly detection chart (HTML)"""
        anomalies = insights.anomalies
        
        if not anomalies.anomalies:
            return "<p>No anomalies detected.</p>"
        
        dates = [a['date'] for a in anomalies.anomalies]
        amounts = [a['amount'] for a in anomalies.anomalies]
        descriptions = [a['description'] for a in anomalies.anomalies]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=amounts,
            mode='markers',
            name='Anomalies',
            marker=dict(
                size=12,
                color='red',
                symbol='diamond'
            ),
            text=descriptions,
            hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Amount: %{y:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Spending Anomalies',
            xaxis_title='Date',
            yaxis_title='Amount',
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='anomaly-chart')
    
    @staticmethod
    def subscription_chart(insights: AllInsights) -> str:
        """Generate subscription breakdown chart (HTML)"""
        subscriptions = insights.subscriptions
        
        if not subscriptions.subscriptions:
            return "<p>No recurring subscriptions detected.</p>"
        
        top_subs = subscriptions.subscriptions[:10]
        labels = [sub.description_pattern for sub in top_subs]
        amounts = [float(sub.average_amount) for sub in top_subs]
        
        fig = go.Figure(data=[go.Bar(
            x=labels,
            y=amounts,
            marker_color='#9467bd',
            text=[f"{a:,.2f}" for a in amounts],
            textposition='outside'
        )])
        
        fig.update_layout(
            title='Recurring Expenses / Subscriptions',
            xaxis_title='Description',
            yaxis_title=f'Average Amount ({subscriptions.currency_code})',
            xaxis_tickangle=-45,
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='subscription-chart')
    
    @staticmethod
    def generate_all_charts(insights: AllInsights) -> Dict[str, str]:
        """Generate all charts and return as HTML strings"""
        return {
            "spending_trend": ChartGenerator.spending_trend_chart(insights),
            "balance_trend": ChartGenerator.balance_trend_chart(insights),
            "category_pie": ChartGenerator.category_pie_chart(insights),
            "group_bar": ChartGenerator.group_bar_chart(insights),
            "anomaly": ChartGenerator.anomaly_chart(insights),
            "subscription": ChartGenerator.subscription_chart(insights),
        }

