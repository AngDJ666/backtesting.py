import pandas as pd

def load_and_merge_data():
    price_df = pd.read_csv("coinglass_data.csv")
    cq_df = pd.read_csv("cryptoQuant_data.csv")
    gn_df = pd.read_csv("glassNode_data.csv")

    price_df['Timestamp'] = pd.to_datetime(price_df['start_time'], unit='ms')
    cq_df['Timestamp'] = pd.to_datetime(cq_df['start_time'], unit='ms')
    gn_df['Timestamp'] = pd.to_datetime(gn_df['start_time'], unit='ms')

    price_df = price_df.rename(columns={'c': 'Close'})[['Timestamp', 'Close']]
    cq_df = cq_df.rename(columns={
        'inflow_mean': 'CQ_inflow_mean',
        'inflow_mean_ma7': 'CQ_inflow_mean_ma7',
        'inflow_total': 'CQ_inflow_total'
    })[['Timestamp', 'CQ_inflow_mean', 'CQ_inflow_mean_ma7', 'CQ_inflow_total']]
    gn_df = gn_df.rename(columns={'v': 'GN_metric'})[['Timestamp', 'GN_metric']]

    df = price_df.merge(cq_df, on='Timestamp', how='inner').merge(gn_df, on='Timestamp', how='inner')
    df.set_index('Timestamp', inplace=True)
    df['return'] = df['Close'].pct_change().fillna(0)

    return df


