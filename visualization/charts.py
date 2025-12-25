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
        
        # Check if we have data
        if not spending.monthly_breakdown:
            return "<div class='empty-state'><p>No spending data available</p></div>"
        
        fig = go.Figure()
        
        # Monthly breakdown
        months = list(spending.monthly_breakdown.keys())
        amounts = [float(v) for v in spending.monthly_breakdown.values()]
        
        if not months or not amounts:
            return "<div class='empty-state'><p>No spending data available</p></div>"
        
        fig.add_trace(go.Scatter(
            x=months,
            y=amounts,
            mode='lines+markers',
            name='Monthly Spending',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#764ba2'),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        fig.update_layout(
            title=dict(text='Spending Trend Over Time', font=dict(size=18)),
            xaxis_title='Month',
            yaxis_title=f'Amount ({spending.currency_code})',
            hovermode='x unified',
            template='plotly_white',
            height=450,
            showlegend=False
        )
        
        return fig.to_html(include_plotlyjs=False, full_html=False, div_id='spending-trend', config={'displayModeBar': True})
    
    @staticmethod
    def balance_trend_chart(insights: AllInsights) -> str:
        """Generate balance trend chart (HTML)"""
        balance = insights.balance
        
        if not balance.trend_over_time:
            return "<div class='empty-state'><p>No balance data available</p></div>"
        
        fig = go.Figure()
        
        months = list(balance.trend_over_time.keys())
        amounts = [float(v) for v in balance.trend_over_time.values()]
        
        if not months or not amounts:
            return "<div class='empty-state'><p>No balance data available</p></div>"
        
        # Use different colors for positive/negative
        colors = ['#28a745' if a >= 0 else '#dc3545' for a in amounts]
        
        fig.add_trace(go.Scatter(
            x=months,
            y=amounts,
            mode='lines+markers',
            name='Net Balance',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color=colors),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.update_layout(
            title=dict(text='Net Balance Trend', font=dict(size=18)),
            xaxis_title='Month',
            yaxis_title=f'Net Balance ({balance.currency_code})',
            hovermode='x unified',
            template='plotly_white',
            height=450,
            showlegend=False
        )
        
        return fig.to_html(include_plotlyjs=False, full_html=False, div_id='balance-trend', config={'displayModeBar': True})
    
    @staticmethod
    def category_pie_chart(insights: AllInsights) -> str:
        """Generate category breakdown pie chart (HTML)"""
        categories = insights.categories
        
        if not categories.top_categories:
            return "<div class='empty-state'><p>No category data available</p></div>"
        
        top_cats = categories.top_categories[:10]
        labels = [cat['category'] for cat in top_cats]
        values = [cat['amount'] for cat in top_cats]
        
        if not labels or not values:
            return "<div class='empty-state'><p>No category data available</p></div>"
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3'])
        )])
        
        fig.update_layout(
            title=dict(text='Spending by Category (Top 10)', font=dict(size=18)),
            template='plotly_white',
            height=450
        )
        
        return fig.to_html(include_plotlyjs=False, full_html=False, div_id='category-pie', config={'displayModeBar': True})
    
    @staticmethod
    def group_bar_chart(insights: AllInsights) -> str:
        """Generate group spending bar chart (HTML)"""
        groups = insights.groups
        
        if not groups.top_groups:
            return "<div class='empty-state'><p>No group data available</p></div>"
        
        top_groups = groups.top_groups[:10]
        group_names = [g['name'] for g in top_groups]
        amounts = [g['total_spending'] for g in top_groups]
        
        if not group_names or not amounts:
            return "<div class='empty-state'><p>No group data available</p></div>"
        
        fig = go.Figure(data=[go.Bar(
            x=group_names,
            y=amounts,
            marker_color='#667eea',
            text=[f"{a:,.0f}" for a in amounts],
            textposition='outside',
            marker=dict(line=dict(color='#764ba2', width=1))
        )])
        
        fig.update_layout(
            title=dict(text='Spending by Group (Top 10)', font=dict(size=18)),
            xaxis_title='Group',
            yaxis_title=f'Total Spending ({groups.currency_code})',
            xaxis_tickangle=-45,
            template='plotly_white',
            height=450
        )
        
        return fig.to_html(include_plotlyjs=False, full_html=False, div_id='group-bar', config={'displayModeBar': True})
    
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
            template='plotly_white',
            height=450
        )
        
        return fig.to_html(include_plotlyjs=False, full_html=False, div_id='anomaly-chart', config={'displayModeBar': True})
    
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
            template='plotly_white',
            height=450
        )
        
        return fig.to_html(include_plotlyjs=False, full_html=False, div_id='subscription-chart', config={'displayModeBar': True})
    
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

