"""CSV exports for the payroll office."""


def export_staff_csv(rows: list[dict]) -> str:
    columns = ["name", "shop", "contract_hours"]
    lines = [",".join(columns)]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            if "," in value or '"' in value:
                value = '"' + value.replace('"', '""') + '"'
            cells.append(value)
        lines.append(",".join(cells))
    return "\r\n".join(lines) + "\r\n"


def export_absences_csv(rows: list[dict]) -> str:
    columns = ["name", "from", "to", "reason"]
    lines = [",".join(columns)]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            if "," in value or '"' in value:
                value = '"' + value.replace('"', '""') + '"'
            cells.append(value)
        lines.append(",".join(cells))
    return "\r\n".join(lines) + "\r\n"
