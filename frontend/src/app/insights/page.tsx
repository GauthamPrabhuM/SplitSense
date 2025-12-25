'use client';

import { motion } from 'framer-motion';
import {
  ArrowLeft,
  Lightbulb,
  TrendingUp,
  TrendingDown,
  Clock,
  AlertTriangle,
  Sparkles,
  Target,
  Wallet,
  Users,
} from 'lucide-react';
import Link from 'next/link';
import { Header } from '@/components/layout/header';
import { Footer } from '@/components/layout/footer';
import { BuyMeCoffee } from '@/components/buy-me-coffee';
import { useInsights } from '@/lib/api';
import { formatCurrency, cn } from '@/lib/utils';
import { CardSkeleton } from '@/components/ui/skeleton';

export default function InsightsPage() {
  const { insights, isLoading } = useInsights();
  const currency = insights?.spending?.currency_code || 'USD';

  const insightCards = insights ? [
    {
      title: 'Cash Flow Analysis',
      icon: Wallet,
      color: 'primary',
      description: insights.cash_flow?.explanation || 'No cash flow data available',
      stats: [
        { label: 'Total Paid', value: formatCurrency(insights.cash_flow?.total_paid || 0, currency), positive: true },
        { label: 'Total Share', value: formatCurrency(insights.cash_flow?.total_share || 0, currency) },
        { label: 'Net Flow', value: formatCurrency(insights.cash_flow?.net_cash_flow || 0, currency), positive: (insights.cash_flow?.net_cash_flow || 0) > 0 },
      ],
    },
    {
      title: 'Settlement Efficiency',
      icon: Clock,
      color: 'success',
      description: insights.settlement_efficiency?.explanation || 'No settlement data available',
      stats: [
        { label: 'Unpaid Balances', value: String(insights.settlement_efficiency?.unpaid_balances_count || 0) },
        { label: 'Total Unpaid', value: formatCurrency(insights.settlement_efficiency?.unpaid_balances_total || 0, currency), warning: (insights.settlement_efficiency?.unpaid_balances_total || 0) > 0 },
        { label: 'Avg Settlement', value: `${insights.settlement_efficiency?.average_settlement_days?.toFixed(0) || 0} days` },
      ],
    },
    {
      title: 'Balance Prediction',
      icon: Target,
      color: 'warning',
      description: insights.balance_prediction?.explanation || 'No prediction data available',
      stats: [
        { label: '30-Day Forecast', value: formatCurrency(insights.balance_prediction?.predicted_balance_30_days || 0, currency) },
        { label: 'Trend', value: insights.balance_prediction?.trend || 'stable' },
      ],
    },
    {
      title: 'Spending Patterns',
      icon: TrendingUp,
      color: 'destructive',
      description: insights.spending?.explanation || 'No spending data available',
      stats: [
        { label: 'Peak Month', value: insights.spending?.peak_month || 'N/A' },
        { label: 'Peak Amount', value: formatCurrency(insights.spending?.peak_amount || 0, currency) },
        { label: 'Trend', value: insights.spending?.spending_trend || 'stable' },
      ],
    },
    {
      title: 'Group Activity',
      icon: Users,
      color: 'primary',
      description: insights.groups?.explanation || 'No group data available',
      stats: [
        { label: 'Top Group', value: insights.groups?.top_groups?.[0]?.name || 'N/A' },
        { label: 'Highest Spending', value: insights.groups?.top_groups?.[0] ? formatCurrency(insights.groups.top_groups[0].total_spending, currency) : 'N/A' },
        { label: 'Total Groups', value: String(insights.groups?.top_groups?.length || 0) },
      ],
    },
    {
      title: 'Friction Analysis',
      icon: AlertTriangle,
      color: 'warning',
      description: insights.friction?.explanation || 'No friction data available',
      stats: insights.friction?.by_person?.slice(0, 3).map((p) => ({
        label: p.name,
        value: formatCurrency(p.unpaid_balance, currency),
        warning: true,
      })) || [],
    },
  ] : [];

  return (
    <div className="flex min-h-screen flex-col">
      <Header />

      <main className="flex-1">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          {/* Page Header */}
          <div className="mb-8">
            <Link
              href="/"
              className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground mb-4"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Dashboard
            </Link>
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-purple-600">
                <Lightbulb className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold tracking-tight">Insights</h1>
                <p className="mt-1 text-muted-foreground">
                  AI-powered analysis of your spending patterns
                </p>
              </div>
            </div>
          </div>

          {isLoading ? (
            <div className="grid gap-6 md:grid-cols-2">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <CardSkeleton key={i} />
              ))}
            </div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="grid gap-6 md:grid-cols-2"
            >
              {insightCards.map((card, index) => (
                <motion.div
                  key={card.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="rounded-xl border bg-card p-6"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className={cn(
                      'flex h-10 w-10 items-center justify-center rounded-lg',
                      card.color === 'primary' && 'bg-primary/10',
                      card.color === 'success' && 'bg-success/10',
                      card.color === 'warning' && 'bg-warning/10',
                      card.color === 'destructive' && 'bg-destructive/10',
                    )}>
                      <card.icon className={cn(
                        'h-5 w-5',
                        card.color === 'primary' && 'text-primary',
                        card.color === 'success' && 'text-success',
                        card.color === 'warning' && 'text-warning',
                        card.color === 'destructive' && 'text-destructive',
                      )} />
                    </div>
                    <h3 className="font-semibold">{card.title}</h3>
                  </div>

                  <p className="text-sm text-muted-foreground mb-4">
                    {card.description}
                  </p>

                  <div className="space-y-2">
                    {card.stats.map((stat, i) => (
                      <div key={i} className="flex items-center justify-between py-2 border-t first:border-t-0">
                        <span className="text-sm text-muted-foreground">{stat.label}</span>
                        <span className={cn(
                          'text-sm font-medium',
                          'positive' in stat && stat.positive && 'text-success',
                          'warning' in stat && stat.warning && 'text-warning',
                        )}>
                          {stat.value}
                        </span>
                      </div>
                    ))}
                  </div>
                </motion.div>
              ))}

              {/* Anomalies Section */}
              {insights?.anomalies?.anomalies && insights.anomalies.anomalies.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                  className="md:col-span-2 rounded-xl border border-destructive/30 bg-destructive/5 p-6"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-destructive/10">
                      <AlertTriangle className="h-5 w-5 text-destructive" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Spending Anomalies Detected</h3>
                      <p className="text-sm text-muted-foreground">
                        {insights.anomalies.anomalies.length} unusual expenses found
                      </p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {insights.anomalies.anomalies.slice(0, 5).map((anomaly, i) => (
                      <div key={i} className="flex items-center justify-between rounded-lg bg-card p-3">
                        <div>
                          <p className="font-medium">{anomaly.description}</p>
                          <p className="text-sm text-muted-foreground">{anomaly.reason}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold text-destructive">
                            {formatCurrency(anomaly.amount, currency)}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {new Date(anomaly.date).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}
        </div>
      </main>

      <Footer />
      <BuyMeCoffee variant="floating" />
    </div>
  );
}
