import pandas as pd
import matplotlib.pyplot as plt

class DataVisualiser:
    def __init__(self):
        # Set display options in the constructor
        pd.options.display.float_format = '{:,.0f}'.format
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

    def display_dataframe(self, df):
        return df

    @staticmethod
    def plot_graph(data):
        # Implement graph plotting logic
        plt.plot(data)
        plt.show()