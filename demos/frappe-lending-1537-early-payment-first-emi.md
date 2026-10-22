# frappe/lending #1537: what a "first EMI date" fix touches outside its diff

- **Type:** impact analysis of a merged upstream fix (not a bug report)
- **Repository:** [frappe/lending](https://github.com/frappe/lending)
- **Upstream:** issue [#1536](https://github.com/frappe/lending/issues/1536) · fix [#1537](https://github.com/frappe/lending/pull/1537) (merged 22 Oct 2026) · backport [#1538](https://github.com/frappe/lending/pull/1538)
- **Code read at:** `develop` @ `267b698`
- **Test-coverage note shared upstream:** in the [#1537 conversation](https://github.com/frappe/lending/pull/1537)

> The fix itself was written and merged by the frappe/lending maintainers. This case only documents what the change affects outside its diff and one test-coverage gap. It is an engineering analysis, not an endorsement by Frappe.

## The question

> What do commits f0364f4, 43ed56c and 3c5dfdc change in `loan_repayment_schedule.py`, and what outside the diff can they affect?

## What the three commits do

When a **Pre Payment** or **Advance Payment** was made before the first EMI, the regenerated schedule started from the payment date and pulled the agreed first EMI months earlier (#1536).

| Commit | Change |
|---|---|
| `f0364f4` | `next_emi_date` can no longer be earlier than the previous schedule's `repayment_start_date` (advance and pre payment branches). Adds `test_prepayments_before_first_emi_keep_deferred_repayment_start_date`. |
| `43ed56c` | After one early payment, `repayment_start_date` itself moves ahead, so a second early payment pushed the first EMI out again. Adds `get_first_emi_date()`, which reads the first row with principal. Test now makes two early payments. |
| `3c5dfdc` | A first row with no principal (interest-only) was skipped. `get_first_emi_date()` now uses the first row only when the previous schedule came from an early payment, and `repayment_start_date` otherwise. No test change. |

Final code (`lending/loan_management/doctype/loan_repayment_schedule/loan_repayment_schedule.py`):

```python
def get_first_emi_date(self, prev_schedule, schedule_field):
    # An early payment moves repayment_start_date ahead, but its schedule has no upfront interest row,
    # so the first row is the first EMI. Other schedules keep the agreed date in repayment_start_date.
    if prev_schedule.restructure_type in ("Pre Payment", "Advance Payment"):
        return getdate(prev_schedule.get(schedule_field)[0].payment_date)

    return getdate(prev_schedule.repayment_start_date)
```
`loan_repayment_schedule.py:970-976`

## Where the change sits in the flow

All verified in code at `267b698`.

| Step | Location |
|---|---|
| Schedule `validate()` | `loan_repayment_schedule.py:94` |
| → `make_customer_repayment_schedule()` | `:102` |
| → `add_rows_from_prev_disbursement()` | `:338` (defined at `:714`) |
| Early-payment check, previous schedule loaded | `:726`, `:734` |
| Advance Payment: new floor on `next_emi_date` | `:857-859` |
| Pre Payment: new floor on `next_emi_date` | `:905-910` |
| First row of the new schedule added | `:864` (advance), `:944` (pre) |
| `repayment_start_date` moved to the following EMI | `:885`, `:961` |

## Impact outside the diff

- **Interest for the gap (verified in code).** The new first EMI date also sets `pending_prev_days = date_diff(next_emi_date, posting_date)`, which drives the interest added for that period (`:878-882` advance, `:914-918` pre). Keeping the agreed later date therefore also changes how much interest the first row carries.
- **Demands and accruals (inferred).** `process_daily_loan_demands` (`process_loan_demand.py:48`) and `process_loan_interest_accrual_for_loans` (`process_loan_interest_accrual.py:62`) work from the active schedule, so they follow the corrected dates. The exact lines where they read the schedule were not traced.
- **Not a new crash path (checked).** `get_first_emi_date()` indexes `[0]`, but `first_date` already reads the same row earlier (`:748`), so an empty schedule would fail before this change too.

## Test coverage

- `test_prepayments_before_first_emi_keep_deferred_repayment_start_date` (`test_loan_repayment.py:278`) uses `rate_of_interest=0` and no moratorium, so the previous schedule never has an interest-only first row.
- The tests found that combine a Principal moratorium with a Pre Payment (`test_correct_moratorium_periods_after_restructure`, `test_accrual_breaks_for_advance_and_pre_payments` in `test_loan_repayment_schedule.py`) pay on 2025-12-05, after the first EMI, so they do not reach the `posting_date < first_date` branch.
- **Gap:** no test found for an early payment made before an interest-only first EMI, the case `3c5dfdc` changes. Search scope: tests mentioning Pre/Advance Payment and `moratorium_tenure`. Interest-only rows from other sources were not searched.

## How Meeba Brain did on this question

- Got right: the purpose of each commit, the call chain and line numbers above, the existing tests, and the interest-only test gap (in one of the runs).
- Missed: the effect on gap interest (`pending_prev_days`); downstream claims about demands and accruals were not cited at the line level.
- Earlier runs on the same question invented commit messages for the two commits they had not read. This was fixed by reading every named commit's diff before answering, and checking quoted historical code against that commit instead of the current file.

## Not verified

- Nothing here was run. Frappe tests need a bench with MariaDB, which was not set up for this analysis.
- Whether the maintainers consider the interest-only gap worth a test is their call.
