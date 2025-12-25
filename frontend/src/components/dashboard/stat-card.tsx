'use client';

import { motion } from 'framer-motion';
import { LucideIcon, TrendingUp, TrendingDown, Minus, Info } from 'lucide-react';
import { cn, formatCurrency, getBalanceColor } from '@/lib/utils';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: LucideIcon;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  tooltip?: string;
  variant?: 'default' | 'positive' | 'negative' | 'highlight';
  delay?: number;
}

export function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendValue,
  tooltip,
  variant = 'default',
  delay = 0,
}: StatCardProps) {
  const TrendIcon =
    trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus;

  const trendColor =
    trend === 'up'
      ? 'text-success'
      : trend === 'down'
      ? 'text-destructive'
      : 'text-muted-foreground';

  const variantStyles = {
    default: 'bg-card',
    positive: 'bg-success/5 border-success/20',
    negative: 'bg-destructive/5 border-destructive/20',
    highlight: 'bg-primary/5 border-primary/20',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: delay * 0.1 }}
      className={cn(
        'group relative rounded-xl border p-6 transition-all duration-200',
        'hover:shadow-card-hover hover:border-border/60',
        variantStyles[variant]
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          {Icon && (
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <Icon className="h-4 w-4 text-primary" />
            </div>
          )}
          <span className="text-sm font-medium text-muted-foreground">
            {title}
          </span>
        </div>
        {tooltip && (
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <button className="text-muted-foreground/60 hover:text-muted-foreground transition-colors">
                  <Info className="h-4 w-4" />
                </button>
              </TooltipTrigger>
              <TooltipContent className="max-w-xs">
                <p>{tooltip}</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        )}
      </div>

      {/* Value */}
      <div className="mt-3">
        <span
          className={cn(
            'text-3xl font-bold tracking-tight stat-number',
            variant === 'positive' && 'text-success',
            variant === 'negative' && 'text-destructive'
          )}
        >
          {value}
        </span>
      </div>

      {/* Footer */}
      <div className="mt-2 flex items-center justify-between">
        {subtitle && (
          <span className="text-sm text-muted-foreground">{subtitle}</span>
        )}
        {trend && trendValue && (
          <div className={cn('flex items-center gap-1 text-sm', trendColor)}>
            <TrendIcon className="h-3.5 w-3.5" />
            <span>{trendValue}</span>
          </div>
        )}
      </div>

      {/* Hover glow effect */}
      <div className="absolute inset-0 -z-10 rounded-xl bg-gradient-to-r from-primary/5 to-purple-500/5 opacity-0 blur-xl transition-opacity duration-500 group-hover:opacity-100" />
    </motion.div>
  );
}

interface BalanceCardProps {
  netBalance: number;
  owedToYou: number;
  youOwe: number;
  currency: string;
}

export function BalanceCard({
  netBalance,
  owedToYou,
  youOwe,
  currency,
}: BalanceCardProps) {
  const isPositive = netBalance >= 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="relative overflow-hidden rounded-xl border bg-gradient-to-br from-card to-muted/30 p-6"
    >
      {/* Background pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary/5 via-transparent to-transparent" />

      <div className="relative">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-muted-foreground">
            Net Balance
          </span>
          <span
            className={cn(
              'inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium',
              isPositive
                ? 'bg-success/10 text-success'
                : 'bg-destructive/10 text-destructive'
            )}
          >
            {isPositive ? 'You are owed' : 'You owe'}
          </span>
        </div>

        <div className="mt-2">
          <span
            className={cn(
              'text-4xl font-bold tracking-tight stat-number',
              getBalanceColor(netBalance)
            )}
          >
            {formatCurrency(Math.abs(netBalance), currency)}
          </span>
        </div>

        <div className="mt-6 grid grid-cols-2 gap-4 border-t pt-4">
          <div>
            <span className="text-xs text-muted-foreground">Owed to you</span>
            <p className="mt-1 text-lg font-semibold text-success">
              +{formatCurrency(owedToYou, currency)}
            </p>
          </div>
          <div>
            <span className="text-xs text-muted-foreground">You owe</span>
            <p className="mt-1 text-lg font-semibold text-destructive">
              -{formatCurrency(youOwe, currency)}
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
