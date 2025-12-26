'use client';

import { motion } from 'framer-motion';
import { Users, ArrowLeft, TrendingUp, TrendingDown } from 'lucide-react';
import Link from 'next/link';
import { Header } from '../../components/layout/header';
import { Footer } from '../../components/layout/footer';
import { BuyMeCoffee } from '../../components/buy-me-coffee';
import { useInsights } from '../../lib/api';
import { formatCurrency, cn, getBalanceColor } from '../../lib/utils';
import { TableSkeleton } from '../../components/ui/skeleton';
import { Button } from '../../components/ui/button';
import { Progress } from '../../components/ui/progress';

export default function GroupsPage() {
  const { insights, isLoading } = useInsights();
  const currency = insights?.groups?.currency_code || insights?.spending?.currency_code || 'INR';
  const groups = Array.isArray(insights?.groups?.top_groups) ? insights.groups.top_groups : [];

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
            <h1 className="text-3xl font-bold tracking-tight">Groups</h1>
            <p className="mt-1 text-muted-foreground">
              {groups.length} groups with shared expenses
            </p>
          </div>

          {isLoading ? (
            <TableSkeleton rows={8} />
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-4"
            >
              {groups.map((group, index) => (
                <motion.div
                  key={group.group_id ?? `group-${index}`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="rounded-xl border bg-card p-6 transition-shadow hover:shadow-card-hover"
                >
                  <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
                    <div className="flex items-center gap-4">
                      <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-purple-600">
                        <Users className="h-7 w-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold">{group.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {group.member_count} members • {group.expense_count} expenses
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-6 sm:flex sm:items-center sm:gap-8">
                      <div className="text-center">
                        <p className="text-sm text-muted-foreground">Total Spending</p>
                        <p className="text-lg font-semibold">
                          {formatCurrency(group.total_spending, currency)}
                        </p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-muted-foreground">Per Member</p>
                        <p className="text-lg font-semibold text-primary">
                          {formatCurrency(group.total_spending / (group.member_count || 1), currency)}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Member count indicator */}
                  <div className="mt-6">
                    <div className="flex items-center justify-between text-sm mb-2">
                      <span className="text-muted-foreground">Expenses tracked</span>
                      <span className="font-medium">
                        {group.expense_count} expenses
                      </span>
                    </div>
                    <Progress
                      value={Math.min((group.expense_count / 100) * 100, 100)}
                    />
                  </div>
                </motion.div>
              ))}

              {groups.length === 0 && (
                <div className="rounded-xl border bg-card p-12 text-center">
                  <Users className="mx-auto h-12 w-12 text-muted-foreground/50" />
                  <h3 className="mt-4 text-lg font-semibold">No groups yet</h3>
                  <p className="mt-2 text-muted-foreground">
                    Import your Splitwise data to see your groups
                  </p>
                  <Button asChild className="mt-6">
                    <Link href="/">Go to Dashboard</Link>
                  </Button>
                </div>
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
