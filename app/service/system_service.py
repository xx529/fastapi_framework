import pandas as pd
from app.config import log_conf
import re


class LogService:

    @staticmethod
    def life_log_records():
        # TODO 日志重写
        # with open(lifespan_log_conf.file) as f:
        #     df_log = pd.DataFrame(data=[x.split('|') for x in f.readlines()],
        #                           columns=['time', 'level', 'message'])
        #
        # for c in df_log.columns:
        #     df_log[c] = df_log[c].str.strip()
        #
        # return df_log.to_html(justify='left').replace('\\n', '<br/>')
        ...

    @staticmethod
    def request_log():
        with open(log_conf.file) as f:
            data = f.readlines()

        columns = ['date', 'time', 'name', 'PID', 'TID', 'level', 'file', 'delimiter', 'RID', 'type', 'message']

        data_ls = []
        for d in data:
            record = d.split()
            data_ls.append(record[:len(columns) - 1] + [' '.join(record[len(columns) - 1:])])

        df_log = pd.DataFrame(data_ls, columns=columns)
        df_log.drop('delimiter', axis=1, inplace=True)
        df_log['PID'] = df_log['PID'].apply(lambda x: re.search('\[PID:(\d+)\]', x).group(1))
        df_log['TID'] = df_log['TID'].apply(lambda x: re.search('\[TID:(\d+)\]', x).group(1))
        df_log['RID'] = df_log['RID'].apply(lambda x: re.search('\[RID:(.*)\]', x).group(1))
        df_log['type'] = df_log['type'].apply(lambda x: x[1:-1])
        df_log['level'] = df_log['level'].apply(lambda x: x[1:-1])
        df_log['file'] = df_log['file'].apply(lambda x: x[1:-1])
        df_log['datetime'] = pd.to_datetime(df_log['date'] + ' ' + df_log['time'])

        df_request = df_log.sort_values('datetime', ascending=False).query('type != "lifespan"').groupby('RID').agg(
            start=pd.NamedAgg('datetime', 'min'),
            end=pd.NamedAgg('datetime', 'max'),
            state=pd.NamedAgg('message', 'first'),
        ).reset_index()

        df_request['duration'] = df_request[['end', 'start']].apply(lambda x: (x[0] - x[1]).seconds, axis=1)
        # df_request['code'] = df_request['state'].apply(lambda x: re.search('status code: (\d+)', x).group(1))

        return df_request.to_html(justify='left').replace('\\n', '<br/>')
