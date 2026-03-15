#!/usr/bin/env python3
"""Generate publication-quality charts for the agents manual.
All charts: black/white, clean, Palatino-inspired, no color."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# Global style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.linewidth': 0.8,
    'axes.edgecolor': '#333',
    'axes.labelcolor': '#000',
    'xtick.color': '#333',
    'ytick.color': '#333',
    'grid.color': '#ddd',
    'grid.linewidth': 0.5,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'text.color': '#000',
})

# ============================================================
# Chart 1: Compounding Reliability Problem
# ============================================================
fig, ax = plt.subplots(figsize=(6, 3.5))

steps = np.arange(1, 31)
rates_95 = 0.95 ** steps * 100
rates_99 = 0.99 ** steps * 100
rates_90 = 0.90 ** steps * 100

ax.plot(steps, rates_95, 'k-', linewidth=2, label='95% per step', marker='o',
        markersize=3, markevery=2)
ax.plot(steps, rates_99, 'k--', linewidth=1.5, label='99% per step', marker='s',
        markersize=3, markevery=3)
ax.plot(steps, rates_90, 'k:', linewidth=1.5, label='90% per step', marker='^',
        markersize=3, markevery=3)

# Annotations
ax.annotate('Demo zone\n(3-5 steps)', xy=(4, 81), fontsize=8,
            ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#999'))
ax.annotate('Production zone\n(10-20 steps)', xy=(15, 50), fontsize=8,
            ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='#999'))

# Key points
for s, r in [(5, 0.95**5*100), (10, 0.95**10*100), (20, 0.95**20*100)]:
    ax.plot(s, r, 'ko', markersize=6, zorder=5)
    ax.annotate(f'{r:.0f}%', xy=(s, r), xytext=(s+1.2, r+3),
                fontsize=8, fontweight='bold')

ax.set_xlabel('Number of Agent Steps')
ax.set_ylabel('Overall Success Rate')
ax.set_xlim(1, 30)
ax.set_ylim(0, 105)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.grid(True, alpha=0.5)
ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
ax.set_title('Compounding Reliability: Why Demos Work but Deployments Fail',
             fontsize=11, fontweight='bold', pad=10)

plt.tight_layout()
plt.savefig('chart_reliability.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved chart_reliability.png")

# ============================================================
# Chart 2: Failure Rates Bar Chart
# ============================================================
fig, ax = plt.subplots(figsize=(6, 3))

categories = [
    'Enterprise AI pilots\nfailing to reach prod.',
    'Agentic tasks failing\non real CRM workflows',
    'Multi-agent pilots\nfailing within 6 months',
    'Devs slower when\nusing AI tools',
    'Orgs with agents\nin production',
]
values = [95, 75, 40, 19, 11]
sources = ['MIT/Fortune', 'Superface', 'Gartner', 'METR', 'Cleanlab']

bars = ax.barh(range(len(categories)), values, color='#333', height=0.6)

# Add value labels
for i, (v, s) in enumerate(zip(values, sources)):
    ax.text(v + 1.5, i, f'{v}%  ({s})', va='center', fontsize=8)

ax.set_yticks(range(len(categories)))
ax.set_yticklabels(categories, fontsize=8)
ax.set_xlim(0, 115)
ax.set_xlabel('Percentage', fontsize=9)
ax.set_title('The Agent Reality Gap (2025-2026)', fontsize=11, fontweight='bold', pad=10)
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('chart_failure_rates.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved chart_failure_rates.png")

# ============================================================
# Chart 3: Scaffolding vs Model (80/20)
# ============================================================
fig, ax = plt.subplots(figsize=(4, 2.5))

labels = ['Scaffolding\n(tools, eval, context,\nsafety, cost controls)', 'Model\n(LLM capability)']
sizes = [80, 20]
colors = ['#333', '#bbb']
explode = (0.03, 0)

wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                    autopct='%1.0f%%', startangle=90,
                                    explode=explode, textprops={'fontsize': 8})
for t in autotexts:
    t.set_fontsize(11)
    t.set_fontweight('bold')
    t.set_color('white')

ax.set_title('Where Agent Value Comes From', fontsize=10, fontweight='bold', pad=10)

plt.tight_layout()
plt.savefig('chart_scaffolding.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved chart_scaffolding.png")

# ============================================================
# Chart 4: Token Cost Explosion
# ============================================================
fig, ax = plt.subplots(figsize=(5, 3))

steps_tok = np.arange(1, 21)
# Each step adds ~5K tokens of tool output, context grows
context_per_step = np.cumsum(np.full(20, 5000))
# Cost per call = context_tokens * price (Sonnet: ~$3/M input)
cost_per_call = context_per_step * 3 / 1_000_000
cumulative_cost = np.cumsum(cost_per_call)

ax.fill_between(steps_tok, 0, context_per_step / 1000, alpha=0.2, color='#666')
ax.plot(steps_tok, context_per_step / 1000, 'k-', linewidth=2, label='Context size (K tokens)')

ax2 = ax.twinx()
ax2.plot(steps_tok, cumulative_cost * 100, 'k--', linewidth=1.5, label='Cumulative cost (cents)')

ax.set_xlabel('Agent Step Number')
ax.set_ylabel('Context Window (K tokens)')
ax2.set_ylabel('Cumulative Cost (cents)')
ax.set_title('Context Growth: Each Step Pays for All Previous Steps',
             fontsize=10, fontweight='bold', pad=10)

# Combined legend
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('chart_token_cost.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved chart_token_cost.png")

# ============================================================
# Chart 5: Tool Count vs Performance (Vercel data)
# ============================================================
fig, ax = plt.subplots(figsize=(4.5, 3))

tool_counts = [40, 20, 10, 8]
success_rates = [80, 85, 95, 100]
labels_t = ['Original\n(40 tools)', '20 tools', '10 tools', 'Final\n(8 tools)']

ax.plot(tool_counts, success_rates, 'k-o', linewidth=2, markersize=8)

for i, (tc, sr, lab) in enumerate(zip(tool_counts, success_rates, labels_t)):
    offset = (0, 8) if i < 3 else (0, -12)
    ax.annotate(f'{sr}%', xy=(tc, sr), xytext=(tc, sr + offset[1]/3),
                ha='center', fontsize=9, fontweight='bold')

ax.set_xlabel('Number of Tools')
ax.set_ylabel('Success Rate (%)')
ax.set_xlim(45, 3)
ax.set_ylim(70, 108)
ax.set_title('The Vercel Experiment: Fewer Tools = Better Performance',
             fontsize=10, fontweight='bold', pad=10)
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('chart_vercel_tools.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved chart_vercel_tools.png")

print("\nAll charts generated.")
