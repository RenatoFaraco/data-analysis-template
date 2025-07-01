import os
import time
from sqlalchemy import create_engine, text

base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'Bragg')
db_path   = os.path.join(base_path, 'comprimentos_de_onda_dia_25_06_2025.db')
engine    = create_engine(f"sqlite:///{db_path}")

def log_step(message, start_time):
    print(f"{message} — concluído em {time.time() - start_time:.2f} segundos.")

with engine.begin() as conn:
    print("Iniciando atualização do banco de dados...")
    
    t0 = time.time()
    try:
        conn.execute(text("ALTER TABLE resonance_summary RENAME COLUMN dia TO data;"))
        log_step("Coluna 'dia' renomeada para 'data'", t0)
    except Exception as e:
        print("Possivelmente já renomeada ou versão antiga do SQLite:", e)

    t1 = time.time()
    conn.execute(text("""
        UPDATE resonance_summary
        SET data = REPLACE(data, '_', '/');
    """))
    log_step("Atualização dos valores da coluna 'data'", t1)

    t2 = time.time()
    conn.execute(text("""
        UPDATE resonance_summary
        SET rodadas = 'Rodada ' || substr(rodadas, instr(rodadas, '_')+1);
    """))
    log_step("Atualização dos valores da coluna 'rodadas'", t2)

    t3 = time.time()
    try:
        conn.execute(text("ALTER TABLE resonance_summary ADD COLUMN conc_lactobacilos REAL;"))
        print("Coluna 'conc_lactobacilos' adicionada.")
    except Exception as e:
        print("Coluna 'conc_lactobacilos' já existe ou erro:", e)
        
    conn.execute(text("""
        UPDATE resonance_summary
        SET conc_lactobacilos = CASE amostras
            WHEN '0'   THEN '0.0'
            WHEN '1'  THEN '0.1'
            WHEN '2'  THEN '0.01'
            WHEN '3'  THEN '0.001'
            WHEN '4' THEN '0.0001'
            WHEN '5' THEN '0.00001'
            WHEN '6' THEN '0.000001'
            WHEN '7' THEN '0.0000001'
            ELSE NULL
        END;
    """))
    log_step("Coluna conc_lactobacilos preenchida", t3)

    t4 = time.time()
    try:
        conn.execute(text("ALTER TABLE resonance_summary ADD COLUMN temp_amostra REAL;"))
        print("Coluna 'temp_amostra' adicionada.")
    except Exception as e:
        print("Coluna 'temp_amostra' já existe ou erro:", e)

    conn.execute(text("""
        UPDATE resonance_summary
        SET temp_amostra = CASE amostras
            WHEN '0'   THEN '20.6'
            WHEN '1'   THEN '20.9'
            WHEN '2'  THEN '21.0'
            WHEN '3'  THEN '21.4'
            WHEN '4'  THEN '21.5'
            WHEN '5' THEN '21.2'
            WHEN '6' THEN '21.1'
            WHEN '7' THEN '21.2'
            ELSE NULL
        END;
    """))
    log_step("Coluna 'temp_amostra' preenchida", t4)

    t5 = time.time()
    try:
        conn.execute(text("ALTER TABLE resonance_summary ADD COLUMN temp_referencia REAL;"))
        print("Coluna 'temp_referencia' adicionada.")
    except Exception as e:
        print("Coluna 'temp_referencia' já existe ou erro:", e)

    conn.execute(text("""
        UPDATE resonance_summary
        SET temp_referencia = CASE amostras
            WHEN '0'   THEN '20.6'
            WHEN '1'   THEN '20.9'
            WHEN '2'  THEN '21.0'
            WHEN '3'  THEN '21.4'
            WHEN '4'  THEN '21.5'
            WHEN '5' THEN '21.2'
            WHEN '6' THEN '21.1'
            WHEN '7' THEN '21.2'
            ELSE NULL
        END;
    """))
    log_step("Coluna 'temp_referencia' preenchida", t5)
    
print(f"\n✅ Finalizado em {time.time() - t0:.2f} segundos.")
print("Banco de dados atualizado com sucesso!")