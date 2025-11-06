# project structure

`app.py` -- app; navigation/navbar; set default landing to `about.py`

---
```
- app.py
- pages/
  -  about.py
  -  select_criteria.py
  -  interview.py
  -  results.py
  -  dashboard.py
```
---

`about.py` -- landing pg; info on website

> [!NOTE]
> TODO: refactor, improve contents, beautify

---

Practice Interview : 3 pages

1. `select_criteria.py` -- select criteria to get random question

    > [!NOTE]
    > TODO: expand criteria (leetcode modes, question types); feed dataset/source (question bank) to QUESTIONS

2. `interview.py` -- solve the given question through (1) code, (2) recorded-verbal response(s) 

    > [!NOTE]
    > TODO: solve the given question; code editor(?), audio recording, transcript, etc.

    > option 1: (resource-heavy) - upon start (countdown 3s), coding IDE with continuous audio recording (supplemental questions prompted during session), end with set time limit or 'stop', evaluate code && full audio transcript

    > option 2: (simpler) - upon start (countdown optional), coding IDE with submission, upon 'submit' prompt/ask follow-up question(s) on code/complexity/design/algorithm/alternatives/etc., record audio, end with 'stop/submit' (submit both (1) code and (2) audio transcript)

3. `results.py` -- review (code, transcript, results), generate feedback & advice, evaluate based on rubric

    > [!NOTE]
    > TODO: evaluate (1) code & (2) transcript based on **metrics/rubric** -- task/**role C**

---

`dashboard.py` -- agg results, filter based on criteria/date/etc., charts & viz., metrics & goals & progress tracking(?)