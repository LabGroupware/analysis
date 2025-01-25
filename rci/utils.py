def bytes_to_human_readable(num_bytes, unit_system='binary', decimal_places=2) -> str:
    """
    バイト数を人間が読みやすい単位に変換します。

    Parameters:
    - num_bytes (int or float): バイト数。
    - unit_system (str): 'binary' (2の累乗) または 'decimal' (10の累乗) を指定。
    - decimal_places (int): 小数点以下の表示桁数。

    Returns:
    - str: 人間が読みやすい形式の文字列。
    """

    if num_bytes < 0:
        raise ValueError("num_bytes は0以上の数値でなければなりません。")

    # 単位の定義
    if unit_system == 'binary':
        # 2の累乗（IEC規格）
        units = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
        step = 1024
    elif unit_system == 'decimal':
        # 10の累乗（SI規格）
        units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        step = 1000
    else:
        raise ValueError("unit_system は 'binary' または 'decimal' のいずれかでなければなりません。")

    # 特殊ケース: 0 Bytes
    if num_bytes == 0:
        return f"0 {units[0]}"

    # ループして適切な単位を見つける
    for i, unit in enumerate(units):
        if num_bytes < step:
            break
        if i < len(units) - 1:
            num_bytes /= step
        else:
            # 単位の範囲を超えた場合は最後の単位を使用
            break

    return f"{num_bytes:.{decimal_places}f} {unit}"