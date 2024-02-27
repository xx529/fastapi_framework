import json
import re
from functools import lru_cache
from typing import List

import numpy as np
import pandas as pd
from pandas import DataFrame

from app.config import log_conf, project_dir
from app.schema.enum import LoggerTypeEnum, RequestMethod
from app.schema.schemas.system import LogDetailParam


class LogService:

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

    def runtime_log(self, param: LogDetailParam):
        if param.refresh:
            self.load_all_log.cache_clear()

        df_log = self.load_all_log()

        df_log = df_log[df_log['request_id'] == param.request_id.hex]
        df_log['duration'] = df_log['datetime'].diff(-1).dt.total_seconds().fillna(0.0).abs()

        total_duration = df_log['duration'].sum()
        df_log['proportion'] = df_log['duration'].apply(lambda x: f'{round(x / total_duration, 2) * 100}%')

        df_log['message'] = df_log[['type', 'message']].apply(
            lambda x: x['message'].replace(' ', '###space###')
            if x['type'] == LoggerTypeEnum.EXCEPTION
            else x['message'], axis=1)

        df_log.drop(['exception', 'request_id'], axis=1, inplace=True)
        html = df_log.to_html(justify='left').replace('\\n', '<br>').replace('###space###', '&nbsp;')
        return html

    def request_log(self, refresh: bool, method: List[RequestMethod], status_code: List[int], url_match: str, last: int):
        if refresh:
            self.load_all_log.cache_clear()

        df_log = self.load_all_log()
        cols = ['datetime', 'request_id', 'message', 'exception']

        df_start = df_log.query(f'type == "{LoggerTypeEnum.REQUEST_START.value}"')[cols]
        df_finish = df_log.query(f'type == "{LoggerTypeEnum.REQUEST_FINISH.value}"')[cols]
        df_request = pd.merge(df_start, df_finish, on='request_id', suffixes=('_start', '_finish'), how='left')

        df_request['duration(s)'] = (df_request['datetime_finish'] - df_request['datetime_start']).dt.total_seconds()

        df_request['status_code'] = df_request['message_finish'].apply(
            lambda x: int(re.findall('status code: (\d+)', x)[0]) if x is not np.nan else 0
        )

        df_request['error_code'] = df_request['message_finish'].apply(
            lambda x: re.findall('error code: (\d+) ', x) if x is not np.nan else [0])
        df_request['msg'] = df_request['message_finish'].apply(
            lambda x: re.findall('error msg: (.*?) ', x) if x is not np.nan else [''])
        df_request['detail'] = df_request['message_finish'].apply(
            lambda x: re.findall('detail: (.*)', x) if x is not np.nan else [''])
        df_request[['method', 'url']] = df_request[['message_start']].apply(
            lambda x: x['message_start'].split(), axis=1, result_type='expand')

        default_filter_urls = ['/openapi.json', 'docs', '/system/log']
        df_request = df_request[~df_request['url'].str.contains('|'.join(default_filter_urls))]

        for col in ['error_code', 'msg', 'detail']:
            df_request[col] = df_request[col].apply(lambda x: x[0] if len(x) > 0 else '')

        if method:
            df_request = df_request[df_request['method'].isin([m.value for m in method])]

        if status_code:
            df_request = df_request[df_request['status_code'].isin(status_code)]

        if url_match:
            df_request = df_request[df_request['url'].str.contains(url_match)]

        out_cols = ['request_id', 'datetime_start', 'datetime_finish', 'duration(s)',
                    'method', 'url', 'status_code', 'error_code', 'msg', 'detail']
        df_request = df_request.sort_values(by='datetime_start', ascending=False).reset_index(drop=True)
        df_request = df_request.iloc[:last]
        html = df_request[out_cols].to_html(justify='left')
        return html
