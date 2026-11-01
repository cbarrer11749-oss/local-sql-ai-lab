# Local SQL Security and AI Lab

A small educational Python lab for reproducing SQL injection, checking a parameterized repair, and evaluating an AI assistant's security reasoning. It uses fictional data and the Python standard library; no API keys, external services, or third-party packages are required.

The application intentionally starts in a vulnerable mode. It binds to `127.0.0.1` only. Run it locally; do not expose it through a public interface or tunnel. The detector is designed for this lab, not for scanning external systems.

## Quick start

Open a terminal in the repository root:

```bash
python3 app.py
```

Open http://127.0.0.1:8765. Search for `ana`, then compare with:

```text
' OR '1'='1
```

In a second terminal at the repository root:

```bash
python3 detectar.py
```

The vulnerable mode should produce `suspicious`. Stop the server with Ctrl+C and start the corrected mode:

```bash
python3 app.py --seguro
```

Repeat the probe. The result should be `not_detected`. A failed or invalid response produces `inconclusive`. Neither a negative result nor a passing suite establishes that an application is secure.

## Tests

From the repository root:

```bash
python3 verificar.py
python3 -m unittest -v test_detectar
```

Run the separate repair exercise:

```bash
cd SQL_REPAIR_EXERCISE
python3 -m unittest -v test_sql_repairs.py
```

Detector integration tests open loopback ports and launch local subprocesses. They require an environment that permits these operations.

## Repository guide

| File or folder | Purpose |
|---|---|
| `app.py` | Vulnerable and corrected SQLite search application |
| `detectar.py` | Lab-specific HTTP probe |
| `verificar.py`, `test_detectar.py` | Application and detector checks |
| `LEEME.md` | Detailed walkthrough in English; original filename retained |
| `SQL_EXAMPLES_BLIND.md` | Introductory model classification exercise |
| `SQL_ADVANCED_BLIND.md` | Harder exercise with missing-context cases |
| `SQL_*ANSWER_KEY.md` | Separate reference classifications |
| `SQL_REPAIR_EXERCISE/` | Repairs, tests, and recorded experiment results |

Some original filenames, identifiers, endpoint fields, and command-line flags remain in Spanish for compatibility. Documentation and user-facing explanations are in English.

## AI evaluation

Use a fresh assistant conversation and provide only the selected blind file. Ask for classifications, reasons, confidence, and missing evidence. Save the initial answers before revealing the key or requesting review. Keep initial and reviewed scores separate.

The recorded advanced exercise scored 9/10 initially and 10/10 after a consistency review. Those are historical results from a small, hand-written set, not a benchmark or evidence of production reliability. The model attribution in the results file was reported by the assistant and has not been independently verified. Published answer keys may be accessible to models with repository tools; instructing a model not to read them is not an access-control boundary.

The detector also includes an intentional false-positive example: legitimate suggestions can expand the results without SQL injection. Its `suspicious` status is a signal requiring investigation, not confirmation.

## Sharing and contributions

Do not commit credentials, private data, chat exports, or runtime logs. No license has been selected yet; public visibility alone does not grant an open-source license. Choose a license before inviting reuse under specific terms.
