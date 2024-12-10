import pandas as pd

def create_aggregate(data: pd.DataFrame):
    # # TotalTimeの"ms"を除去して整数化
    data['TotalTime_ms'] = data['TotalTime'].str.replace('ms', '', regex=False).astype(int)

    # 日付をdatetime型へ変換（UTCを仮定、タイムゾーンは任意）
    # ISO8601はpandasが自動認識しますが、必要なら utc=True オプションを付与
    time_cols = ['StartTime', 'ReceivedDatetime', 'LastActionDatetime', 'ProcessStartDatetime', 'ActionDatetime']
    for col in time_cols:
        # 欠損値対策として errors='coerce'。必ず日付がある前提でなければエラー回避にも有効
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], errors='coerce')

    data['StartTime'] = pd.to_datetime(data['StartTime'], utc=True)
    data['ActionDatetime'] = pd.to_datetime(data['ActionDatetime'], utc=True)
    data['ReceivedDatetime'] = pd.to_datetime(data['ReceivedDatetime'], utc=True)
    data['LastActionDatetime'] = pd.to_datetime(data['LastActionDatetime'], utc=True)
    data['ProcessStartDatetime'] = pd.to_datetime(data['ProcessStartDatetime'], utc=True)

    # JOB_PROCESSEDの解析
    processed = data[data['EventType'] == 'JOB_PROCESSED'].copy()

    # LastActionCodeごとに集計: TotalTime_ms と ActionMinusStart_ms
    processed_stats = processed.groupby('LastActionCode').agg(
        TotalTime_count=('TotalTime_ms', 'count'),
        TotalTime_mean=('TotalTime_ms', 'mean'),
        TotalTime_max=('TotalTime_ms', 'max'),
        TotalTime_min=('TotalTime_ms', 'min'),
        TotalTime_median=('TotalTime_ms', 'median'),
        TotalTime_var=('TotalTime_ms', 'var'),
    )

    # JOB_SUCCESSの解析
    success = data[data['EventType'] == 'JOB_SUCCESS'].copy()


    # Successの場合: TotalTime_msと(ActionDatetime - ProcessStartDatetime)
    success['SeverTotalTime_ms'] = (success['ActionDatetime'] - success['ProcessStartDatetime']).dt.total_seconds() * 1000

    success_client_stats = success.agg(
        ClientTotalTime_count=('TotalTime_ms', 'count'),
        ClientTotalTime_mean=('TotalTime_ms', 'mean'),
        ClientTotalTime_max=('TotalTime_ms', 'max'),
        ClientTotalTime_min=('TotalTime_ms', 'min'),
        ClientTotalTime_median=('TotalTime_ms', 'median'),
        ClientTotalTime_var=('TotalTime_ms', 'var'),
    )

    success_sever_stats = success.agg(
        SeverTotalTime_count=('SeverTotalTime_ms', 'count'),
        SeverTotalTime_mean=('SeverTotalTime_ms', 'mean'),
        SeverTotalTime_max=('SeverTotalTime_ms', 'max'),
        SeverTotalTime_min=('SeverTotalTime_ms', 'min'),
        SeverTotalTime_median=('SeverTotalTime_ms', 'median'),
        SeverTotalTime_var=('SeverTotalTime_ms', 'var')
    )

    return processed_stats, success_client_stats.T, success_sever_stats.T