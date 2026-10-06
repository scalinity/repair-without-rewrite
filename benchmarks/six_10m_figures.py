"""Plot all frozen DEVELOPMENT learning-curve endpoints from descriptive receipts."""
import argparse
import hashlib
import json
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


COLORS = {0.0001: "#195C5D", 0.0003: "#846B9C", 0.0006: "#B47B30"}
LR_LABELS = {0.0001: "1e-4", 0.0003: "3e-4", 0.0006: "6e-4"}
VIEWS = ["clean_preservation", "uniquely_recoverable_repair", "mixed_repair_preservation"]


def setup():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.labelcolor": "#1A1A1A", "text.color": "#1A1A1A",
        "xtick.color": "#736E67", "ytick.color": "#736E67",
        "grid.color": "#DFDAD1", "grid.linewidth": 0.6,
        "axes.facecolor": "#FCFCFB", "figure.facecolor": "#FCFCFB",
        "svg.hashsalt": "six10m-frozen-development-curves"})


def canvas(title):
    fig, axes = plt.subplots(2, 3, figsize=(12.8, 8.0), sharex=True)
    fig.suptitle(title, fontsize=15, x=0.06, ha="left", y=0.97)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.86, bottom=0.20, hspace=0.38, wspace=0.27)
    for axis in axes.flat:
        axis.grid(axis="y")
        axis.set_axisbelow(True)
        axis.set_xticks([0, 1.017149, 3.018478, 6.693230, 9.350642, 10.007223])
        axis.set_xticklabels(["0", "1.02", "3.02", "6.69", "9.35", "10.01"], rotation=45, ha="right")
    for axis in axes[-1]:
        axis.set_xlabel("Actual canonical exposures (millions)")
    return fig, axes


def save(fig, directory, stem, caption, files):
    caption = "\n".join(textwrap.fill(line, width=140) for line in caption.splitlines())
    fig.text(0.06, 0.045, caption, ha="left", va="bottom", fontsize=8, color="#736E67")
    for suffix in ("svg", "png"):
        path = directory / f"{stem}_V2.{suffix}"
        if path.exists():
            raise ValueError(f"figure already exists: {path}")
        fig.savefig(path, dpi=180, metadata={"Creator": "Repair Without Rewrite", "Date": None} if suffix == "svg" else None)
        files.append(str(path))
    plt.close(fig)


def figures(data, directory):
    expected = {f"{arm}-seed42-lr{lr}" for arm in ("B100", "C101") for lr in ("1e-04", "3e-04", "6e-04")}
    if len(data["outcomes"]) != 6 or {item["recipe_id"] for item in data["outcomes"]} != expected:
        raise ValueError("figures require all six prescribed outcomes")
    setup()
    directory.mkdir(parents=True, exist_ok=True)
    files = []
    fig, axes = canvas("Natural DEVELOPMENT · repair, introduced errors and WER")
    for row, arm in enumerate(("B100", "C101")):
        for outcome in data["outcomes"]:
            if outcome["arm"] != arm:
                continue
            points = outcome["learning_curve"]
            x = [point["actual_endpoint"]["canonical_exposure"] / 1e6 for point in points]
            color, label = COLORS[outcome["peak_lr"]], LR_LABELS[outcome["peak_lr"]]
            natural = [point["natural"] for point in points]
            axes[row, 0].plot(x, [value["wer"] * 100 for value in natural], "o-", color=color, label=label, markersize=3)
            for column, field, scale in ((1, "introduced", 100 / 2270), (2, "completed_repair", 1)):
                lower = [value[field][0] * scale for value in natural]
                upper = [value[field][1] * scale for value in natural]
                axes[row, column].plot(x, lower, "o-", color=color, label=label, markersize=3)
                axes[row, column].fill_between(x, lower, upper, color=color, alpha=0.16)
        axes[row, 0].axhline(64 / 2270 * 100, color="#736E67", linestyle="--", linewidth=1, label="RAW")
        axes[row, 0].set_yscale("symlog", linthresh=1)
        axes[row, 1].set_yscale("symlog", linthresh=1)
        for column in (0, 1):
            axes[row, column].set_yticks([0, 1, 3, 10, 100, 1000])
            axes[row, column].set_yticklabels(["0", "1", "3", "10", "100", "1,000"])
        for column, title in enumerate(("Failure-inclusive WER (%)", "Introduced error bounds (%)", "Completed repair bounds (count)")):
            axes[row, column].set_title(f"{arm} · {title}", loc="left", fontsize=10)
            axes[row, column].legend(frameon=False, fontsize=8)
            axes[row, column].set_ylim(bottom=0)
    save(fig, directory, "SIX_10M_NATURAL_CURVES",
        "108 natural cases; 2,270 reference words. All failures retained. Bounds are scorer correspondence bounds, not confidence intervals.\n"
        "WER and introduced-error axes are linear through 1%, logarithmic above 1%. Points are the six frozen completed-update endpoints.", files)

    fig, axes = canvas("Generated DEVELOPMENT · whole-case conformance by frozen view")
    view_titles = ["Clean preservation", "Required repair", "Mixed repair + preservation"]
    for row, arm in enumerate(("B100", "C101")):
        for outcome in data["outcomes"]:
            if outcome["arm"] != arm:
                continue
            points = outcome["learning_curve"]
            x = [point["actual_endpoint"]["canonical_exposure"] / 1e6 for point in points]
            for column, view in enumerate(VIEWS):
                values = [point["generated"]["by_view"][view] for point in points]
                axes[row, column].plot(x, [value["conformant"] / value["cases"] * 100 for value in values], "o-",
                    color=COLORS[outcome["peak_lr"]], label=LR_LABELS[outcome["peak_lr"]], markersize=3)
        for column, title in enumerate(view_titles):
            axes[row, column].set_title(f"{arm} · {title}", loc="left", fontsize=10)
            axes[row, column].set_ylim(-2, 102)
            axes[row, column].set_ylabel("Conformant cases (%)")
            axes[row, column].legend(frameon=False, fontsize=8)
    save(fig, directory, "SIX_10M_GENERATED_CURVES",
        "96 cases per view; 288 generated cases total. Whole-case conformance includes all required repair and preservation fields.\n"
        "A genuine required-repair case can pass the eligibility repair condition without whole-case conformance. Natural denominators remain separate.", files)

    fig, axes = canvas("DEVELOPMENT · source identity and retained output failures")
    for row, arm in enumerate(("B100", "C101")):
        for outcome in data["outcomes"]:
            if outcome["arm"] != arm:
                continue
            points = outcome["learning_curve"]
            x = [point["actual_endpoint"]["canonical_exposure"] / 1e6 for point in points]
            color, label = COLORS[outcome["peak_lr"]], LR_LABELS[outcome["peak_lr"]]
            axes[row, 0].plot(x, [point["natural"]["source_lexical_identity"] / 108 * 100 for point in points], "o-", color=color, label=label, markersize=3)
            axes[row, 1].plot(x, [point["natural"]["invalid_or_incomplete"] for point in points], "o-", color=color, label=label, markersize=3)
            axes[row, 2].plot(x, [point["generated"]["invalid_or_incomplete"] for point in points], "o-", color=color, label=label + " all", markersize=3)
            axes[row, 2].plot(x, [point["generated"]["decoder_invalid_or_incomplete"] for point in points], "--", color=color, label=label + " decoder", linewidth=1)
        for column, title in enumerate(("Natural source lexical identity (%)", "Natural invalid / incomplete (count)", "Generated invalid / incomplete (count)")):
            axes[row, column].set_title(f"{arm} · {title}", loc="left", fontsize=10)
            axes[row, column].set_ylim(bottom=0, top=102 if column == 0 else 110 if column == 1 else 296)
            axes[row, column].legend(frameon=False, fontsize=7, ncol=2 if column == 2 else 1)
    save(fig, directory, "SIX_10M_IDENTITY_FAILURE_CURVES",
        "Identity counts require complete valid output. Natural denominator: 108; generated denominator: 288.\n"
        "Generated solid lines include structural grammar failures; dashed lines show decoder incompleteness alone. Every frozen case remains in the totals.", files)
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tables", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    arguments = parser.parse_args()
    data = json.loads(arguments.tables.read_text())
    files = figures(data, arguments.directory)
    def sha(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    receipt = {"tables_path": str(arguments.tables), "tables_sha256": sha(arguments.tables),
        "figure_helper_sha256": sha(Path(__file__)), "campaign_sha256": data["campaign_sha256"],
        "figures_sha256": {path: sha(path) for path in files}, "disposition": data["disposition"]}
    with arguments.receipt.open("x") as stream:
        stream.write(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"figures": files, "disposition": data["disposition"]}))
