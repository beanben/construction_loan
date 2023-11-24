import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from construction_loan.cashflow import Cashflow

class DataVisualiser:
    def __init__(self):
        # Set display options in the constructor
        pd.options.display.float_format = '{:,.0f}'.format
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

    def display_dataframe(self, df):
        return df

    def plot_cost_summary(self, cashflow_instance):
        # Check if the provided object is an instance of Cashflow
        if not isinstance(cashflow_instance, Cashflow):
            raise TypeError("The provided object is not an instance of Cashflow")

        # Flatten the MultiIndex for easier handling
        df = cashflow_instance.df.copy()
        df.columns = [' '.join(map(str, col)).strip() for col in df.columns.values]

        # Create a line plot for each cost_type within each cost_category
        fig = go.Figure()
        for column in df.columns:
            cost_category, cost_type = column.split(' ', 1)
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df[column], 
                mode='lines+markers', 
                name=column, 
                hoverinfo='text',
                text=[f"{column}: {y}" for y in df[column]],
                line=dict(dash='solid' if cost_category == 'Acquisition costs' else 'dot')
            ))

        # Update layout for the graph
        fig.update_layout(
            title='Total Costs by Category and Period',
            xaxis_title='Period',
            yaxis_title='Total Amount',
            legend=dict(
                orientation="v",  # Vertical orientation
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05  # Position the legend to the right of the plot
            ),
            autosize=True,
            width=1200,  # Adjust width to accommodate the legend
            height=600,
            margin=dict(l=10, r=10, t=40, b=40)  # Adjust right margin for legend
        )

        fig.show()

    def plot_cumulative_cost_summary(self, cashflow_instance):
        # Check if the provided object is an instance of Cashflow
        if not isinstance(cashflow_instance, Cashflow):
            raise TypeError("The provided object is not an instance of Cashflow")

        # Flatten the MultiIndex for easier handling
        df = cashflow_instance.df.copy()
        df.columns = [' '.join(map(str, col)).strip() for col in df.columns.values]

        # Calculate cumulative sum for each column
        cumulative_df = df.cumsum()

        # Create a stacked bar chart for each cost_type within each cost_category
        fig = go.Figure()
        for column in cumulative_df.columns:
            fig.add_trace(go.Bar(
                x=cumulative_df.index, 
                y=cumulative_df[column], 
                name=column,
                # text=[f"{column}: {y}" for y in cumulative_df[column]]
            ))

        # Update layout for the graph
        fig.update_layout(
            title='Cumulative Costs by Category and Period',
            xaxis_title='Period',
            yaxis_title='Cumulative Amount',
            barmode='stack',  # Stack bars for different cost types
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            ),
            autosize=True,
            width=1200,
            height=600,
            margin=dict(l=10, r=10, t=40, b=40)
        )

        fig.show()