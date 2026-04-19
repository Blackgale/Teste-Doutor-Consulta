from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dados" / "commodities_sample.csv"
CHARTS_DIR = BASE_DIR / "graficos"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values(["commodity", "date"]).reset_index(drop=True)


def build_metrics(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["daily_return_pct"] = result.groupby("commodity")["price_usd_ton"].pct_change() * 100
    result["ma_7"] = result.groupby("commodity")["price_usd_ton"].transform(lambda s: s.rolling(7, min_periods=1).mean())
    result["ma_30"] = result.groupby("commodity")["price_usd_ton"].transform(lambda s: s.rolling(30, min_periods=1).mean())
    result["ret_7d_pct"] = result.groupby("commodity")["price_usd_ton"].pct_change(7) * 100
    result["ret_30d_pct"] = result.groupby("commodity")["price_usd_ton"].pct_change(30) * 100
    return result


def build_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    latest = metrics.sort_values("date").groupby("commodity").tail(1).copy()
    vol = (
        metrics.groupby("commodity")["daily_return_pct"]
        .std()
        .mul((252 ** 0.5))
        .rename("annualized_volatility_pct")
        .reset_index()
    )
    summary = latest.merge(vol, on="commodity", how="left")
    summary = summary[
        [
            "commodity",
            "date",
            "price_usd_ton",
            "ret_7d_pct",
            "ret_30d_pct",
            "ma_7",
            "ma_30",
            "annualized_volatility_pct",
        ]
    ].sort_values("annualized_volatility_pct", ascending=False)
    return summary.round(2)


def plot_price_series(metrics: pd.DataFrame, out_path: Path) -> None:
    plt.figure(figsize=(11, 6))
    for commodity, group in metrics.groupby("commodity"):
        plt.plot(group["date"], group["price_usd_ton"], label=commodity, linewidth=2)
    plt.title("Preço por tonelada — séries históricas")
    plt.xlabel("Data")
    plt.ylabel("USD / ton")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()


def plot_indexed_series(metrics: pd.DataFrame, out_path: Path) -> None:
    indexed = metrics.copy()
    indexed["base_100"] = indexed.groupby("commodity")["price_usd_ton"].transform(lambda s: s / s.iloc[0] * 100)
    plt.figure(figsize=(11, 6))
    for commodity, group in indexed.groupby("commodity"):
        plt.plot(group["date"], group["base_100"], label=commodity, linewidth=2)
    plt.title("Comparação indexada (base 100)")
    plt.xlabel("Data")
    plt.ylabel("Índice")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()


def export_summary(summary: pd.DataFrame, out_path: Path) -> None:
    out_path.write_text(summary.to_markdown(index=False), encoding="utf-8")


def generate_insights(summary: pd.DataFrame) -> str:
    most_volatile = summary.iloc[0]
    most_stable = summary.iloc[-1]
    strongest_30d = summary.sort_values("ret_30d_pct", ascending=False).iloc[0]
    weakest_30d = summary.sort_values("ret_30d_pct", ascending=True).iloc[0]

def main() -> None:
    CHARTS_DIR.mkdir(exist_ok=True, parents=True)
    metrics = build_metrics(load_data())
    summary = build_summary(metrics)

    plot_price_series(metrics, CHARTS_DIR / "price_series.png")
    plot_indexed_series(metrics, CHARTS_DIR / "indexed_series.png")
    summary.to_csv(BASE_DIR / "summary.csv", index=False)
    export_summary(summary, BASE_DIR / "summary.md")
    (BASE_DIR / "insights.txt").write_text(generate_insights(summary), encoding="utf-8")

    print("Análise concluída.")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
