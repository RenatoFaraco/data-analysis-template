import os
import pandas as pd
from sqlalchemy import create_engine


def process_day(day_path):

    all_dfs = []
    day = os.path.basename(day_path)

    for rodadas in os.listdir(day_path):
        rodadas_path = os.path.join(day_path, rodadas)
        if not os.path.isdir(rodadas_path):
            continue

        for amostra in os.listdir(rodadas_path):
            amostra_path = os.path.join(rodadas_path, amostra)
            if not os.path.isdir(amostra_path):
                continue

            for fname in os.listdir(amostra_path):
                if not fname.lower().endswith('.txt'):
                    continue
                full_file = os.path.join(amostra_path, fname)
                try:
                    df = pd.read_csv(full_file, sep='\t', decimal=',', header=None)
                    df.columns = [
                        'wavelength',
                        'spectrum_1', # LPG inerte
                        'spectrum_2', # Interferômetro temp referencia
                        'spectrum_3', # LPG lactobacilos
                        'spectrum_4', # Interferômetro lactobacilos
                    ]
                    df['rodadas'] = rodadas
                    df['amostras'] = amostra
                    df['dia'] = day
                    all_dfs.append(df)
                except Exception as e:
                    print(f"[!] Falha ao ler/processar {full_file}: {e}")

    if not all_dfs:
        return None

    return pd.concat(all_dfs, ignore_index=True)


def main():
    base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'Bragg')
    day_path = day_path = os.path.join(base_path, '25_06_2025')

    output_db = os.path.join(base_path, 'espectros_braggmeter_dia_25_06_2025.db')
    engine = create_engine(f"sqlite:///{output_db}")

    df_day = process_day(day_path)

    df_day.to_sql(
        name='spectra',
        con=engine,
        if_exists='append',
        index=False,
        chunksize=100_000
    )
    print(f"  Inseridos {len(df_day)} linhas.")

    print(f"Concluído. Banco SQLite em: {output_db}")


if __name__ == '__main__':
    main()
