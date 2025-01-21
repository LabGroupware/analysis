import pandas as pd

actions_lists = {
    "create_user_profile": ["CREATE_USER_PROFILE", "CREATE_USER_PREFERENCE"],
    "create_file_object": ["VALIDATE_FILE_OBJECT", "CREATE_FILE_OBJECT"],
    "create_organization": ["VALIDATE_ORGANIZATION", "VALIDATE_USER", "CREATE_ORGANIZATION_AND_ADD_INITIAL_ORGANIZATION_USER", "CREATE_DEFAULT_TEAM_AND_ADD_INITIAL_DEFAULT_TEAM_USER"],
    "create_team": ["VALIDATE_TEAM", "VALIDATE_ORGANIZATION_AND_ORGANIZATION_USER_EXIST", "CREATE_TEAM_AND_ADD_INITIAL_TEAM_USER"],
    "create_task": ["VALIDATE_TASK", "VALIDATE_USER", "VALIDATE_TEAM", "VALIDATE_FILE_OBJECT", "CREATE_TASK_AND_ATTACH_FILE_OBJECT"]
}

def create_aggregate(data: pd.DataFrame, action: str) -> tuple:

    # JOB_PROCESSEDの解析
    processed = data[data['EventType'] == 'JOB_PROCESSED'].copy()

    actions_list = actions_lists[action]

    action_set = []
    last_action = actions_list[-1]
    last_action_time_diff = processed[processed['LastActionCode'] == last_action]['DatetimeDiff_ms'].mean()
    pre_action_diff = 0
    for action in actions_list:
        processed_action = processed[processed['LastActionCode'] == action]
        if processed_action.empty:
            continue
        currentActionDiff = processed_action['DatetimeDiff_ms'] - pre_action_diff
        action_set.append(currentActionDiff.mean())
        pre_action_diff = processed_action['DatetimeDiff_ms'].mean()

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

    return processed_stats, success_client_stats.T, success_sever_stats.T, action_set, last_action_time_diff