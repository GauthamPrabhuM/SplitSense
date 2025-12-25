'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Users, User, TrendingUp, TrendingDown, AlertCircle } from 'lucide-react';
import { cn, formatCurrency, getBalanceColor, getInitials } from '@/lib/utils';
import type { GroupBreakdown, PersonBalance, FrictionPerson, TopGroup } from '@/types/api';

interface GroupListProps {
  groups: TopGroup[] | GroupBreakdown[];
  currency: string;
}

export function GroupList({ groups, currency }: GroupListProps) {
  const [expandedId, setExpandedId] = useState<number | string | null>(null);

  // Normalize groups to have consistent id field
  const normalizedGroups = groups.map((group, index) => {
    if ('group_id' in group) {
      return {
        id: group.group_id ?? `non-group-${index}`,
        name: group.name,
        total_spending: group.total_spending,
        expense_count: group.expense_count,
        member_count: group.member_count,
        your_share: 0, // Not available in TopGroup
      };
    }
    return group as GroupBreakdown;
  });

  return (
    <div className="rounded-xl border bg-card">
      <div className="flex items-center justify-between border-b p-4">
        <h3 className="font-semibold">Groups</h3>
        <span className="text-sm text-muted-foreground">{normalizedGroups.length} groups</span>
      </div>
      <div className="divide-y">
        {normalizedGroups.map((group) => (
          <div key={group.id}>
            <button
              onClick={() => setExpandedId(expandedId === group.id ? null : group.id)}
              className="flex w-full items-center justify-between p-4 text-left transition-colors hover:bg-muted/50"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <Users className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="font-medium">{group.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {group.member_count} members • {group.expense_count} expenses
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className="font-semibold">
                    {formatCurrency(group.total_spending, currency)}
                  </p>
                  {group.your_share > 0 && (
                    <p className="text-sm text-muted-foreground">
                      Your share: {formatCurrency(group.your_share, currency)}
                    </p>
                  )}
                </div>
                <ChevronDown
                  className={cn(
                    'h-5 w-5 text-muted-foreground transition-transform',
                    expandedId === group.id && 'rotate-180'
                  )}
                />
              </div>
            </button>
            <AnimatePresence>
              {expandedId === group.id && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="overflow-hidden border-t bg-muted/30"
                >
                  <div className="p-4 space-y-3">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="rounded-lg bg-card p-3">
                        <span className="text-muted-foreground">Total Spending</span>
                        <p className="mt-1 text-lg font-semibold">
                          {formatCurrency(group.total_spending, currency)}
                        </p>
                      </div>
                      <div className="rounded-lg bg-card p-3">
                        <span className="text-muted-foreground">Your Share</span>
                        <p className="mt-1 text-lg font-semibold">
                          {formatCurrency(group.your_share, currency)}
                        </p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      This group has {group.expense_count} expenses tracked across {group.member_count} members.
                    </p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </div>
  );
}

interface FriendListProps {
  friends: Record<string, number> | PersonBalance[];
  currency: string;
}

export function FriendList({ friends, currency }: FriendListProps) {
  // Convert dictionary format to array if needed
  const friendsArray: PersonBalance[] = Array.isArray(friends)
    ? friends
    : friends && typeof friends === 'object'
      ? Object.entries(friends).map(([userId, balance]) => ({
          user_id: parseInt(userId),
          name: `User ${userId}`,
          balance: Number(balance),
          direction: (Number(balance) > 0 ? 'owed' : 'owe') as 'owed' | 'owe',
        }))
      : [];

  return (
    <div className="rounded-xl border bg-card">
      <div className="flex items-center justify-between border-b p-4">
        <h3 className="font-semibold">Balance by Person</h3>
        <span className="text-sm text-muted-foreground">{friendsArray.length} people</span>
      </div>
      <div className="divide-y">
        {friendsArray.map((friend) => (
          <div
            key={friend.user_id}
            className="flex items-center justify-between p-4"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted text-sm font-medium">
                {getInitials(friend.name)}
              </div>
              <div>
                <p className="font-medium">{friend.name}</p>
                <p className="text-sm text-muted-foreground">
                  {friend.direction === 'owed' ? 'Owes you' : 'You owe'}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {friend.direction === 'owed' ? (
                <TrendingUp className="h-4 w-4 text-success" />
              ) : (
                <TrendingDown className="h-4 w-4 text-destructive" />
              )}
              <span className={cn('font-semibold', getBalanceColor(friend.balance))}>
                {formatCurrency(Math.abs(friend.balance), currency)}
              </span>
            </div>
          </div>
        ))}
        {friendsArray.length === 0 && (
          <div className="p-8 text-center text-muted-foreground">
            <User className="mx-auto h-8 w-8 opacity-50" />
            <p className="mt-2">No balances with friends</p>
          </div>
        )}
      </div>
    </div>
  );
}

interface FrictionListProps {
  friction: FrictionPerson[];
  currency: string;
}

export function FrictionList({ friction, currency }: FrictionListProps) {
  if (friction.length === 0) return null;

  return (
    <div className="rounded-xl border border-warning/30 bg-warning/5">
      <div className="flex items-center gap-2 border-b border-warning/30 p-4">
        <AlertCircle className="h-5 w-5 text-warning" />
        <h3 className="font-semibold">Settlement Friction</h3>
      </div>
      <div className="p-4 space-y-4">
        <p className="text-sm text-muted-foreground">
          These people have unpaid balances and may need a reminder.
        </p>
        <div className="space-y-3">
          {friction.slice(0, 5).map((person, index) => (
            <div
              key={person.user_id}
              className="flex items-center justify-between rounded-lg bg-card p-3"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-warning/20 text-xs font-medium text-warning">
                  {index + 1}
                </span>
                <span className="font-medium">{person.name}</span>
              </div>
              <div className="text-right">
                <p className="font-semibold text-warning">
                  {formatCurrency(person.unpaid_balance, currency)}
                </p>
                <p className="text-xs text-muted-foreground">
                  Avg delay: {person.average_delay_days?.toFixed(0) || 0} days
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
