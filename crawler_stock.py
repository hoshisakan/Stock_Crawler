import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from module.handle_exception import HandleException
from module.log_generate import Loggings
from module.date import DateTimeTools as DT
from module.reptile import RequestPageSource
from module.argument_config import ArgumentConfig
import pandas as pd
from instance.config import Initialization as Init
import math
from threading import Thread
from decimal import Decimal, ROUND_HALF_UP

logger = Loggings()

def timer(func):
    def time_count():
        exc_start_time = DT.get_current_datetime()
        func()
        exc_end_time = DT.get_current_datetime()
        exc_time = exc_end_time - exc_start_time
        msg = "Execute time: {}".format(exc_time)
        logger.info(msg)
    return time_count

def write_iterator_to_log(iterator):
    [logger.info(read_iterator_info) for read_iterator_info in iterator]

def write_iterator_multiple_to_log(iterator):
    for outside_index, outside in enumerate(iterator, 1):
        logger.info(f'The {outside_index} iterator')
        logger.info('------------------------------------------------------')
        for inner_index, inner_iterator in enumerate(outside, 1):
            logger.info(f"The {inner_index} data is {inner_iterator}")
        logger.info('------------------------------------------------------')

class Stock():
    """
        :Parameters:
            ticker : str
                Valid ticker stock company name or number: 2317.TW,FB,6758.T
            output_path : str
                stock info write csv output path
    """
    def __init__(self, **kwargs):
        self.__base_url = Init.base_url_list['stock']['yahoo_finance'][-1]
        self.__ticker = kwargs.get('ticker', None)
        self.__output_path = kwargs.get('output_path', None)
        self.__col = ['trade_date','open_price', 'high_price', 'low_price',
                        'close_price', 'adj_close_price', 'volume']

    def __check_nan_exists(self, check_val):
        return str(check_val).lower().find("nan")

    def __round_down(self, f):
        return Decimal(str(f)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    def __regular_data_for_api_v8(self, cols, rows):
        result = []
        for date, open_price, high_price, low_price, close_price, adjclose_price, volume in zip(
            rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6],
        ):
            date = DT.convert_timestamp_to_datetime(date) if date else '1990-01-01'
            # logger.warning([date, open_price, high_price, low_price, close_price, adjclose_price, volume])
            open_price = 0 if open_price is None or self.__check_nan_exists(str(open_price)) != -1 else self.__round_down(open_price)
            high_price = 0 if high_price is None or self.__check_nan_exists(str(high_price)) != -1 else self.__round_down(high_price)
            low_price = 0 if low_price is None or self.__check_nan_exists(str(low_price)) != -1 else self.__round_down(low_price)
            close_price = 0 if close_price is None or self.__check_nan_exists(str(close_price)) != -1 else self.__round_down(close_price)
            adjclose_price = 0 if adjclose_price is None or self.__check_nan_exists(str(adjclose_price)) != -1 else self.__round_down(adjclose_price)
            volume = 0 if volume is None or self.__check_nan_exists(str(volume)) != -1 else volume
            temp = [
                date, open_price, high_price,
                low_price, close_price, adjclose_price, volume
            ]
            result.append(dict(zip(cols, temp))) if any(temp[1:]) is True else logger.warning(f'{self.__ticker} no data in {temp[0]}')
        return result

    def __check_path_exists_and_create(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __check_path_exists_and_remove(self, path):
        if os.path.exists(path):
            os.remove(path)
            logger.info(f'Removeing duplicate file from path {path}.')

    def obtain_history_records_v2(self, start=None, end=None):
        result = {'json_rows': ''}
        rows = []
        info = []
        try:
            if start is None and end is None:
                raise Exception('The start date and end date is required')
            start_date = int(DT.get_datetime_convert_to_timestamp(start))
            end_date = int(DT.get_datetime_convert_to_timestamp(end))

            logger.info(f'Staring get ticker {self.__ticker} history records')
            full_url = f'{self.__base_url}v8/finance/chart/{self.__ticker}?symbol={self.__ticker}&period1={start_date}&period2={end_date}&interval=1d&events=history'
            logger.warning(f'Request yahoo finance api v8 endpoint: {full_url}')
            validate_url = f'https://finance.yahoo.com/quote/{self.__ticker}/history?&period1={start_date}&period2={end_date}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
            logger.warning(f'Validate from yahoo finance api obtain stock info url: {validate_url}')

            with RequestPageSource(
                url=full_url, mode=False,
                headers={'User-Agent': 'Mozilla/5.0'}
            ) as res:
                res_json = res.json()['chart']['result'][0]
                stock_info = res_json['indicators']['quote'][0]
                if not res_json or not stock_info:
                    raise Exception(f'The tikcer {self.__ticker} not found any stock price info.')
                rows.extend(
                    [
                        res_json['timestamp'], stock_info['open'],
                        stock_info['high'], stock_info['low'],
                        stock_info['close'], res_json['indicators']['adjclose'][0]['adjclose'],
                        stock_info['volume']
                    ])
            logger.info(f'Finish get ticker {self.__ticker} history records')
            if len(rows) > 0:
                info = sorted(self.__regular_data_for_api_v8(self.__col, rows), key=lambda x: x['trade_date'], reverse=True)
                result['json_rows'] = info
                if self.__output_path is None:
                    raise FileNotFoundError('Output path is required.')
                self.__check_path_exists_and_create(self.__output_path)
        except (FileNotFoundError, OSError) as fe:
            logger.error(HandleException.show_exp_detail_message(fe))
        except Exception as e:
            logger.error(HandleException.show_exp_detail_message(e))
        else:
            full_path = f"{self.__output_path}\\{self.__ticker}.csv"
            self.__check_path_exists_and_remove(full_path)
            df = pd.DataFrame(result['json_rows'])
            df.to_csv(full_path, encoding='utf-8-sig', index=False)
        result.clear()
        rows.clear()
        info.clear()

def run_job():
    stock_crawler_target_list = []

    ArgumentConfig.run()

    if not os.path.exists(Init.stock_info_list_path):
        raise Exception(f'Not found stock info list txt file path: {Init.stock_info_list_path}')

    with open(Init.stock_info_list_path, mode='r') as f:
        stock_crawler_target_list = [read.strip().split(',') for read in f.readlines()]
    write_iterator_to_log(stock_crawler_target_list)

    for task_items in stock_crawler_target_list:
        current_task = []
        obj = Stock(ticker=task_items[0], output_path=Init.output_path)
        current_task = Thread(
            target=lambda start, end:obj.obtain_history_records_v2(start, end),
            kwargs=({'start': f'{task_items[1]} 08:00:00', 'end': f'{task_items[2]} 23:59:59'})
        )
        current_task.start()
        current_task.join()
        del obj

@timer
def main():
    run_job()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(HandleException.show_exp_detail_message(e))
    except KeyboardInterrupt:
        os._exit(0)
