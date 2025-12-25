'use client';

import { useMemo } from 'react';
import { motion } from 'framer-motion';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  Legend,
} from 'recharts';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { cn, formatCurrency, formatCompactNumber } from '@/lib/utils';
import type { SpendingInsight, BalanceInsight, CategoryBreakdown, GroupBreakdown, TopGroup } from '@/types/api';

const CHART_COLORS = [
  'hsl(238, 84%, 67%)',   // Primary
  'hsl(280, 65%, 60%)',   // Purple
  'hsl(142, 76%, 36%)',   // Green
  'hsl(38, 92%, 50%)',    // Amber
  'hsl(0, 84%, 60%)',     // Red
  'hsl(200, 80%, 50%)',   // Blue
  'hsl(320, 70%, 50%)',   // Pink
  'hsl(160, 60%, 45%)',   // Teal
];

interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  annotation?: string;
}

function ChartCard({ title, subtitle, children, annotation }: ChartCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="rounded-xl border bg-card p-6"
    >
      <div className="mb-4 flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold">{title}</h3>
          {subtitle && (
            <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
          )}
        </div>
      </div>
      <div className="h-[300px]">{children}</div>
      {annotation && (
        <div className="mt-4 rounded-lg bg-muted/50 px-4 py-3">
          <p className="text-sm text-muted-foreground">{annotation}</p>
        </div>
      )}
    </motion.div>
  );
}

interface SpendingChartProps {
  data: SpendingInsight;
}

export function SpendingChart({ data }: SpendingChartProps) {
  const chartData = useMemo(() => {
    return Object.entries(data.monthly_breakdown || {}).map(([month, amount]) => ({
      month: new Date(month + '-01').toLocaleDateString('en-US', { month: 'short', year: '2-digit' }),
      amount: Number(amount),
    }));
  }, [data.monthly_breakdown]);

  const trend = data.spending_trend;
  const TrendIcon = trend === 'increasing' ? TrendingUp : trend === 'decreasing' ? TrendingDown : null;

  return (
    <ChartCard
      title="Spending Over Time"
      subtitle={`Monthly average: ${formatCurrency(data.monthly_average, data.currency_code)}`}
      annotation={data.explanation}
    >
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="spendingGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(238, 84%, 67%)" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(238, 84%, 67%)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" className="stroke-border" vertical={false} />
          <XAxis
            dataKey="month"
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
            dy={10}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
            tickFormatter={(value) => formatCompactNumber(value)}
            dx={-10}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                return (
                  <div className="rounded-lg border bg-popover px-3 py-2 shadow-md">
                    <p className="text-sm font-medium">
                      {formatCurrency(payload[0].value as number, data.currency_code)}
                    </p>
                    <p className="text-xs text-muted-foreground">{payload[0].payload.month}</p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Area
            type="monotone"
            dataKey="amount"
            stroke="hsl(238, 84%, 67%)"
            strokeWidth={2}
            fill="url(#spendingGradient)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

interface BalanceChartProps {
  data: BalanceInsight;
}

export function BalanceChart({ data }: BalanceChartProps) {
  const chartData = useMemo(() => {
    return Object.entries(data.trend_over_time || {}).map(([month, balance]) => ({
      month: new Date(month + '-01').toLocaleDateString('en-US', { month: 'short', year: '2-digit' }),
      balance: Number(balance),
    }));
  }, [data.trend_over_time]);

  return (
    <ChartCard
      title="Balance Trend"
      subtitle={`Current: ${formatCurrency(data.net_balance, data.currency_code)}`}
      annotation={data.explanation}
    >
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="positiveGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(142, 76%, 36%)" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(142, 76%, 36%)" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="negativeGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(0, 84%, 60%)" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(0, 84%, 60%)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" className="stroke-border" vertical={false} />
          <XAxis
            dataKey="month"
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
            dy={10}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
            tickFormatter={(value) => formatCompactNumber(value)}
            dx={-10}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const value = payload[0].value as number;
                return (
                  <div className="rounded-lg border bg-popover px-3 py-2 shadow-md">
                    <p className={cn('text-sm font-medium', value >= 0 ? 'text-success' : 'text-destructive')}>
                      {formatCurrency(value, data.currency_code)}
                    </p>
                    <p className="text-xs text-muted-foreground">{payload[0].payload.month}</p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Area
            type="monotone"
            dataKey="balance"
            stroke={data.net_balance >= 0 ? 'hsl(142, 76%, 36%)' : 'hsl(0, 84%, 60%)'}
            strokeWidth={2}
            fill={data.net_balance >= 0 ? 'url(#positiveGradient)' : 'url(#negativeGradient)'}
          />
        </AreaChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

interface CategoryChartProps {
  categories: CategoryBreakdown[];
  currency: string;
}

export function CategoryChart({ categories, currency }: CategoryChartProps) {
  const chartData = useMemo(() => {
    return categories.slice(0, 8).map((cat, index) => ({
      name: cat.category,
      value: cat.amount,
      percentage: cat.percentage,
      fill: CHART_COLORS[index % CHART_COLORS.length],
    }));
  }, [categories]);

  return (
    <ChartCard
      title="Spending by Category"
      subtitle={`${categories.length} categories tracked`}
    >
      <div className="flex h-full">
        <div className="w-1/2">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={2}
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const item = payload[0].payload;
                    return (
                      <div className="rounded-lg border bg-popover px-3 py-2 shadow-md">
                        <p className="text-sm font-medium">{item.name}</p>
                        <p className="text-sm text-muted-foreground">
                          {formatCurrency(item.value, currency)} ({item.percentage.toFixed(1)}%)
                        </p>
                      </div>
                    );
                  }
                  return null;
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="w-1/2 space-y-2 overflow-y-auto pl-4">
          {chartData.map((item, index) => (
            <div key={item.name} className="flex items-center gap-2">
              <div
                className="h-3 w-3 rounded-full"
                style={{ backgroundColor: item.fill }}
              />
              <span className="flex-1 truncate text-sm">{item.name}</span>
              <span className="text-sm font-medium text-muted-foreground">
                {item.percentage.toFixed(0)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </ChartCard>
  );
}

interface GroupChartProps {
  groups: GroupBreakdown[] | TopGroup[];
  currency: string;
}

export function GroupChart({ groups, currency }: GroupChartProps) {
  const chartData = useMemo(() => {
    return groups.slice(0, 8).map((group) => ({
      name: group.name.length > 15 ? group.name.slice(0, 15) + '...' : group.name,
      fullName: group.name,
      spending: group.total_spending,
      share: 'your_share' in group ? group.your_share : 0,
    }));
  }, [groups]);

  return (
    <ChartCard
      title="Group Spending"
      subtitle={`${groups.length} groups`}
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} layout="vertical" margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-border" horizontal={false} />
          <XAxis
            type="number"
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
            tickFormatter={(value) => formatCompactNumber(value)}
          />
          <YAxis
            type="category"
            dataKey="name"
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
            width={100}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const item = payload[0].payload;
                return (
                  <div className="rounded-lg border bg-popover px-3 py-2 shadow-md">
                    <p className="text-sm font-medium">{item.fullName}</p>
                    <p className="text-sm text-muted-foreground">
                      Total: {formatCurrency(item.spending, currency)}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Your share: {formatCurrency(item.share, currency)}
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Bar dataKey="spending" fill="hsl(238, 84%, 67%)" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}
