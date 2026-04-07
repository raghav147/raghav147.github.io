# Tableau Assignment Grader (M2.2 Ready)

This grader is set up for your assignment:

**M2.2: Walkthrough - Configuring and Setting Up Your Data**

It evaluates Tableau **packaged workbook submissions** (`.twbx`) and generates a score table with:

- score out of **25**,
- missed walkthrough topic(s),
- points missed (5 points each topic),
- file naming validity.

---

## 1) What this grader checks

For M2.2, the default rubric checks these five walkthrough topics (5 points each):

1. Connecting and Cleaning Data
2. Splitting Data
3. Relationships and Joins
4. Pivoting Data
5. Extracting Data

Rubric file:

- `tableau-assignment-grader/rubric.m2_2_configuring_and_setting_up_your_data.json`

> Important: Tableau workbooks can be authored in slightly different ways. If your class uses different field names/table captions, update the rubric JSON strings to match your class template exactly.

---

## 2) Submission requirements captured

The assignment says students should submit:

- a `.twbx` packaged workbook,
- with naming format: `lastname_firstname_ConfiguringAndSettingUpYourData.twbx`.

The grader can validate this naming pattern using `--filename-regex` and reports it as `filename_valid` in the output CSV.

---

## 3) Quick start (copy/paste)

From repo root:

```bash
python3 tableau-assignment-grader/grade_tableau.py \
  --submissions ./submissions \
  --rubric ./tableau-assignment-grader/rubric.m2_2_configuring_and_setting_up_your_data.json \
  --output ./grades_m2_2.csv \
  --filename-regex '^[A-Za-z]+_[A-Za-z]+_ConfiguringAndSettingUpYourData\.twbx$'
```

---

## 4) Very detailed starter guide

### Step A — Create a clean grading folder structure

```text
/workspace/raghav147.github.io/
  submissions/
    student files here (*.twbx)
  tableau-assignment-grader/
    grade_tableau.py
    rubric.m2_2_configuring_and_setting_up_your_data.json
```

Recommended:

- Keep only files for one assignment run inside `submissions/`.
- Remove duplicate student uploads before grading.
- Keep original files untouched; do not manually unzip/modify student files.

### Step B — Validate Python availability

```bash
python3 --version
```

The script only uses Python standard library, so no pip install is required.

### Step C — (Optional but recommended) dry run with `--help`

```bash
python3 tableau-assignment-grader/grade_tableau.py --help
```

This confirms CLI options are available.

### Step D — Run grading for M2.2

```bash
python3 tableau-assignment-grader/grade_tableau.py \
  --submissions ./submissions \
  --rubric ./tableau-assignment-grader/rubric.m2_2_configuring_and_setting_up_your_data.json \
  --output ./grades_m2_2.csv \
  --filename-regex '^[A-Za-z]+_[A-Za-z]+_ConfiguringAndSettingUpYourData\.twbx$'
```

### Step E — Open and interpret `grades_m2_2.csv`

Columns produced:

- `student`: filename stem
- `file`: full submitted filename
- `filename_valid`: `True`/`False` against required naming pattern
- `score`: earned points
- `total_points`: usually 25
- `percent`: score percentage
- `missed_points`: points lost
- `missed_checks`: human-readable walkthrough checks missed
- `passed_checks`: check IDs that passed

Example interpretation:

- `score=20.00`, `missed_points=5.00` and `missed_checks` contains `pivoting_data` means the student missed the Pivoting Data walkthrough evidence.

### Step F — Re-grade after rubric adjustment (if needed)

If your instructor file has different naming conventions (for example `Resolved Incidents1` instead of `Resolved Incidents`):

1. Open the rubric JSON.
2. Update `contains` or field names for the relevant check.
3. Run the same command again.

---

## 5) Running against an instructor-provided sample `.twbx`

When you provide a known-good sample `.twbx`:

1. Place sample file in `./submissions`.
2. Run the command above.
3. Confirm the sample gets full score (25).

If the sample does not get 25:

- inspect the missed check text in CSV,
- adjust rubric text match to the exact field/table labels used in that workbook,
- re-run.

---

## 6) Supported check types (for custom rubrics)

- `worksheet_exists`
- `dashboard_exists`
- `datasource_exists`
- `field_exists`
- `calculation_contains`
- `workbook_text_contains`
- `workbook_text_not_contains`
- `all_of` (nested)
- `any_of` (nested)

Each top-level check typically has:

- `id`
- `description`
- `type`
- `points`

---

## 7) Notes and limitations

- The grader infers walkthrough completion from final workbook artifacts.
- It cannot verify every click path in Tableau UI; it verifies evidence in workbook XML.
- For strict grading consistency, calibrate rubric checks against:
  - one known perfect student sample,
  - one intentionally incomplete sample.

---

## 8) Minimal command set for each grading cycle

```bash
# 1) grade
python3 tableau-assignment-grader/grade_tableau.py \
  --submissions ./submissions \
  --rubric ./tableau-assignment-grader/rubric.m2_2_configuring_and_setting_up_your_data.json \
  --output ./grades_m2_2.csv \
  --filename-regex '^[A-Za-z]+_[A-Za-z]+_ConfiguringAndSettingUpYourData\.twbx$'

# 2) review
cat ./grades_m2_2.csv
```
