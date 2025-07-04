def cuerpo_dominante(df, idx, umbral=0.7):
    o, h, l, c = df.loc[idx, ['open', 'high', 'low', 'close']]
    cuerpo = abs(c - o)
    rango = h - l
    return (rango > 0) and (cuerpo / rango >= umbral)

def detectar_patron_5velas(df):
    df['prediccion_sexta'] = None
    rects = []
    secuencias = []

    for i in range(4, len(df) - 1):
        indices = [i - 4, i - 3, i - 2, i - 1, i]
        if not all(cuerpo_dominante(df, j) for j in indices):
            continue
        colores = ['verde' if df.loc[j, 'close'] > df.loc[j, 'open'] else 'roja' for j in indices]

        if colores == ['roja', 'verde', 'roja', 'verde', 'roja']:
            df.loc[i + 1, 'prediccion_sexta'] = 'CALL'
        elif colores == ['verde', 'roja', 'verde', 'roja', 'verde']:
            df.loc[i + 1, 'prediccion_sexta'] = 'PUT'
        else:
            continue

        # Guardamos datos para visual y tabla
        rects.append({
            "x0": df.loc[i - 4, 'time'],
            "x1": df.loc[i, 'time'],
            "y0": df.loc[i - 4:i, 'low'].min(),
            "y1": df.loc[i - 4:i, 'high'].max()
        })
        secuencias.append({
            "Inicio": df.loc[i - 4, 'time'],
            "Predicción": df.loc[i + 1, 'time'],
            "Secuencia": ''.join(['🟢' if c == 'verde' else '🔴' for c in colores]),
            "Señal": df.loc[i + 1, 'prediccion_sexta']
        })

    return df, rects, pd.DataFrame(secuencias)



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
