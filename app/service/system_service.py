import pandas as pd

from app.config import lifespan_log_conf


class LogService:

    @staticmethod
    def life_log_records():
        with open(lifespan_log_conf.file) as f:
            df_log = pd.DataFrame(data=[x.split('|') for x in f.readlines()],
                                  columns=['time', 'level', 'message'])

        for c in df_log.columns:
            df_log[c] = df_log[c].str.strip()

        return df_log.to_html(justify='left').replace('\\n', '<br/>')
