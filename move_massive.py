import shutil
from pathlib import Path
import argparse

def move_massive_execute_dirs(base_dir: Path):
    """
    基点ディレクトリ以下を再帰的に検索し、
    名前が'massive_execute_'で始まるディレクトリを基点ディレクトリ直下に移動する。
    """
    if not base_dir.exists() or not base_dir.is_dir():
        print(f"指定された基点ディレクトリが存在しないか、ディレクトリではありません: {base_dir}")
        return

    # 基点ディレクトリ直下に移動先があることを確認
    target_dir = base_dir.resolve()

    # 再帰的に検索
    for path in base_dir.rglob('exec_*'):
        if path.is_file():
            try:
                # ディレクトリを移動
                shutil.move(str(path), str(destination))
                print(f"移動完了: {path} -> {destination}")
            except Exception as e:
                print(f"ディレクトリの移動に失敗しました: {path}. エラー: {e}")
        if path.is_dir():
            print(f"見つかったディレクトリ: {path}")

            # 移動先のパスを作成
            destination = target_dir / path.name

            # 移動先に同名のディレクトリが既に存在する場合
            if destination.exists():
                print(f"移動先に同名のディレクトリが既に存在します: {destination}. スキップします。")
                continue

            try:
                # ディレクトリを移動
                shutil.move(str(path), str(destination))
                print(f"移動完了: {path} -> {destination}")
            except Exception as e:
                print(f"ディレクトリの移動に失敗しました: {path}. エラー: {e}")

def main():
    parser = argparse.ArgumentParser(description="massive_execute_* ディレクトリを基点ディレクトリ直下に移動します。")
    parser.add_argument('base_directory', type=str, help='検索を開始する基点ディレクトリのパス')
    args = parser.parse_args()

    base_dir = Path(args.base_directory).resolve()
    move_massive_execute_dirs(base_dir)

if __name__ == "__main__":
    main()