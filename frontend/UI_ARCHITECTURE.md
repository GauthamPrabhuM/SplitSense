# SplitSense Dashboard - UI/UX Overhaul Summary

## Overview

This document outlines the complete UI/UX overhaul of the SplitSense dashboard, designed to meet best-in-class quality standards comparable to Stripe, Linear, Notion, and Vercel dashboards.

---

## 1. Buy Me a Coffee Integration ☕

### Implementation

Three variants are available to suit different contexts:

```tsx
// In header navigation - subtle, non-intrusive
<BuyMeCoffee variant="header" />

// In footer - text link style
<BuyMeCoffee variant="footer" />

// Floating FAB - appears after 1s delay
<BuyMeCoffee variant="floating" />
```

### Design Decisions

- **Non-disruptive**: Placed in header/footer, never blocking content
- **Brand-aligned**: Uses Buy Me a Coffee yellow (#FFDD00) with subtle transitions
- **Micro-interactions**: Scale on hover (1.02x), gentle tap feedback
- **Accessibility**: Opens in new tab, keyboard accessible, proper ARIA labels

### File Location
`frontend/src/components/buy-me-coffee.tsx`

---

## 2. UI Architecture

### Component Hierarchy

```
src/
├── app/                     # Next.js App Router pages
│   ├── layout.tsx          # Root layout with fonts, metadata
│   ├── page.tsx            # Main dashboard
│   ├── groups/page.tsx     # Groups detail view
│   ├── friends/page.tsx    # Friends & balances
│   ├── insights/page.tsx   # AI-powered insights
│   ├── loading.tsx         # Loading state
│   └── not-found.tsx       # 404 page
│
├── components/
│   ├── ui/                 # Primitives (shadcn/ui style)
│   │   ├── button.tsx      # Button with gradient variant
│   │   ├── input.tsx       # Form input
│   │   ├── skeleton.tsx    # Skeleton loaders
│   │   ├── tabs.tsx        # Tab navigation
│   │   ├── accordion.tsx   # Expandable sections
│   │   ├── tooltip.tsx     # Info tooltips
│   │   └── progress.tsx    # Progress bars
│   │
│   ├── layout/             # Layout components
│   │   ├── header.tsx      # Navigation header
│   │   └── footer.tsx      # Site footer
│   │
│   ├── dashboard/          # Dashboard-specific
│   │   ├── stat-card.tsx   # StatCard, BalanceCard
│   │   ├── charts.tsx      # All Recharts components
│   │   ├── lists.tsx       # GroupList, FriendList, FrictionList
│   │   └── data-ingestion.tsx  # API/file import flow
│   │
│   └── buy-me-coffee.tsx   # Support button
│
├── lib/
│   ├── utils.ts            # Utility functions (cn, formatCurrency, etc.)
│   └── api.ts              # API client with SWR hooks
│
├── types/
│   └── api.ts              # TypeScript interfaces
│
└── styles/
    └── globals.css         # Tailwind + CSS variables
```

---

## 3. Design System

### Color Palette (Stripe-inspired)

```css
/* Light Mode */
--primary: 238 84% 67%;        /* Indigo */
--success: 142 76% 36%;        /* Green - positive balances */
--destructive: 0 84% 60%;      /* Red - amounts owed */
--warning: 38 92% 50%;         /* Amber - friction alerts */
--muted: 220 14% 96%;          /* Subtle backgrounds */

/* Chart Colors */
--chart-1: Indigo
--chart-2: Purple
--chart-3: Green
--chart-4: Amber
--chart-5: Red
```

### Typography

- **Font**: Inter (variable)
- **Weights**: 400 (body), 500 (medium), 600 (semibold), 700 (bold)
- **Features**: `tabular-nums` for financial data alignment

### Spacing Scale

Tailwind default with custom additions:
- `text-2xs`: 0.625rem for micro labels

### Shadows

```css
--shadow-card: subtle elevation for cards
--shadow-card-hover: enhanced on interaction
--shadow-glow: primary color glow for CTAs
```

---

## 4. Key Components

### StatCard

```tsx
<StatCard
  title="Total Spending"
  value={formatCurrency(12345, 'USD')}
  subtitle="All time"
  icon={CreditCard}
  trend="up"
  trendValue="+12%"
  tooltip="Your total spending across all groups"
  variant="default" // or 'positive', 'negative', 'highlight'
/>
```

**Features:**
- Fade-in animation with staggered delay
- Icon container with brand color
- Trend indicator with arrow icon
- Hover glow effect
- Info tooltip for context

### BalanceCard

Large hero card showing:
- Net balance with color-coded status
- "You are owed" / "You owe" badge
- Breakdown of owed to you vs you owe
- Gradient background pattern

### Charts (Recharts)

1. **SpendingChart** - Area chart with gradient fill
2. **BalanceChart** - Area chart with positive/negative colors
3. **CategoryChart** - Donut chart with legend
4. **GroupChart** - Horizontal bar chart

All charts include:
- Custom tooltips matching design system
- Responsive containers
- Annotation area explaining insights
- Grid lines using border color

### Lists with Progressive Disclosure

- **GroupList**: Expandable accordion with spending details
- **FriendList**: Balance by person with avatar initials
- **FrictionList**: Warning-styled for overdue settlements

---

## 5. Animations (Framer Motion)

### Principles

1. **Purposeful**: Motion serves a function (feedback, hierarchy)
2. **Subtle**: Never distracting or slow
3. **Consistent**: Same easing and timing across app

### Implementations

```tsx
// Page entry
initial={{ opacity: 0 }}
animate={{ opacity: 1 }}
transition={{ duration: 0.5 }}

// Card stagger
transition={{ delay: index * 0.1 }}

// Hover feedback
whileHover={{ scale: 1.02 }}
whileTap={{ scale: 0.98 }}

// Accordion content
data-[state=open]:animate-accordion-down
data-[state=closed]:animate-accordion-up
```

---

## 6. Loading States

### Skeleton Loaders (Not Spinners)

```tsx
<CardSkeleton />    // For stat cards
<ChartSkeleton />   // For charts with mock bars
<TableSkeleton />   // For lists with avatar placeholders
```

**CSS Animation:**
```css
.skeleton::after {
  animation: shimmer 2s infinite;
  background: linear-gradient(90deg, transparent, rgba(...), transparent);
}
```

---

## 7. Responsive Design

### Breakpoints

- Mobile: < 640px (single column)
- Tablet: 640px - 1024px (2 columns)
- Desktop: > 1024px (4-column grid)

### Mobile Considerations

- Hamburger menu for navigation
- Stacked cards
- Touch-friendly tap targets (min 44px)
- Swipeable charts

---

## 8. Accessibility

### Keyboard Navigation

- All interactive elements focusable
- Tab order follows visual hierarchy
- Enter/Space activates buttons
- Escape closes modals/menus

### ARIA

- Labels on icon-only buttons
- Live regions for status updates
- Role attributes on custom components

### Focus Indicators

```css
.focus-ring {
  @apply focus-visible:outline-none 
         focus-visible:ring-2 
         focus-visible:ring-ring 
         focus-visible:ring-offset-2;
}
```

---

## 9. Performance Optimizations

1. **SWR Caching**: Prevents unnecessary refetches
2. **Code Splitting**: Next.js automatic page chunking
3. **Skeleton States**: Perceived performance improvement
4. **Memoization**: `useMemo` for chart data transformations
5. **Font Optimization**: Next.js font loader with display=swap

---

## 10. UX Rationale

### Progressive Disclosure

- **Level 1**: Summary cards (glanceable)
- **Level 2**: Charts (trends over time)
- **Level 3**: Expandable lists (details on demand)
- **Level 4**: Dedicated pages (deep dives)

### Visual Hierarchy

1. Balance card (largest, top-left)
2. Stat cards (medium, top row)
3. Charts (large, main content)
4. Lists (compact, secondary)

### Contextual Insights

Each data point includes:
- What it means (title/value)
- Why it matters (tooltip/annotation)
- What to do (actionable insights)

### Error Prevention

- Clear ingestion flow with two paths (API/file)
- Inline validation feedback
- Graceful error states with retry options

---

## 11. Getting Started

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

Ensure the FastAPI backend is running on `http://localhost:8000`.

---

## 12. File Index

| File | Purpose |
|------|---------|
| `src/app/page.tsx` | Main dashboard page |
| `src/app/layout.tsx` | Root layout with metadata |
| `src/components/buy-me-coffee.tsx` | Support button (3 variants) |
| `src/components/layout/header.tsx` | Navigation with logo, links, BMC |
| `src/components/layout/footer.tsx` | Footer with links |
| `src/components/dashboard/stat-card.tsx` | StatCard, BalanceCard |
| `src/components/dashboard/charts.tsx` | All chart components |
| `src/components/dashboard/lists.tsx` | Group, Friend, Friction lists |
| `src/components/dashboard/data-ingestion.tsx` | API/file import UI |
| `src/components/ui/*.tsx` | Primitive UI components |
| `src/lib/api.ts` | SWR hooks, API functions |
| `src/lib/utils.ts` | Utilities (cn, format, etc.) |
| `src/types/api.ts` | TypeScript interfaces |
| `src/styles/globals.css` | Tailwind config, CSS vars |
| `tailwind.config.ts` | Extended Tailwind config |

---

## Conclusion

This UI/UX overhaul delivers a production-ready, Stripe-quality dashboard that prioritizes:

✅ **Clarity** - Every metric is understandable at a glance  
✅ **Performance** - Skeleton loaders, caching, code splitting  
✅ **Accessibility** - Keyboard nav, ARIA, focus states  
✅ **Delight** - Purposeful animations, thoughtful interactions  
✅ **Monetization** - Tasteful Buy Me a Coffee integration  

The codebase is maintainable, extensible, and ready for v1 launch.
