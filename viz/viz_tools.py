import matplotlib.pyplot as plt
from collections import Counter
import os

def generate_summary_charts(
    real_energy,
    base_energy,
    arr_retained_real,
    arr_retained_base,
    real_churn,
    base_churn,
    penalty_tracker=None,
    annotations=None,
    churned_users=None,
    user_states=None,
    save=False,
    prefix="chart",
    dashboard=True
):
    """
    Generates a series of metric charts comparing the challenger (adaptive system)
    to the baseline (heuristic system).

    Chart outputs include:
    - Energy usage per batch
    - ARR retention over time
    - Churn rate over time
    - Penalty intensity (optional)
    - Churned archetype distribution (optional)
    - Composite dashboard (optional)

    Parameters:
        real_energy (list[float]): Energy used by challenger per batch
        base_energy (list[float]): Energy used by baseline per batch
        arr_retained_real (list[float]): ARR retained by challenger per batch
        arr_retained_base (list[float]): ARR retained by baseline per batch
        real_churn (list[float]): Churn ratio of challenger per batch
        base_churn (list[float]): Churn ratio of baseline per batch
        penalty_tracker (list[float], optional): Penalty score per batch
        annotations (list[tuple], optional): List of (batch_idx, label) tuples to annotate events
        churned_users (list, optional): Unused in current logic (placeholder)
        user_states (dict, optional): Unused in current logic (placeholder)
        save (bool): Whether to save the charts as PNGs
        prefix (str): Filename prefix for saved charts
        dashboard (bool): Whether to create a composite dashboard view
    """

    os.makedirs("output", exist_ok=True)
    figs = []

    # --- Energy Usage Chart ---
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    ax1.plot(real_energy, label="Challenger Energy", linewidth=2, alpha=0.4)
    ax1.plot(base_energy, label="Baseline Energy", linestyle="--", alpha=0.4)
    ax1.set_title("Energy Usage per Batch")
    ax1.set_xlabel("Batch")
    ax1.set_ylabel("kWh")
    ax1.grid(True)
    ax1.legend()
    figs.append(fig1)
    if save:
        fig1.savefig(f"{prefix}_energy.png", dpi=300)
    plt.close(fig1)

    # --- ARR Retention Chart ---
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.plot(arr_retained_real, label="Challenger", linewidth=2, alpha=0.6)
    ax2.plot(arr_retained_base, label="Baseline", linestyle="--", alpha=0.6)
    ax2.set_title("ARR Retention Over Time")
    ax2.set_xlabel("Batch")
    ax2.set_ylabel("ARR Retained ($)")
    ax2.grid(True)
    ax2.legend()
    figs.append(fig2)
    if save:
        fig2.savefig(f"{prefix}_arr.png", dpi=300)
    plt.close(fig2)

    # --- Churn Rate Chart ---
    fig3, ax3 = plt.subplots(figsize=(6, 3))
    ax3.plot(real_churn, label="Challenger Churn", linewidth=2, color='blue', alpha=0.6)
    ax3.plot(base_churn, label="Baseline Churn", linestyle="--", color='orange', alpha=0.6)
    if annotations:
        for batch_idx, label in annotations:
            ax3.axvline(x=batch_idx, color="gray", linestyle=":", alpha=0.6)
            ax3.text(batch_idx + 1, 0.05, label, rotation=90, fontsize=8, color="gray")
    ax3.set_title("Churn Rate Over Time")
    ax3.set_xlabel("Batch")
    ax3.set_ylabel("Churn Ratio")
    ax3.grid(True)
    ax3.legend()
    figs.append(fig3)
    if save:
        fig3.savefig(f"{prefix}_churn.png", dpi=300)
    plt.close(fig3)

    # --- Penalty Intensity Chart (if provided) ---
    if penalty_tracker:
        fig4, ax4 = plt.subplots(figsize=(6, 3))
        ax4.plot(penalty_tracker, label="Penalty Score", color='darkred')
        ax4.set_title("Intervention Penalty Intensity")
        ax4.set_xlabel("Batch")
        ax4.set_ylabel("Penalty")
        ax4.grid(True)
        figs.append(fig4)
        if save:
            fig4.savefig(f"{prefix}_penalty.png", dpi=300)
        plt.close(fig4)

    # --- (Optional) Additional chart logic could go here (e.g., churned archetypes) ---

    # --- Composite Dashboard ---
    if dashboard:
        total = len(figs)
        rows = (total + 1) // 2
        fig_dash, axes = plt.subplots(rows, 2, figsize=(12, 3.5 * rows))
        axes = axes.flatten()

        for idx, fig in enumerate(figs):
            tmp_ax = fig.get_axes()[0]
            new_ax = axes[idx]
            for line in tmp_ax.lines:
                new_ax.plot(
                    line.get_xdata(),
                    line.get_ydata(),
                    label=line.get_label(),
                    linestyle=line.get_linestyle()
                )
            new_ax.set_title(tmp_ax.get_title())
            new_ax.set_xlabel(tmp_ax.get_xlabel())
            new_ax.set_ylabel(tmp_ax.get_ylabel())
            new_ax.grid(True)
            new_ax.legend()

        for j in range(len(figs), len(axes)):
            fig_dash.delaxes(axes[j])  # Hide any unused subplot space

        fig_dash.tight_layout()
        fig_dash.savefig("output/dashboard.png", dpi=300)
        plt.close(fig_dash)


# Copyright 2025 Divine Comedy Labs LLC
# Released under the Polyform Noncommercial License 1.0.0
# See LICENSE or https://polyformproject.org/licenses/noncommercial/1.0.0/
