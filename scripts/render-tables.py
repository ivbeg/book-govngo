#!/usr/bin/env python3
"""Render the two manuscript tables from data/*.csv into appendix chapters.

Edit the CSV, then run this script from the repository root. Do not keep a
second copy of the numbers in a finance chapter.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
APPENDICES = ROOT / "docs" / "09-appendices"

NAME_FIXES = {
    "Ненецкий-автономный округ": "Ненецкий автономный округ",
    "Республика Северная-Осетия Алания": "Республика Северная Осетия — Алания",
}


def comma(value: str, digits: int = 2) -> str:
    if value == "":
        return ""
    return f"{float(value):.{digits}f}".replace(".", ",")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def repair_federal(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    repaired = []
    for row in rows:
        name = row["name"]
        if name.startswith('АНО "Национальное агентство развития квалификаций') and not name.endswith('"'):
            name = name + '"'
        category = row["category"].replace("Иcтория", "История")
        repaired.append({**row, "name": name, "category": category})
    return repaired


def repair_regions(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [{**row, "region": NAME_FIXES.get(row["region"], row["region"])} for row in rows]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def render_federal(rows: list[dict[str, str]]) -> str:
    total = sum(float(row["amount_billion_rub"]) for row in rows)
    body = markdown_table(
        ["№", "Название", "Сумма, млрд руб.", "Доля, %", "Категория"],
        [
            [
                str(index),
                row["name"].replace("|", "\\|"),
                comma(row["amount_billion_rub"]),
                comma(row["share_of_nko_subsidies_percent"]),
                row["category"],
            ]
            for index, row in enumerate(rows, start=1)
        ],
    )
    return f"""# Крупнейшие получатели субсидий из федерального бюджета, 2019

Единственная копия списка. Глава о [федеральном бюджете](../06-finance/02-federal.md) на эту таблицу ссылается и свою не держит.

:::note
Источник рукописи: Единый портал бюджетной системы Минфина России, [budget.gov.ru](https://budget.gov.ru/). Машиночитаемая копия — `data/federal-top-2019.csv`. Сумма строк — {comma(str(total))} млрд руб.
:::

В прежней главе часть сумм была округлена иначе, чем в приложении: 8 вместо 8,01, 0,85 вместо 0,86. Ниже оставлена более подробная версия приложения. Категории взяты оттуда же. Это метки рукописи, не поле бюджетной росписи.

{body}

Две правки относительно исходной таблицы: в категории «История» латинская «c» заменена на кириллическую, у АНО «Национальное агентство развития квалификаций» закрыта кавычка в названии.

## Источники

[budget.gov.ru](https://budget.gov.ru/), как указано в прежнем приложении 1. Дата выгрузки в рукописи не проставлена.
"""


def render_regions(rows: list[dict[str, str]]) -> str:
    total = sum(float(row["amount_billion_rub"]) for row in rows)
    share_all = [float(row["share_of_all_regional_nko_subsidies_percent"]) for row in rows]
    shares = [float(row["share_of_region_budget_percent"]) for row in rows]
    share_all_sum = sum(share_all)
    mean_budget = sum(shares) / len(shares)
    body = markdown_table(
        [
            "Регион",
            "Сумма, млрд руб.",
            "Доля субъекта в сумме субсидий НКО всех субъектов, %",
            "Доля субсидий НКО в расходах бюджета субъекта, %",
        ],
        [
            [
                row["region"],
                comma(row["amount_billion_rub"]),
                comma(row["share_of_all_regional_nko_subsidies_percent"]),
                comma(row["share_of_region_budget_percent"]),
            ]
            for row in rows
        ],
    )
    return f"""# Субсидии НКО в бюджетах субъектов, 2019

:::note
Источник рукописи: отчёты об исполнении консолидированных бюджетов субъектов, Федеральное казначейство, [roskazna.ru](https://roskazna.ru/). Машиночитаемая копия — `data/regions-2019.csv`.
:::

Сумма столбца сумм — {comma(str(total))} млрд руб. Это та же величина, которую глава о [региональных бюджетах](../06-finance/03-regional.md) округляет до «более 349 миллиардов».

Столбец доли субъекта в общей сумме субсидий в сумме даёт {comma(str(share_all_sum))}%. Расхождение с 100% — округление строк. В старой таблице последняя строка называлась «ИТОГО СРЕДНЕЕ» и содержала 1,18 в этом столбце. 1,18 — это 100 / 85, среднее арифметическое долей, а не итог. Строка убрана, чтобы её не читали как сумму.

В соседнем столбце старая строка содержала 1,34. Среднее арифметическое доли субсидий НКО в бюджете субъекта по этим 85 строкам — {comma(str(mean_budget))}%. Глава использует 1,34% и как долю всех расходов консолидированных бюджетов. Оба смысла сохранены в главе, в таблицу среднее не подставлено вместо суммы.

Два названия исправлены при переносе: «Ненецкий-автономный округ» и «Республика Северная-Осетия Алания».

{body}

## Источники

[roskazna.ru](https://roskazna.ru/). Дата выгрузки в рукописи не проставлена. Расхождения Москвы, ЯНАО и ограничения Татарстана объяснены в главе, не в этой таблице.
"""


def main() -> None:
    federal_path = DATA / "federal-top-2019.csv"
    federal_fields = [
        "name",
        "amount_billion_rub",
        "share_of_nko_subsidies_percent",
        "category",
    ]
    federal = repair_federal(read_rows(federal_path))
    write_csv(federal_path, federal_fields, federal)

    regions_path = DATA / "regions-2019.csv"
    region_fields = [
        "region",
        "amount_billion_rub",
        "share_of_all_regional_nko_subsidies_percent",
        "share_of_region_budget_percent",
    ]
    regions = repair_regions(read_rows(regions_path))
    write_csv(regions_path, region_fields, regions)

    (APPENDICES / "03-federal-top-2019.md").write_text(render_federal(federal))
    (APPENDICES / "05-regions-2019.md").write_text(render_regions(regions))


if __name__ == "__main__":
    main()
