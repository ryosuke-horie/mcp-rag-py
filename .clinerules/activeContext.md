# Active Context

## Current Work Focus

-   `rag_api_server` の実装が完了:
    - FastAPIアプリケーションの初期設定
    - `rag_core` との連携実装
    - APIエンドポイントの実装（ドキュメント登録と検索機能）
    - CORSサポートの追加
    - 設定管理機能の実装（環境変数による設定のカスタマイズ）
    - インポート問題の解決（プロジェクトルートからの実行方式の採用）
    - 詳細なREADMEの整備（セットアップ手順、API仕様など）
-   次のステップとして、`mcp_adapter` の実装を開始する。

## Recent Changes

-   `rag_api_server` の実装完了。主な実装内容：
    -   `config.py`: 環境変数を使用した設定管理
    -   `core.py`: RAGコア機能の統合
    -   `main.py`: FastAPIアプリケーションとエンドポイントの実装
    -   `README.md`: 詳細な使用方法とAPI仕様の文書化

## Next Steps

1.  `mcp_adapter` の実装を開始する:
    -   MCPサーバーのスケルトンコード作成
    -   `rag_api_server` との連携実装
    -   MCPツールとリソースの定義
