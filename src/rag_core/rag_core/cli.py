from pathlib import Path

import typer

from .main import process_directory, process_file

app = typer.Typer(help="RAG Core CLI - ドキュメントを処理してベクトルDBに登録します。")


@app.command()
def main(
    file: Path = typer.Option(
        None,
        "--file",
        "-f",
        help="処理する単一のドキュメントファイル (.txt または .md)。--dir と同時に指定することはできません。",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
    directory: Path = typer.Option(
        None,
        "--dir",
        "-d",
        help="処理するドキュメントが含まれるディレクトリ。中の .txt と .md を再帰的に処理します。--file と同時に指定することはできません。",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    指定されたファイルまたはディレクトリ内のドキュメントを処理し、ベクトルDBに登録します。
    """
    if file and directory:
        typer.echo(
            "エラー: --file と --dir を同時に指定することはできません。", err=True
        )
        raise typer.Exit(code=1)
    if not file and not directory:
        typer.echo(
            "エラー: --file または --dir のいずれかを指定してください。", err=True
        )
        raise typer.Exit(code=1)

    if file:
        if file.suffix not in [".txt", ".md"]:
            typer.echo(
                f"エラー: サポートされていないファイル形式です: {file.suffix}", err=True
            )
            raise typer.Exit(code=1)
        typer.echo(f"処理を開始します (ファイル): {file}")
        process_file(file)
        typer.echo(f"ファイルの処理が完了しました: {file}")

    if directory:
        typer.echo(f"処理を開始します (ディレクトリ): {directory}")
        process_directory(directory)
        typer.echo(f"ディレクトリの処理が完了しました: {directory}")

    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
