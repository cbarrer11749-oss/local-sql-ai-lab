# SQL Classification and Repair Experiment Results

## Classification results (previously reported)

- Initial classification: 9/10.
- After the consistency review: 10/10. The review identified and corrected B's inconsistent label: its reasoning described a query altered by untrusted input, so the classification was changed to vulnerable.

These scores are reported from the earlier evaluation; they were not recalculated during preparation of this file.

## Repairs and test evidence

B, F, and I were repaired in the separate `SQL_REPAIR_EXERCISE`; the original evaluation exercises were preserved.

- Previously reported repair-suite result: 6 tests passed after implementing the repairs.
- Previously reported mutation checks: each targeted test failed in a temporary copy with its corresponding vulnerability restored. B's comment-based injection test failed with a SQLite binding error; F's payload returned both rows; I's payload bypassed integer validation. The temporary copies were removed.
- Previously reported strengthened-B experiment: the SELECT-expression input `name || '!' AS name` executed in a temporary vulnerable copy and returned `[('Alice!',)]`; against the repaired implementation, the allowlist rejected it with `ValueError`. The test addition retained the existing tests, and 7 tests passed afterward.
- Rerun while preparing this file: `python3 -m unittest -v` in `SQL_REPAIR_EXERCISE` passed all 7 tests.

The mutation experiments used temporary copies and did not alter the repaired implementation. The strengthened B test asserts the intended allowlist rejection; the vulnerable-copy check demonstrated the expression's effect on returned data.

## Limitations

- The examples and tests are small and hand-written; they do not cover the breadth of SQL injection patterns or application environments.
- The reviewed cases are no longer blind, so later results are not independent blind-evaluation results.
- Passing these tests does not establish production reliability or security in a real application.

## Model and settings

- Model identifier available for this session: `gpt-6-luna`.
- Provider available for this session: `openai-codex`.
- Other relevant generation/evaluation settings: unknown; none were available in the recorded experiment context.
