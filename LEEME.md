# Local Vulnerability and AI Lab

First exercise: SQL injection. Requires Python 3; no packages, Docker, keys, or accounts. All users are fictional, and the in-memory database is recreated for every search. The server listens only on 127.0.0.1. Keep it bound to loopback; do not tunnel or publish it.

## 1. Start the lab

In Terminal:

```bash
cd path/to/local-sql-ai-lab
python3 app.py
```

Open http://127.0.0.1:8765 and search for `ana`. You will see one row. Then search for this input, including the leading quote:

```text
' OR '1'='1
```

You will see three rows: the input changed the query condition and exposed more data than intended.

## 2. Detect

In another Terminal window:

```bash
cd path/to/local-sql-ai-lab
python3 detectar.py
```

The report should show `status: suspicious` in vulnerable mode. This detector is a probe for this specific exercise, not a general scanner or a complete audit. A suspicious result is not confirmation of a vulnerability.

## 3. Parameterize and repeat

Stop the server with Ctrl+C and run:

```bash
python3 app.py --seguro
```

Run `python3 detectar.py` again in the other terminal. It should now show `not_detected`: the parameterized query treats the input as data. The legitimate search for `ana` still works. `not_detected` does not prove that other flaws are absent.

## 4. Study with an AI assistant

Start your AI assistant from this folder and ask:

> We are studying an authorized local lab with fictional data. Read app.py, detectar.py, and verificar.py. Explain how concatenation lets input alter a query and how parameters prevent that. Use code examples and distinguish evidence from assumptions. Do not modify files or access external systems. Ask three questions to check my understanding, then suggest ways to evaluate detector false positives and false negatives.

AI can help explain and investigate. Reproducible comparison between the two modes provides evidence. This exercise uses no CVEs or vulnerable dependencies and does not integrate an AI API.

## 5. Run the tests

```bash
python3 verificar.py
python3 -m unittest -v test_detectar
```

The tests cover the legitimate search, unintended data exposure in vulnerable mode, parameterized behavior, detector status classification, and inconclusive network/response errors. Suggested next exercise: review dependencies in a small project and prioritize findings by exposure and actual use.

## Blind SQL classification exercise

Use `SQL_EXAMPLES_BLIND.md` to ask an AI model to classify six snippets as vulnerable or correctly parameterized. Check its answers against `SQL_EXAMPLES_ANSWER_KEY.md` only after it responds.
