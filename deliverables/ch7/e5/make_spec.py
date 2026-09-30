import sys
sys.path.insert(0, "..")
from tables import *

P = lambda titles, bullets, **k: {"titles": titles, "bullets": bullets, **k}
R = lambda icon, name, sub, a, b, c: {"icon": icon, "name": name, "sub": sub, "cols": [a, b, c]}
rows = [
    R("azure:workflow", "Dify", "（ワークフロー作成・実行基盤）", P(["Dify"], ["生産技術部員のワークフロー変更・作成", "RAG／エージェントのオーケストレーション"]),
      P(["n8n"], ["柔軟なワークフロー設計", "既存システム連携に強い"]), ["現場ユーザーによるフロー作成・変更のしやすさ", "必要機能（RAG、権限、運用管理）の充足度", "運用コスト・保守性・社内スキルの適合性"]),
    R("azure:app-services", "FastAPI", "（検索・判定・生成の決定的処理）", P(["FastAPI（Python）"], ["検索 APIのエンドポイント実装", "コード検証・版判定などの決定処理"]),
      P(["Flask / Spring Boot"], ["シンプルな構成（Flask）", "既存資産との親和性（Spring Boot）"]), ["開発・保守のしやすさ、拡張性", "セキュリティ対応、認証・監査ログ連携", "社内標準との整合性"]),
    R("azure:machine-learning", "vLLM", "（LLM 推論基盤）", P(["vLLM"], ["高スループットな LLM 推論", "オンプレ（DGX Spark）での運用適合"]),
      P(["Text Generation Inference（TGI）", "llama.cpp（軽量構成）"], ["環境や規模に応じた選択肢"], tsize=17), ["応答速度・同時利用性能", "対応モデルの豊富さ", "DGX Spark での動作安定性・運用コスト"]),
    R("azure:virtual-machine", "llama.cpp", "（軽量LLM 推論）", P(["llama.cpp"], ["小～中規模モデルの軽量・安定推論", "検証用途・比較評価に利用"]),
      P(["Ollama / LM Studio"], ["簡易運用・検証環境"]), ["低リソース環境での動作安定性", "必要精度・応答速度の達成可否", "運用の簡易性（導入・更新・管理）"]),
    R("azure:cognitive-services", "日本語Embedding\vモデル", "（ベクトル化）", P(["intfloat/multilingual-e5-large"], ["日本語を含む多言語対応", "高い検索性能・実績"], tsize=18),
      P(["BAAI/bge-large-ja", "SBIntuitions/text-embedding-3-large"], ["日本語特化／商用モデルの選択肢"], tsize=15.5), ["検索精度（再現率・適合率）", "日本語ドメインでの性能", "モデルサイズ・推論速度・運用コスト"]),
    R("azure:metrics", "Ruri系リランカー", "（再ランキング）", P(["ruri-large（Ruri系）"], ["日本語特化の高精度リランク", "社内文書に適した関連度向上"]),
      P(["bge-reranker-large-ja", "cohere-rerank（商用）"], ["精度・コストに応じた選択肢"], tsize=17), ["再ランキング後の精度向上効果", "日本語での性能・安定性", "推論速度・運用コスト"]),
    R("azure:cognitive-search", "OpenSearch", "（全文検索・ベクトル検索）", P(["OpenSearch（2.11 以降）"], ["全文検索＋ベクトル検索の統合", "ハイブリッド検索・RRF 対応"]),
      P(["Elasticsearch"], ["既存環境・運用要件に応じて選択"]), ["検索性能（全文・ベクトル・ハイブリッド）", "運用性・スケーラビリティ", "社内標準・既存資産との整合性"]),
    R("azure:azure-database-postgresql-server", "pgvector", "（構造化データのベクトル検索）", P(["PostgreSQL + pgvector"], ["構造化データとベクトルの統合検索", "版管理・トランザクションとの親和性"]),
      P(["専用ベクトルDB（Pinecone 等）"], ["大規模化時のクラウド選択肢"]), ["検索性能・拡張性", "運用コスト・保守性", "オンプレ/クラウド移行時の再現性"]),
    R("azure:form-recognizers", "Docling", "（文書抽出・前処理）", P(["Docling"], ["PDF/図面のテキスト・表・画像抽出", "RAG 向けの構造化データ生成"]),
      P(["Azure Document Intelligence", "Unstructured / OCR（Tesseract 等）"], ["クラウド／既存ツールの選択肢"], tsize=15.5), ["抽出精度（テキスト・表・画像）", "図面・TIFF 等の対応可否", "運用コスト・オンプレ/クラウドの適合性"]),
]
s = build("表7-3　推奨製品・モデルと代替案（PoC評価で最終採否を決定）",
          [[("対象", 20)], [("推奨案", 20)], [("代替案", 20)], [("選定・切替の基準", 20), ("（PoCでの評価ポイント）", 15)]],
          [356, 412, 398, 478], rows, H0=42, total=870, name_sizes=(19.5, 14.5), bsize=16, colored_cells=True)
dump(s)
