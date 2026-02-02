import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, RegularPolygon


def add_box(ax, center, text, width=3.6, height=0.8):
	x, y = center
	box = FancyBboxPatch(
		(x - width / 2, y - height / 2),
		width,
		height,
		boxstyle="round,pad=0.02",
		linewidth=1.2,
		edgecolor="#2c3e50",
		facecolor="#ecf0f1",
	)
	ax.add_patch(box)
	ax.text(x, y, text, ha="center", va="center", fontsize=9)


def add_diamond(ax, center, text, size=0.75):
	x, y = center
	diamond = RegularPolygon(
		(x, y),
		numVertices=4,
		radius=size,
		orientation=0.785398,
		linewidth=1.2,
		edgecolor="#2c3e50",
		facecolor="#fef9e7",
	)
	ax.add_patch(diamond)
	ax.text(x, y, text, ha="center", va="center", fontsize=9)


def add_arrow(ax, start, end, text=None):
	ax.annotate(
		"",
		xy=end,
		xytext=start,
		arrowprops=dict(arrowstyle="->", color="#2c3e50", lw=1.1),
	)
	if text:
		mx = (start[0] + end[0]) / 2
		my = (start[1] + end[1]) / 2
		ax.text(mx, my, text, ha="center", va="center", fontsize=8)


def draw_flowchart(output_path="q1_workflow_flowchart.png"):
	fig, ax = plt.subplots(figsize=(8, 13))
	ax.set_xlim(0, 10)
	ax.set_ylim(0, 22)
	ax.axis("off")

	nodes = {
		"config": (5, 21),
		"load_data": (5, 19.6),
		"season_loop": (5, 18.2),
		"check_skip": (5, 16.8),
		"single_season": (5, 15.1),
		"sim_loop": (5, 13.6),
		"week_loop": (5, 12.0),
		"simulate_votes": (5, 10.4),
		"eliminate": (5, 8.8),
		"accuracy_check": (5, 7.2),
		"store_valid": (5, 5.6),
		"no_valid": (1.8, 6.2),
		"best_model": (5, 4.2),
		"metrics": (5, 2.7),
		"season_outputs": (5, 1.2),
		"summary": (5, 0.2),
	}

	add_box(ax, nodes["config"], "Load config parameters")
	add_box(ax, nodes["load_data"], "Read weekly_modeling_data.csv")
	add_box(ax, nodes["season_loop"], "Loop seasons")
	add_diamond(ax, nodes["check_skip"], "Skip\nexisting?")
	add_box(ax, nodes["single_season"], "Prepare season data & rule type")
	add_box(ax, nodes["sim_loop"], "Monte Carlo loop")
	add_box(ax, nodes["week_loop"], "Loop weeks")
	add_box(ax, nodes["simulate_votes"], "Compute votes & shares")
	add_box(ax, nodes["eliminate"], "Apply elimination rule")
	add_diamond(ax, nodes["accuracy_check"], "Accuracy\n¡Ý threshold?")
	add_box(ax, nodes["store_valid"], "Store valid model")
	add_box(ax, nodes["no_valid"], "No valid model\n¡ú skip season", width=2.6, height=0.9)
	add_box(ax, nodes["best_model"], "Select best model")
	add_box(ax, nodes["metrics"], "Build tables & metrics")
	add_box(ax, nodes["season_outputs"], "Save season CSV & plots")
	add_box(ax, nodes["summary"], "Season summary & final report", width=4.2, height=0.9)

	add_arrow(ax, nodes["config"], nodes["load_data"])
	add_arrow(ax, nodes["load_data"], nodes["season_loop"])
	add_arrow(ax, nodes["season_loop"], nodes["check_skip"])
	add_arrow(ax, nodes["check_skip"], nodes["single_season"], text="No")
	add_arrow(ax, (3.2, 16.8), nodes["season_loop"], text="Yes")

	add_arrow(ax, nodes["single_season"], nodes["sim_loop"])
	add_arrow(ax, nodes["sim_loop"], nodes["week_loop"])
	add_arrow(ax, nodes["week_loop"], nodes["simulate_votes"])
	add_arrow(ax, nodes["simulate_votes"], nodes["eliminate"])
	add_arrow(ax, nodes["eliminate"], nodes["accuracy_check"])
	add_arrow(ax, nodes["accuracy_check"], nodes["store_valid"], text="Yes")
	add_arrow(ax, nodes["accuracy_check"], nodes["no_valid"], text="No")
	add_arrow(ax, nodes["store_valid"], nodes["sim_loop"])

	add_arrow(ax, nodes["no_valid"], nodes["season_loop"])
	add_arrow(ax, nodes["store_valid"], nodes["best_model"])
	add_arrow(ax, nodes["best_model"], nodes["metrics"])
	add_arrow(ax, nodes["metrics"], nodes["season_outputs"])
	add_arrow(ax, nodes["season_outputs"], nodes["summary"])
	add_arrow(ax, nodes["summary"], nodes["season_loop"])

	plt.tight_layout()
	plt.savefig(output_path, dpi=300, bbox_inches="tight")
	plt.close(fig)


if __name__ == "__main__":
	draw_flowchart()
