'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Wallet,
  TrendingUp,
  Users,
  CreditCard,
  RefreshCw,
  Calendar,
  PieChart,
  AlertTriangle,
  FileText,
  Download,
} from 'lucide-react';
import { Header } from '../components/layout/header';
import { Footer } from '../components/layout/footer';
import { BuyMeCoffee } from '../components/buy-me-coffee';
import { StatCard, BalanceCard } from '../components/dashboard/stat-card';
import { SpendingChart, BalanceChart, CategoryChart, GroupChart } from '../components/dashboard/charts';
import { GroupList, FriendList, FrictionList } from '../components/dashboard/lists';
import { DataIngestion } from '../components/dashboard/data-ingestion';
import { CardSkeleton, ChartSkeleton, TableSkeleton } from '../components/ui/skeleton';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { useInsights, useFriends } from '../lib/api';
import { formatCurrency, formatDate } from '../lib/utils';

export default function DashboardPage() {
  const { insights, isLoading, isError, refresh } = useInsights();
  const { friends: friendBalances } = useFriends();
  const [showIngestion, setShowIngestion] = useState(false);

  // Show ingestion if no data
  useEffect(() => {
    if (!isLoading && !insights && !isError) {
      setShowIngestion(true);
    }
    
    // Check if coming from OAuth callback
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('oauth') === 'success') {
      // OAuth was successful, refresh data
      setTimeout(() => {
        refresh();
        // Clean up URL
        window.history.replaceState({}, '', window.location.pathname);
      }, 1000);
    }
  }, [isLoading, insights, isError, refresh]);

  const handleIngestionSuccess = () => {
    setShowIngestion(false);
    refresh();
  };

  // Use INR as default since the data is primarily in INR
  const currency = insights?.spending?.currency_code || 'INR';

  return (
    <div className="flex min-h-screen flex-col">
      <Header />

      <main className="flex-1">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          {/* Ingestion Screen */}
          {showIngestion ? (
            <div className="py-16">
              <DataIngestion onSuccess={handleIngestionSuccess} />
            </div>
          ) : isLoading ? (
            <DashboardSkeleton />
          ) : isError ? (
            <ErrorState onRetry={() => setShowIngestion(true)} />
          ) : insights ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="space-y-8"
            >
              {/* Page Header */}
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                  <p className="mt-1 text-muted-foreground">
                    {insights.data_summary?.total_expenses} expenses tracked •{' '}
                    {insights.data_summary?.date_range?.earliest && (
                      <>
                        {formatDate(insights.data_summary.date_range.earliest)} -{' '}
                        {formatDate(insights.data_summary.date_range.latest)}
                      </>
                    )}
                  </p>
                </div>
                <div className="flex gap-2">
                  <Button 
                    variant="outline" 
                    onClick={() => {
                      // Trigger PDF download - use relative URL so it works in any environment
                      const link = document.createElement('a');
                      link.href = '/api/report';
                      link.download = 'splitsense_report.pdf';
                      document.body.appendChild(link);
                      link.click();
                      document.body.removeChild(link);
                    }} 
                    className="gap-2"
                  >
                    <FileText className="h-4 w-4" />
                    Download Report
                  </Button>
                  <Button variant="outline" onClick={() => refresh()} className="gap-2">
                    <RefreshCw className="h-4 w-4" />
                    Refresh
                  </Button>
                </div>
              </div>

              {/* Summary Stats */}
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <BalanceCard
                  netBalance={insights.balance?.net_balance || 0}
                  owedToYou={insights.balance?.owed_to_user || insights.balance?.total_owed_to_you || 0}
                  youOwe={insights.balance?.user_owes || insights.balance?.total_you_owe || 0}
                  currency={currency}
                />
                <StatCard
                  title="Total Spending"
                  value={formatCurrency(insights.spending?.total_spending || 0, currency)}
                  subtitle="All time"
                  icon={CreditCard}
                  trend={insights.spending?.spending_trend === 'increasing' ? 'up' : insights.spending?.spending_trend === 'decreasing' ? 'down' : 'neutral'}
                  tooltip="Your total spending across all groups and categories"
                  delay={1}
                />
                <StatCard
                  title="Monthly Average"
                  value={formatCurrency(insights.spending?.monthly_average || 0, currency)}
                  subtitle="Per month"
                  icon={Calendar}
                  tooltip="Average monthly spending over the tracked period"
                  delay={2}
                />
                <StatCard
                  title="Monthly Subscriptions"
                  value={formatCurrency(insights.subscriptions?.total_monthly_subscriptions || 0, currency)}
                  subtitle={`${insights.subscriptions?.subscriptions?.length || 0} recurring`}
                  icon={RefreshCw}
                  variant="highlight"
                  tooltip="Detected recurring expenses and subscriptions"
                  delay={3}
                />
              </div>

              {/* Tabs for different views */}
              <Tabs defaultValue="overview" className="space-y-6">
                <TabsList>
                  <TabsTrigger value="overview" className="gap-2">
                    <PieChart className="h-4 w-4" />
                    Overview
                  </TabsTrigger>
                  <TabsTrigger value="groups" className="gap-2">
                    <Users className="h-4 w-4" />
                    Groups
                  </TabsTrigger>
                  <TabsTrigger value="insights" className="gap-2">
                    <TrendingUp className="h-4 w-4" />
                    Insights
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="overview" className="space-y-6">
                  {/* Charts Grid */}
                  <div className="grid gap-6 lg:grid-cols-2">
                    {insights.spending && <SpendingChart data={insights.spending} />}
                    {insights.balance && <BalanceChart data={insights.balance} />}
                    {insights.categories?.top_categories && (
                      <CategoryChart
                        categories={insights.categories.top_categories}
                        currency={currency}
                      />
                    )}
                    {insights.groups?.top_groups && (
                      <GroupChart groups={insights.groups.top_groups} currency={currency} />
                    )}
                  </div>
                </TabsContent>

                <TabsContent value="groups" className="space-y-6">
                  <div className="grid gap-6 lg:grid-cols-2">
                    {insights.groups?.top_groups && (
                      <GroupList groups={insights.groups.top_groups} currency={currency} />
                    )}
                    {/* Show friend balances - prefer real Splitwise data */}
                    {(friendBalances && friendBalances.length > 0) || (insights.balance?.by_person && Object.keys(insights.balance.by_person).length > 0) ? (
                      <FriendList 
                        friends={insights.balance?.by_person || {}} 
                        currency={currency} 
                        friendBalances={friendBalances}
                      />
                    ) : null}
                    {/* Show friction list with real balances from Splitwise API */}
                    {(friendBalances && friendBalances.length > 0) || (insights.friction?.by_person && insights.friction.by_person.length > 0) ? (
                      <FrictionList 
                        friction={insights.friction?.by_person || []} 
                        currency={currency} 
                        friendBalances={friendBalances}
                      />
                    ) : null}
                  </div>
                </TabsContent>

                <TabsContent value="insights" className="space-y-6">
                  <div className="grid gap-6 lg:grid-cols-2">
                    {/* Cash Flow Card */}
                    <InsightCard
                      title="Cash Flow Analysis"
                      icon={Wallet}
                      description={insights.cash_flow?.explanation || ''}
                    >
                      <div className="mt-4 grid grid-cols-2 gap-4">
                        <div className="rounded-lg bg-success/10 p-4">
                          <span className="text-sm text-muted-foreground">Total Paid</span>
                          <p className="mt-1 text-xl font-semibold text-success">
                            {formatCurrency(insights.cash_flow?.total_paid || 0, currency)}
                          </p>
                        </div>
                        <div className="rounded-lg bg-destructive/10 p-4">
                          <span className="text-sm text-muted-foreground">Total Owed</span>
                          <p className="mt-1 text-xl font-semibold text-destructive">
                            {formatCurrency(insights.cash_flow?.total_received || 0, currency)}
                          </p>
                        </div>
                      </div>
                    </InsightCard>

                    {/* Settlement Efficiency */}
                    <InsightCard
                      title="Settlement Efficiency"
                      icon={TrendingUp}
                      description={insights.settlement_efficiency?.explanation || ''}
                    >
                      <div className="mt-4 space-y-3">
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Unpaid Balances</span>
                          <span className="font-semibold">{insights.settlement_efficiency?.unpaid_balances_count}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Total Unpaid</span>
                          <span className="font-semibold">
                            {formatCurrency(insights.settlement_efficiency?.unpaid_balances_total || 0, currency)}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Avg Settlement Time</span>
                          <span className="font-semibold">
                            {insights.settlement_efficiency?.average_settlement_days?.toFixed(0) || 0} days
                          </span>
                        </div>
                      </div>
                    </InsightCard>

                    {/* Friction Warning */}
                    {((friendBalances && friendBalances.length > 0) || insights.friction?.by_person) && (
                      <div className="lg:col-span-2">
                        <FrictionList 
                          friction={insights.friction?.by_person || []} 
                          currency={currency}
                          friendBalances={friendBalances}
                        />
                      </div>
                    )}
                  </div>
                </TabsContent>
              </Tabs>
            </motion.div>
          ) : null}
        </div>
      </main>

      <Footer />
      <BuyMeCoffee variant="floating" />
    </div>
  );
}

function InsightCard({
  title,
  icon: Icon,
  description,
  children,
}: {
  title: string;
  icon: React.ElementType;
  description: string;
  children?: React.ReactNode;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border bg-card p-6"
    >
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
          <Icon className="h-5 w-5 text-primary" />
        </div>
        <h3 className="font-semibold">{title}</h3>
      </div>
      <p className="mt-3 text-sm text-muted-foreground">{description}</p>
      {children}
    </motion.div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="space-y-8">
      <div className="flex justify-between">
        <div className="space-y-2">
          <div className="skeleton h-8 w-48 rounded" />
          <div className="skeleton h-4 w-64 rounded" />
        </div>
        <div className="skeleton h-10 w-24 rounded" />
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <CardSkeleton key={i} />
        ))}
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <ChartSkeleton />
        <ChartSkeleton />
      </div>
    </div>
  );
}

function ErrorState({ onRetry }: { onRetry: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-destructive/10">
        <AlertTriangle className="h-8 w-8 text-destructive" />
      </div>
      <h2 className="mt-6 text-xl font-semibold">Unable to load data</h2>
      <p className="mt-2 text-muted-foreground">
        There was a problem loading your dashboard data.
      </p>
      <Button onClick={onRetry} className="mt-6">
        Try Again
      </Button>
    </div>
  );
}
