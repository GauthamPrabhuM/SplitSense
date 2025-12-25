'use client';

import { motion } from 'framer-motion';
import { User, ArrowLeft, TrendingUp, TrendingDown, Send, MessageCircle } from 'lucide-react';
import Link from 'next/link';
import { Header } from '@/components/layout/header';
import { Footer } from '@/components/layout/footer';
import { BuyMeCoffee } from '@/components/buy-me-coffee';
import { useInsights } from '@/lib/api';
import { formatCurrency, cn, getBalanceColor, getInitials } from '@/lib/utils';
import { TableSkeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';

export default function FriendsPage() {
  const { insights, isLoading } = useInsights();
  const currency = insights?.balance?.currency_code || insights?.spending?.currency_code || 'INR';
  
  // Get friction data since by_person might be empty
  const frictionData = insights?.friction?.by_person;
  
  // Convert friction data to friends format (has more data including user balances)
  const friends = frictionData && Array.isArray(frictionData)
    ? frictionData.map((person) => ({
        user_id: person.user_id,
        name: `User ${person.user_id}`,
        balance: person.unpaid_balance,
        direction: person.unpaid_balance > 0 ? 'owed' : 'owe' as 'owed' | 'owe',
        friction_score: person.friction_score,
        average_delay_days: person.average_delay_days,
      }))
    : [];

  // Sort by absolute balance
  const sortedFriends = [...friends].sort((a, b) => Math.abs(b.balance) - Math.abs(a.balance));

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
            <h1 className="text-3xl font-bold tracking-tight">Friends & Balances</h1>
            <p className="mt-1 text-muted-foreground">
              {friends.length} people you share expenses with
            </p>
          </div>

          {isLoading ? (
            <TableSkeleton rows={8} />
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-3"
            >
              {sortedFriends.map((friend, index) => (
                <motion.div
                  key={friend.user_id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.03 }}
                  className="group flex items-center justify-between rounded-xl border bg-card p-4 transition-all hover:shadow-card-hover"
                >
                  <div className="flex items-center gap-4">
                    <div className={cn(
                      'flex h-12 w-12 items-center justify-center rounded-full text-sm font-semibold',
                      friend.balance > 0 ? 'bg-success/10 text-success' : 'bg-destructive/10 text-destructive'
                    )}>
                      {getInitials(friend.name)}
                    </div>
                    <div>
                      <h3 className="font-semibold">{friend.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        {friend.direction === 'owed' ? 'Owes you' : 'You owe'}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      {friend.balance > 0 ? (
                        <TrendingUp className="h-5 w-5 text-success" />
                      ) : (
                        <TrendingDown className="h-5 w-5 text-destructive" />
                      )}
                      <span className={cn('text-xl font-bold', getBalanceColor(friend.balance))}>
                        {formatCurrency(Math.abs(friend.balance), currency)}
                      </span>
                    </div>

                    <div className="hidden gap-2 sm:flex opacity-0 transition-opacity group-hover:opacity-100">
                      <Button variant="ghost" size="sm" className="gap-1.5">
                        <Send className="h-4 w-4" />
                        Remind
                      </Button>
                    </div>
                  </div>
                </motion.div>
              ))}

              {friends.length === 0 && (
                <div className="rounded-xl border bg-card p-12 text-center">
                  <User className="mx-auto h-12 w-12 text-muted-foreground/50" />
                  <h3 className="mt-4 text-lg font-semibold">No balances yet</h3>
                  <p className="mt-2 text-muted-foreground">
                    Import your Splitwise data to see balances with friends
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
