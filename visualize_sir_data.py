import sys
import pandas as pd
import altair as alt

def visualize_sir_data(event):
    sir_data = pd.read_csv(f'{event}_sir_data.csv')

    sir_data['timestamp'] = pd.to_datetime(sir_data['timestamp'])

    chart = alt.Chart(sir_data).mark_line(point=True).encode(
        x=alt.X('timestamp:T', title='Time', axis=alt.Axis(grid=False)),
        y=alt.Y('value:Q', title='User count', axis=alt.Axis(grid=True)),
        color=alt.Color('variable:N', scale=alt.Scale(scheme='category10'), legend=alt.Legend(title="User States"))
    ).transform_fold(
        ['susceptible', 'infected', 'recovered'],
        as_=['variable', 'value']
    ).properties(
        title=f'SIR-like Graph for {event}',
        width=800,
        height=400
    ).configure_view(
        strokeWidth=0.5
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=14
    )

    chart.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python visualize_sir_data.py <event>')
    else:
        event = sys.argv[1]
        visualize_sir_data(event)
