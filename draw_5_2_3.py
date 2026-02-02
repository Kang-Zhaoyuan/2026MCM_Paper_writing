import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def build_weekly_accuracy(df):
	rename_map = {
		"赛季": "Season",
		"周数": "Week",
		"预测淘汰": "PredictedElim",
		"实际淘汰": "ActualElim",
	}
	df = df.rename(columns=rename_map)

	required_cols = {"Season", "Week", "PredictedElim", "ActualElim"}
	missing = required_cols - set(df.columns)
	if missing:
		raise ValueError(f"Missing columns: {missing}")

	# 逐行对比预测淘汰与实际淘汰
	df["IsCorrect"] = df["PredictedElim"] == df["ActualElim"]

	# 计算每周的估计精度：正确数目 / (正确数目 + 错误数目)
	weekly_accuracy_data = []
	for (season, week), group in df.groupby(["Season", "Week"]):
		correct_count = int(group["IsCorrect"].sum())
		incorrect_count = int((group["IsCorrect"] == False).sum())
		total = correct_count + incorrect_count
		accuracy = correct_count / total if total > 0 else 0
		weekly_accuracy_data.append({
			"Season": season,
			"Week": week,
			"accuracy": accuracy,
		})

	weekly_acc = pd.DataFrame(weekly_accuracy_data)
	return weekly_acc


def plot_accuracy_heatmap(csv_path, output_path):
	df = pd.read_csv(csv_path, encoding="utf-8-sig")
	weekly_acc = build_weekly_accuracy(df)

	seasons = sorted(weekly_acc["Season"].unique())
	max_week = int(weekly_acc["Week"].max())
	weeks = list(range(1, max_week + 1))

	heatmap_data = (
		weekly_acc.pivot(index="Season", columns="Week", values="accuracy")
		.reindex(index=seasons, columns=weeks)
	)

	mask = heatmap_data.isna()

	plt.figure(figsize=(12, 9))
	sns.heatmap(
		heatmap_data,
		mask=mask,
		cmap="YlGnBu",
		vmin=0,
		vmax=1,
		linewidths=0.3,
		linecolor="#f0f0f0",
		cbar_kws={"label": "Weekly accuracy"},
	)
	plt.title("Season-Week Prediction Accuracy", fontsize=13)
	plt.xlabel("Week")
	plt.ylabel("Season")
	plt.tight_layout()
	plt.savefig(output_path, dpi=300, bbox_inches="tight")
	plt.close()


def plot_binary_accuracy_heatmap(csv_path, output_path, threshold=0.75):
	df = pd.read_csv(csv_path, encoding="utf-8-sig")
	weekly_acc = build_weekly_accuracy(df)

	seasons = sorted(weekly_acc["Season"].unique())
	max_week = int(weekly_acc["Week"].max())
	weeks = list(range(1, max_week + 1))

	heatmap_data = (
		weekly_acc.pivot(index="Season", columns="Week", values="accuracy")
		.reindex(index=seasons, columns=weeks)
	)

	mask = heatmap_data.isna()
	# 二值化：>=阈值为1（深蓝），<阈值为0（浅蓝）
	binary_data = (heatmap_data >= threshold).astype(float)

	plt.figure(figsize=(12, 9))
	sns.heatmap(
		binary_data,
		mask=mask,
		cmap=sns.color_palette(["#a6cee3", "#1f78b4"], as_cmap=True),
		vmin=0,
		vmax=1,
		linewidths=0.3,
		linecolor="#f0f0f0",
		cbar_kws={"label": f"Accuracy >= {int(threshold*100)}%"},
	)
	plt.title("Season-Week Prediction Accuracy (Binary)", fontsize=13)
	plt.xlabel("Week")
	plt.ylabel("Season")
	plt.tight_layout()
	plt.savefig(output_path, dpi=300, bbox_inches="tight")
	plt.close()


if __name__ == "__main__":
	base_dir = os.path.dirname(__file__)
	csv_path = os.path.join(base_dir, "全赛季每周估计详情.csv")
	output_path = os.path.join(base_dir, "consistency_accuracy_heatmap.png")
	plot_accuracy_heatmap(csv_path, output_path)

	binary_output_path = os.path.join(base_dir, "consistency_accuracy_heatmap_binary.png")
	plot_binary_accuracy_heatmap(csv_path, binary_output_path, threshold=0.75)
