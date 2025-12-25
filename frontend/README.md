# SplitSense Dashboard - Next.js Frontend

A best-in-class analytics dashboard for Splitwise data, built with modern web technologies.

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom design system
- **Components**: Radix UI primitives
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Data Fetching**: SWR

## Features

- 📊 **Summary Cards** - Net balance, monthly spend, subscriptions at a glance
- 📈 **Interactive Charts** - Spending trends, balance history, category breakdown
- 👥 **Group & Friend Views** - Expandable lists with detailed breakdowns
- 💡 **Smart Insights** - Cash flow analysis, settlement efficiency, friction detection
- ☕ **Buy Me a Coffee** - Tasteful support button with micro-interactions
- 📱 **Fully Responsive** - Mobile-first design
- ⌨️ **Accessible** - Keyboard navigation, ARIA labels
- ⚡ **Performance** - Skeleton loaders, optimistic updates

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm, npm, or yarn

### Installation

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### Backend Connection

The frontend proxies API requests to `http://localhost:8000`. Ensure the FastAPI backend is running:

```bash
# From project root
python main.py
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Dashboard page
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   ├── layout/          # Header, Footer, Nav
│   │   ├── dashboard/       # Dashboard-specific components
│   │   └── buy-me-coffee.tsx
│   ├── lib/
│   │   ├── api.ts           # API client & hooks
│   │   └── utils.ts         # Utility functions
│   ├── types/
│   │   └── api.ts           # TypeScript types
│   └── styles/
│       └── globals.css      # Global styles & Tailwind config
├── tailwind.config.ts
├── next.config.js
└── package.json
```

## Design System

### Colors

The design uses a Stripe-inspired color palette:

- **Primary**: Indigo (`hsl(238, 84%, 67%)`)
- **Success**: Green for positive balances
- **Destructive**: Red for amounts owed
- **Warning**: Amber for friction alerts
- **Muted**: Subtle grays for secondary content

### Typography

- Font: Inter (variable font)
- Sizes follow a modular scale
- Tabular numbers for financial data

### Animations

Framer Motion is used purposefully:

- Page transitions (fade-in-up)
- Card hover effects (subtle scale)
- Accordion open/close
- Loading states (shimmer)

## Components

### Buy Me a Coffee Button

Three variants available:

```tsx
<BuyMeCoffee variant="header" />  // In navigation
<BuyMeCoffee variant="footer" />  // Text link style
<BuyMeCoffee variant="floating" /> // Fixed position FAB
```

### Stat Cards

```tsx
<StatCard
  title="Total Spending"
  value={formatCurrency(1234, 'USD')}
  icon={CreditCard}
  trend="up"
  trendValue="+12%"
  tooltip="Your total spending across all groups"
/>
```

### Charts

All charts include:
- Responsive container
- Custom tooltips
- Annotation area for insights
- Gradient fills

## Performance

- **Skeleton loaders** instead of spinners
- **SWR** for data fetching with caching
- **Code splitting** via Next.js
- **Image optimization** (if images are added)

## Accessibility

- Keyboard navigation for all interactive elements
- ARIA labels on buttons and icons
- Focus indicators (visible ring)
- Color contrast meets WCAG AA

## UX Rationale

1. **Progressive Disclosure**: Summary cards show key metrics; charts reveal trends; tabs organize detailed views
2. **Visual Hierarchy**: Large balance numbers, muted secondary text, color-coded status
3. **Contextual Insights**: Each chart includes an "annotation" explaining why the data matters
4. **Zero Friction Onboarding**: Clear ingestion flow with API token or file upload options
5. **Delightful Details**: Subtle animations, hover states, and micro-interactions

## License

MIT
