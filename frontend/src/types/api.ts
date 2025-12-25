// API Types matching backend schemas
export interface Insights {
  spending: SpendingInsight;
  balance: BalanceInsight;
  categories: CategoryInsight;
  groups: GroupInsight;
  subscriptions: SubscriptionInsight;
  cash_flow: CashFlowInsight;
  settlement_efficiency: SettlementEfficiency;
  balance_prediction: BalancePrediction;
  friction: FrictionInsight;
  anomalies: AnomalyInsight;
  validation: ValidationResult;
  data_summary: DataSummary;
}

export interface SpendingInsight {
  total_spending: number;
  monthly_average: number;
  monthly_breakdown: Record<string, number>;
  currency_code: string;
  spending_trend: 'increasing' | 'decreasing' | 'stable';
  peak_month: string;
  peak_amount: number;
  explanation: string;
}

export interface BalanceInsight {
  net_balance: number;
  total_owed_to_you: number;
  total_you_owe: number;
  owed_to_user: number;
  user_owes: number;
  currency_code: string;
  trend_over_time: Record<string, number>;
  by_person: Record<string, number>;  // user_id -> net balance (from backend)
  explanation: string;
}

export interface PersonBalance {
  user_id: number;
  name: string;
  balance: number;
  direction: 'owed' | 'owe';
}

export interface CategoryInsight {
  top_categories: CategoryBreakdown[];
  category_trends: Record<string, Record<string, number>>;
  currency_code: string;
  explanation: string;
}

export interface CategoryBreakdown {
  category: string;
  amount: number;
  percentage: number;
  count: number;
}

export interface GroupInsight {
  by_group: Record<string, GroupByGroupEntry>;
  top_groups: TopGroup[];
  currency_code: string;
  explanation: string;
}

export interface GroupByGroupEntry {
  name: string;
  total_spending: number;
  expense_count: number;
  member_count: number;
}

export interface TopGroup {
  group_id: number | null;
  name: string;
  total_spending: number;
  expense_count: number;
  member_count: number;
}

export interface GroupBreakdown {
  id: number;
  name: string;
  total_spending: number;
  expense_count: number;
  member_count: number;
  your_share: number;
}

export interface SubscriptionInsight {
  subscriptions: Subscription[];
  total_monthly_subscriptions: number;
  currency_code: string;
  explanation: string;
}

export interface Subscription {
  description: string;
  amount: number;
  frequency: 'weekly' | 'monthly' | 'yearly';
  category: string;
}

export interface CashFlowInsight {
  net_cash_flow: number;
  total_paid: number;
  total_received: number;
  front_pay_percentage: number;
  currency_code: string;
  explanation: string;
}

export interface SettlementEfficiency {
  unpaid_balances_count: number;
  unpaid_balances_total: number;
  average_settlement_days: number;
  currency_code: string;
  explanation: string;
}

export interface BalancePrediction {
  predicted_balance: number;
  trend: 'increasing' | 'decreasing' | 'stable';
  currency_code: string;
  confidence_level: string;
  based_on_months: number;
  explanation: string;
}

export interface FrictionInsight {
  by_person: FrictionPerson[];
  explanation: string;
}

export interface FrictionPerson {
  user_id: number;
  name: string;
  unpaid_balance: number;
  average_delay_days: number;
  friction_score: number;
}

export interface AnomalyInsight {
  anomalies: Anomaly[];
  explanation: string;
}

export interface Anomaly {
  expense_id: number;
  description: string;
  amount: number;
  date: string;
  reason: string;
  severity: 'low' | 'medium' | 'high';
}

export interface ValidationResult {
  is_valid: boolean;
  errors: string[];
  warnings: string[];
}

export interface DataSummary {
  total_expenses: number;
  total_groups: number;
  date_range: {
    earliest: string;
    latest: string;
  };
  currencies: string[];
  original_currency: string;
  base_currency: string;
}

export interface Charts {
  spending_trend: string;
  balance_trend: string;
  category_pie: string;
  group_bar: string;
  anomaly: string;
  subscription: string;
}

export interface IngestResponse {
  status: string;
  expenses_count: number;
  groups_count: number;
  message: string;
}
