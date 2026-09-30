# deliverables

- `pptx/`: 章ごとの完成pptx（画像→PowerPoint変換済み）
- `chN/`: 各スライドの生成スクリプト（make_spec.py → spec.json → build_pptx.py で再生成）
- `reference/`: AINestテンプレート

再生成: `python3 make_spec.py && python3 ../../../.claude/skills/png-to-editable-pptx/scripts/build_pptx.py spec.json out.pptx`（パスは章フォルダに合わせて調整）
