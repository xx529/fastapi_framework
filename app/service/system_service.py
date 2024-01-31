import json
from functools import lru_cache
from typing import List
from uuid import UUID

import pandas as pd
from pandas import DataFrame

from app.config import log_conf, project_dir
from app.schema.enum import LoggerTypeEnum


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
    @lru_cache
    def load_all_log() -> DataFrame:
        with open(log_conf.file) as f:
            df_raw = pd.DataFrame([json.loads(x)['record'] for x in f.readlines()])
        df_log = pd.DataFrame()
        df_log['datetime'] = pd.to_datetime(df_raw['time'].apply(lambda x: x['repr']))
        df_log['PID'] = df_raw['process'].apply(lambda x: f"{x['name']}({x['id']})")
        df_log['TID'] = df_raw['thread'].apply(lambda x: f"{x['name']}({x['id']})")
        df_log['level'] = df_raw['level'].apply(lambda x: x['name'])
        df_log['type'] = df_raw['extra'].apply(lambda x: x['type'])
        df_log['file'] = df_raw['file'].apply(lambda x: x['path'])
        df_log['file'] = df_log['file'].apply(lambda x: x.removeprefix(str(project_dir.root)))
        df_log['line'] = df_raw['line']
        df_log['request_id'] = df_raw['extra'].apply(lambda x: x['request_id'])
        df_log['message'] = df_raw['message']
        df_log['exception'] = df_raw['exception']
        return df_log

    @classmethod
    def runtime_log(cls, refresh: bool, request_id: UUID):
        if refresh:
            cls.load_all_log.cache_clear()

        df_log = cls.load_all_log()

        df_log = df_log[df_log['request_id'] == request_id.hex]
        df_log['duration'] = df_log['datetime'].diff().dt.total_seconds().fillna(0.0)

        total_duration = df_log['duration'].sum()
        df_log['proportion'] = df_log['duration'].apply(lambda x: f'{round(x/total_duration, 2)*100}%')
        return df_log.to_html(justify='left')

    @classmethod
    def request_log(cls, refresh: bool, method: List[str], code: List[int], url_match: str):
        # TODO exception 报错明细信息
        if refresh:
            cls.load_all_log.cache_clear()

        df_log = cls.load_all_log()
        cols = ['datetime', 'request_id', 'message', 'exception']

        df_start = df_log.query(f'type == "{LoggerTypeEnum.REQUEST_START.value}"')[cols]
        df_finish = df_log.query(f'type == "{LoggerTypeEnum.REQUEST_FINISH.value}"')[cols]

        df_request = pd.merge(df_start, df_finish, on='request_id', suffixes=('_start', '_finish'))
        df_request['duration(s)'] = (df_request['datetime_finish'] - df_request['datetime_start']).dt.total_seconds()
        df_request['code'] = df_request['message_finish'].apply(lambda x: int(x.removeprefix('status code: ')))
        df_request['exception'] = df_request['exception_finish'].apply(lambda x: x['type'] if x is not None else '')
        df_request['detail'] = df_request['exception_finish'].apply(lambda x: x['value'] if x is not None else '')
        df_request[['method', 'url']] = df_request[['message_start']].apply(
            lambda x: x['message_start'].split(), axis=1, result_type='expand'
        )
        print(df_request.columns)
        default_filter_urls = ['/openapi.json', 'docs', '/system/log']
        df_request = df_request[~df_request['url'].str.contains('|'.join(default_filter_urls))]

        if method:
            df_request = df_request[df_request['method'].isin(method)]

        if code:
            df_request = df_request[df_request['code'].isin(code)]

        if url_match:
            df_request = df_request[df_request['url'].str.contains(url_match)]

        out_cols = ['request_id', 'datetime_start', 'datetime_finish', 'duration(s)',
                    'method', 'url', 'code', 'exception', 'detail']

        df_request.sort_values(by='datetime_start', ascending=False, inplace=True)
        return df_request[out_cols].to_html(justify='left')
