# Architecture Overview

## Design Principles

1. **Modularity**: Each component (ingestion, validation, analytics, visualization) is independent and testable
2. **Correctness**: All calculations are verifiable with unit tests and validation checks
3. **Type Safety**: Pydantic models ensure data integrity throughout the pipeline
4. **Privacy**: Sensitive data is masked by default, tokens are not stored
5. **Extensibility**: Easy to add new analytics or data sources

## Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│                      (main.py)                           │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐      ┌─────────▼──────────┐
│   Ingestion    │      │   Visualization    │
│                │      │                    │
│ - API Client   │      │ - Chart Generator  │
│ - File Parser  │      │ - Dashboard HTML   │
│ - Normalizer   │      └────────────────────┘
└───────┬────────┘
        │
┌───────▼────────┐
│  Validation    │
│                │
│ - DataVerifier │
│ - Cross-checks │
└───────┬────────┘
        │
┌───────▼────────┐
│   Analytics    │
│                │
│ - Spending     │
│ - Balances     │
│ - Categories   │
│ - Groups       │
│ - Advanced     │
└────────────────┘
```

## Data Flow

1. **Ingestion**
   - API: `SplitwiseAPIClient` → Fetch → Parse → `Expense`/`Group` models
   - File: `FileParser` → Read → Parse → `Expense`/`Group` models

2. **Normalization**
   - `DataNormalizer` → Currency conversion → Timestamp normalization

3. **Validation**
   - `DataVerifier` → Cross-verify totals → Check consistency → `ValidationResult`

4. **Analytics**
   - Multiple analyzers → Process normalized data → Generate insights

5. **Visualization**
   - `ChartGenerator` → Convert insights to Plotly charts → HTML output

## Key Design Decisions

### Currency Normalization
- All amounts are normalized to a base currency (default: USD)
- Exchange rates are simplified (in production, use historical rates API)
- Multi-currency expenses are converted at transaction time

### Data Integrity
- Every expense is validated: `sum(paid_shares) == sum(owed_shares)`
- Group balances must sum to zero
- Settlements are verified separately
- Currency consistency is checked per group

### Balance Calculation
- Net balance = sum(paid - owed) for current user
- Positive = user is owed money
- Negative = user owes money
- Balances are tracked over time for trend analysis

### Recurring Expense Detection
- Groups expenses by description pattern (first 3 words)
- Requires at least 3 occurrences
- Calculates average amount and frequency
- Identifies monthly subscriptions

### Anomaly Detection
- Uses statistical method: mean + (multiplier × standard deviation)
- Default threshold: 3× standard deviation
- Flags expenses significantly above average

### Settlement Efficiency
- Tracks time between expense and settlement
- Calculates average and median settlement days
- Identifies unpaid balances

## Testing Strategy

1. **Unit Tests**: Each analyzer and validator has isolated tests
2. **Integration Tests**: Full pipeline from ingestion to insights
3. **Validation Tests**: Verify correctness of calculations
4. **Edge Cases**: Empty data, single expense, etc.

## Security Considerations

1. **Token Handling**
   - Tokens are never stored unless explicitly enabled
   - Tokens are masked in logs
   - Environment variables preferred over hardcoding

2. **Data Privacy**
   - Sensitive data (names, amounts) can be masked
   - All processing is local (no external API calls except Splitwise)
   - Optional storage can be disabled

3. **Input Validation**
   - File size limits
   - Type checking via Pydantic
   - Error handling for malformed data

## Performance Considerations

1. **Pagination**: API client handles pagination automatically
2. **Rate Limiting**: Built-in delays to respect API limits
3. **Lazy Loading**: Charts generated on-demand
4. **Caching**: Insights cached in memory (in production, use Redis/DB)

## Extensibility Points

1. **New Data Sources**: Add parsers to `ingestion/file_parser.py`
2. **New Analytics**: Add analyzers to `analytics/` directory
3. **New Charts**: Add methods to `visualization/charts.py`
4. **New Validations**: Add checks to `validation/verifier.py`

## Limitations & Future Improvements

1. **Currency Conversion**: Currently uses static rates; should use historical API
2. **Settlement Matching**: Simplified matching; could be more sophisticated
3. **User Identification**: Current user ID detection could be improved
4. **Storage**: Optional DuckDB storage; could add PostgreSQL/MySQL support
5. **Real-time Updates**: Currently batch processing; could add webhooks

