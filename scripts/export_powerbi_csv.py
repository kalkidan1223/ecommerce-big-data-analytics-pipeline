from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "processed" / "analytics.duckdb"
OUTPUT_DIR = PROJECT_ROOT / "data" / "powerbi"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(DB_PATH), read_only=True) as con:
        tables = [row[0] for row in con.sql("show tables").fetchall()]
        for table in tables:
            output_path = OUTPUT_DIR / f"{table}.csv"
            con.table(table).df().to_csv(output_path, index=False)
            row_count = con.table(table).count("*").fetchone()[0]
            print(f"exported {table}: {row_count} rows -> {output_path}")


if __name__ == "__main__":
    main()
