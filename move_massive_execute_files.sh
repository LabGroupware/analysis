#!/bin/bash

# =============================================================================
# スクリプト名: move_massive_execute_files.sh
# 説明: 指定されたディレクトリを再帰的に検索し、massive_execute_*.csv
#       という名前のファイルを指定された移動先ディレクトリに移動します。
#       ファイル名には元のディレクトリ名をプレフィックスとして追加します。
# 使用法: ./move_massive_execute_files.sh <source_directory> <destination_directory>
# =============================================================================

# -----------------------------------------------------------------------------
# 関数: usage
# 説明: スクリプトの使用方法を表示します。
# -----------------------------------------------------------------------------
usage() {
    echo "Usage: $0 <source_directory> <destination_directory>"
    exit 1
}

# -----------------------------------------------------------------------------
# 引数の数をチェック
# -----------------------------------------------------------------------------
if [ "$#" -ne 2 ]; then
    echo "Error: Exactly two arguments are required."
    usage
fi

SOURCE_DIR="$1"
DEST_DIR="$2"

# -----------------------------------------------------------------------------
# ソースディレクトリの存在とディレクトリであることを確認
# -----------------------------------------------------------------------------
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist or is not a directory."
    exit 1
fi

# -----------------------------------------------------------------------------
# 移動先ディレクトリが存在しない場合は作成
# -----------------------------------------------------------------------------
if [ ! -d "$DEST_DIR" ]; then
    echo "Destination directory '$DEST_DIR' does not exist. Creating it..."
    mkdir -p "$DEST_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create destination directory '$DEST_DIR'."
        exit 1
    fi
fi

# -----------------------------------------------------------------------------
# massive_execute_*.csv ファイルを検索して移動
# -----------------------------------------------------------------------------
echo "Searching for 'massive_execute_*.csv' in '$SOURCE_DIR' and moving them to '$DEST_DIR'..."

# find コマンドを使用してファイルを検索
find "$SOURCE_DIR" -type f -name 'massive_execute_*.csv' | while IFS= read -r FILE; do
    # ファイルが属するディレクトリ名を取得
    DIR_NAME=$(basename "$(dirname "$FILE")")
    
    # ファイル名を取得
    FILE_NAME=$(basename "$FILE")
    
    # 新しいファイル名を作成（ディレクトリ名をプレフィックスとして追加）
    NEW_FILE_NAME="${DIR_NAME}_${FILE_NAME}"
    
    # 移動先のパスを設定
    DEST_PATH="$DEST_DIR/$NEW_FILE_NAME"
    
    # 移動先に同名のファイルが存在する場合はスキップ
    if [ -e "$DEST_PATH" ]; then
        echo "Warning: File '$DEST_PATH' already exists. Skipping '$FILE'."
        continue
    fi
    
    # ファイルを移動
    mv "$FILE" "$DEST_PATH"
    if [ $? -eq 0 ]; then
        echo "Moved: '$FILE' -> '$DEST_PATH'"
    else
        echo "Error: Failed to move '$FILE' to '$DEST_DIR'."
    fi
done

# -----------------------------------------------------------------------------
# 空のディレクトリを削除（オプション）
# -----------------------------------------------------------------------------
find "$SOURCE_DIR" -type d -empty -delete

echo "Operation completed."
