# Round two answer key — keep separate until predictions are saved

This is an educational rubric, not a measured benchmark. Credit a classification only when its reasoning matches the stated assumptions. Safe means safe against SQL injection within the shown code, not secure in every respect.

| ID | Expected classification | Reason |
|---|---|---|
| A | Safe against SQL injection | The identifier comes only from a fixed mapping; the value is bound. |
| B | Vulnerable | Binding name does not protect a separately interpolated untrusted SQL expression. |
| C | Safe against SQL injection | int converts accepted input into an integer rendered as numeric text; SQL syntax in raw input cannot survive conversion. Invalid input can still cause an exception. |
| D | Uncertain | Safety depends on the missing clean_name implementation and database context. Concatenation is suspicious but the function could enforce a strict safe allowlist or could provide no protection. |
| E | Safe against SQL injection | The entire pattern is bound as data. User-supplied LIKE wildcards may broaden matching, which is a separate behavior question. |
| F | Vulnerable | Removing semicolons does not prevent changing a condition within a single statement. |
| G | Safe against SQL injection | Only generated placeholder punctuation enters the query text; all external strings are bound separately. |
| H | Uncertain | A compatible driver normally binds this form safely, but an unknown wrapper could interpolate it unsafely or reject it. Need the actual execute implementation and driver contract. |
| I | Vulnerable | A nonempty check does not restrict the SQL syntax concatenated into the numeric expression. |
| J | Safe against SQL injection | Only the fixed constants ASC or DESC can enter the query text. |

## Scoring

Expected totals: 5 safe, 3 vulnerable, 2 uncertain. Record each prediction before opening this file. Report the full three-class confusion matrix, correct cases out of 10, vulnerable cases classified safe, safe cases classified vulnerable, and uncertain cases asserted confidently safe/vulnerable. Do not count an uncertain prediction as a correct vulnerability finding. Review explanations as well as labels; confidence alone is not evidence of calibration.

For later rounds, use fresh cases and shuffle ordering again. This set remains small, hand-written, and limited to SQL construction patterns.
