def cuerpo_dominante(df, idx, umbral=0.7):
    o, h, l, c = df.loc[idx, ['open', 'high', 'low', 'close']]
    cuerpo = abs(c - o)
    rango = h - l
    return (rango > 0) and (cuerpo / rango >= umbral)

def detectar_patron_5velas(df):
    df['prediccion_sexta'] = None
    for i in range(4, len(df) - 1):
        indices = [i-4, i-3, i-2, i-1, i]
        if not all(cuerpo_dominante(df, j) for j in indices):
            continue
        colores = ['verde' if df.loc[j, 'close'] > df.loc[j, 'open'] else 'roja' for j in indices]
        if colores == ['roja', 'verde', 'roja', 'verde', 'roja']:
            df.loc[i+1, 'prediccion_sexta'] = 'CALL'
        elif colores == ['verde', 'roja', 'verde', 'roja', 'verde']:
            df.loc[i+1, 'prediccion_sexta'] = 'PUT'
    return df


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
