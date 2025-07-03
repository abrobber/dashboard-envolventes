def detectar_envolventes(df):
    df['alcista'] = (
        (df['close'] > df['open']) &
        (df['open'].shift(1) > df['close'].shift(1)) &
        (df['close'] > df['open'].shift(1)) &
        (df['open'] < df['close'].shift(1))
    )
    df['bajista'] = (
        (df['close'] < df['open']) &
        (df['open'].shift(1) < df['close'].shift(1)) &
        (df['close'] < df['open'].shift(1)) &
        (df['open'] > df['close'].shift(1))
    )
    return df
