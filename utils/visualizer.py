# data_analysis_app/utils/visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    @staticmethod
    def bar_chart(data, x, y, title=None):
        plt.figure(figsize=(10, 6))
        sns.barplot(x=x, y=y, data=data)
        if title:
            plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt

    @staticmethod
    def line_chart(data, x, y, title=None):
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=x, y=y, data=data)
        if title:
            plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt

    @staticmethod
    def scatter_plot(data, x, y, title=None):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=x, y=y, data=data)
        if title:
            plt.title(title)
        plt.tight_layout()
        return plt

    @staticmethod
    def histogram(data, column, bins=30, title=None):
        plt.figure(figsize=(10, 6))
        sns.histplot(data=data, x=column, bins=bins)
        if title:
            plt.title(title)
        plt.tight_layout()
        return plt

    @staticmethod
    def heatmap(data, title=None):
        plt.figure(figsize=(12, 10))
        sns.heatmap(data, annot=True, cmap='coolwarm')
        if title:
            plt.title(title)
        plt.tight_layout()
        return plt
