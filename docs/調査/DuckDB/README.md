# DuckDB と VSS 拡張について

このディレクトリには、DuckDB とその Vector Similarity Search (VSS) 拡張に関する情報をまとめています。

## 概要

DuckDB は、**OLAP (Online Analytical Processing) 分析に特化したインプロセス（組み込み型）のリレーショナルデータベース管理システム (RDBMS)** です。「SQLite の OLAP 版」とも表現されます。

### 主な特徴

*   **高速な分析処理:** 列指向ストレージとベクトル化実行エンジン。
*   **インプロセス:** アプリケーションへの直接組み込み。
*   **インストール不要:** セットアップが容易。
*   **SQL サポート:** 標準 SQL と豊富な分析関数。
*   **多様なデータ形式の直接クエリ:** Parquet, CSV, JSON など。
*   **Python との親和性:** Pandas DataFrame などとの連携。
*   **拡張性:** VSS などの機能を追加可能。
*   **OSS:** MIT ライセンス。

参考: [DuckDB 公式サイト](https://duckdb.org/)

## VSS (Vector Similarity Search) 拡張

DuckDB VSS 拡張は、DuckDB にベクトル類似性検索機能を追加します。

### 概要

*   高次元ベクトルデータに対する類似度検索 (ANN)。
*   RAG システムのベクトルストアとしての活用。

### 主な機能

*   **HNSW アルゴリズム:** `usearch` ライブラリに基づく効率的な ANN 実装。
*   **SQL インターフェース:** SQL でインデックス作成や検索を実行。

参考:
*   [DuckDB VSS Extension Blog Post](https://duckdb.org/2024/05/03/vector-similarity-search-vss.html)
*   [GitHub: duckdb/duckdb-vss](https://github.com/duckdb/duckdb-vss)

## 詳細情報

*   **セットアップ:** [Python 環境でのセットアップ手順](./setup.md)
*   **Python での使い方:** [基本的な使い方、注意点、試行錯誤の過程](./usage_python.md)
