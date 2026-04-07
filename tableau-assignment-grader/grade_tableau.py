#!/usr/bin/env python3
"""Grade Tableau packaged workbook submissions against a configurable rubric.

Supports .twbx (preferred), .twbx, and legacy .tbbx packaged workbooks.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET


@dataclass
class WorkbookIndex:
    worksheets: set[str]
    dashboards: set[str]
    datasources: set[str]
    fields: set[str]
    calculations: List[str]
    workbook_text: str


@dataclass
class CheckResult:
    check_id: str
    description: str
    points: float
    passed: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Grade Tableau packaged workbook files from a JSON rubric."
    )
    parser.add_argument("--submissions", required=True, type=Path, help="Folder with submissions")
    parser.add_argument("--rubric", required=True, type=Path, help="Rubric JSON file")
    parser.add_argument("--output", required=True, type=Path, help="Output CSV path")
    parser.add_argument(
        "--extensions",
        default=".twbx,.twbx,.tbbx",
        help="Comma-separated submission file extensions to include",
    )
    parser.add_argument(
        "--filename-regex",
        default="",
        help="Optional regex filenames must match (example: ^[A-Za-z]+_[A-Za-z]+_ConfiguringAndSettingUpYourData\\.twbx$)",
    )
    return parser.parse_args()


def read_rubric(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as f:
        rubric = json.load(f)

    if "checks" not in rubric or not isinstance(rubric["checks"], list):
        raise ValueError("Rubric must include a list field named 'checks'.")

    return rubric


def extract_twb_xml(package_path: Path) -> str:
    with zipfile.ZipFile(package_path, "r") as zf:
        twb_candidates = [name for name in zf.namelist() if name.lower().endswith(".twb")]
        if not twb_candidates:
            raise ValueError("No .twb workbook found inside packaged workbook.")

        with zf.open(twb_candidates[0], "r") as twb_file:
            return twb_file.read().decode("utf-8", errors="replace")


def build_workbook_index(twb_xml: str) -> WorkbookIndex:
    root = ET.fromstring(twb_xml)

    worksheets: set[str] = set()
    dashboards: set[str] = set()
    datasources: set[str] = set()
    fields: set[str] = set()
    calculations: List[str] = []

    for elem in root.iter():
        tag = elem.tag.lower()

        if tag.endswith("worksheet"):
            name = elem.attrib.get("name")
            if name:
                worksheets.add(name)

        if tag.endswith("dashboard"):
            name = elem.attrib.get("name")
            if name:
                dashboards.add(name)

        if tag.endswith("datasource"):
            caption = elem.attrib.get("caption")
            name = elem.attrib.get("name")
            if caption:
                datasources.add(caption)
            if name:
                datasources.add(name)

        if tag.endswith("column"):
            caption = elem.attrib.get("caption")
            name = elem.attrib.get("name")
            if caption:
                fields.add(caption)
            if name:
                fields.add(name)

        formula = elem.attrib.get("formula")
        if formula:
            calculations.append(formula)

    return WorkbookIndex(
        worksheets=worksheets,
        dashboards=dashboards,
        datasources=datasources,
        fields=fields,
        calculations=calculations,
        workbook_text=twb_xml,
    )


def contains_value(haystack: str, needle: str, case_sensitive: bool) -> bool:
    if case_sensitive:
        return needle in haystack
    return needle.lower() in haystack.lower()


def evaluate_check(check: Dict, index: WorkbookIndex) -> bool:
    check_type = check.get("type")
    case_sensitive = bool(check.get("case_sensitive", False))

    if check_type == "worksheet_exists":
        target = str(check.get("worksheet", ""))
        values = index.worksheets if case_sensitive else {v.lower() for v in index.worksheets}
        return target in values if case_sensitive else target.lower() in values

    if check_type == "dashboard_exists":
        target = str(check.get("dashboard", ""))
        values = index.dashboards if case_sensitive else {v.lower() for v in index.dashboards}
        return target in values if case_sensitive else target.lower() in values

    if check_type == "datasource_exists":
        target = str(check.get("datasource", ""))
        values = index.datasources if case_sensitive else {v.lower() for v in index.datasources}
        return target in values if case_sensitive else target.lower() in values

    if check_type == "field_exists":
        target = str(check.get("field", ""))
        values = index.fields if case_sensitive else {v.lower() for v in index.fields}
        return target in values if case_sensitive else target.lower() in values

    if check_type == "calculation_contains":
        needle = str(check.get("contains", ""))
        return any(contains_value(formula, needle, case_sensitive) for formula in index.calculations)

    if check_type == "workbook_text_contains":
        needle = str(check.get("contains", ""))
        return contains_value(index.workbook_text, needle, case_sensitive)

    if check_type == "workbook_text_not_contains":
        needle = str(check.get("contains", ""))
        return not contains_value(index.workbook_text, needle, case_sensitive)

    if check_type == "all_of":
        subchecks = check.get("checks", [])
        return all(evaluate_check(subcheck, index) for subcheck in subchecks)

    if check_type == "any_of":
        subchecks = check.get("checks", [])
        return any(evaluate_check(subcheck, index) for subcheck in subchecks)

    raise ValueError(f"Unsupported check type: {check_type}")


def grade_submission(package_path: Path, rubric: Dict) -> Tuple[float, List[CheckResult], float]:
    checks = rubric["checks"]
    total_points = float(rubric.get("total_points", sum(float(c.get("points", 0)) for c in checks)))

    twb_xml = extract_twb_xml(package_path)
    index = build_workbook_index(twb_xml)

    results: List[CheckResult] = []
    score = 0.0

    for check in checks:
        points = float(check.get("points", 0))
        passed = evaluate_check(check, index)
        if passed:
            score += points

        results.append(
            CheckResult(
                check_id=str(check.get("id", "")),
                description=str(check.get("description", "")),
                points=points,
                passed=passed,
            )
        )

    return score, results, total_points


def get_student_name(filename: str) -> str:
    return Path(filename).stem


def write_results(rows: List[Dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "student",
        "file",
        "filename_valid",
        "score",
        "total_points",
        "percent",
        "missed_points",
        "missed_checks",
        "passed_checks",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def list_submission_files(folder: Path, extensions: List[str]) -> List[Path]:
    accepted = {ext.lower().strip() for ext in extensions if ext.strip()}
    all_files = [p for p in folder.iterdir() if p.is_file()]
    return sorted([p for p in all_files if p.suffix.lower() in accepted])


def main() -> None:
    args = parse_args()
    rubric = read_rubric(args.rubric)

    if not args.submissions.exists():
        raise FileNotFoundError(f"Submissions folder not found: {args.submissions}")

    extensions = [e.strip() for e in args.extensions.split(",") if e.strip()]
    filename_regex = re.compile(args.filename_regex) if args.filename_regex else None

    rows: List[Dict[str, str]] = []
    files = list_submission_files(args.submissions, extensions)

    for path in files:
        student = get_student_name(path.name)
        filename_valid = bool(filename_regex.match(path.name)) if filename_regex else True

        try:
            score, results, total_points = grade_submission(path, rubric)
            missed = [r for r in results if not r.passed]
            passed = [r for r in results if r.passed]

            missed_points = sum(r.points for r in missed)
            percent = (score / total_points * 100.0) if total_points else 0.0

            rows.append(
                {
                    "student": student,
                    "file": path.name,
                    "filename_valid": str(filename_valid),
                    "score": f"{score:.2f}",
                    "total_points": f"{total_points:.2f}",
                    "percent": f"{percent:.2f}",
                    "missed_points": f"{missed_points:.2f}",
                    "missed_checks": " | ".join(
                        f"{m.check_id}:{m.description} (-{m.points:g})" for m in missed
                    ),
                    "passed_checks": " | ".join(p.check_id for p in passed),
                }
            )
        except Exception as exc:
            total_points = float(rubric.get("total_points", 25))
            rows.append(
                {
                    "student": student,
                    "file": path.name,
                    "filename_valid": str(filename_valid),
                    "score": "0.00",
                    "total_points": f"{total_points:.2f}",
                    "percent": "0.00",
                    "missed_points": f"{total_points:.2f}",
                    "missed_checks": f"ERROR: {exc}",
                    "passed_checks": "",
                }
            )

    write_results(rows, args.output)
    print(f"Graded {len(rows)} submission(s). Results written to: {args.output}")


if __name__ == "__main__":
    main()
