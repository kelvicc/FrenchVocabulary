# DUO Français 3.0 — フランス語版 DUO 総合学習システム

本リポジトリは、全45セクション・560例文・2,221見出し語・巻末11,458総合索引、および全音声を収録した完全統合型のフランス語学習 Web アプリケーションです。

---

## 📱 アプリケーション一覧

| アプリ | 説明 | 推奨環境 |
| :--- | :--- | :--- |
| **[`mobile.html`](mobile.html)** | **スマホ最適化版**（2カラム横並び維持・例文間左右スワイプ移動・片手親指ナビゲーション） | スマートフォン（iPhone / Android） |
| **[`index.html`](index.html)** | **PC・タブレット版**（本家DUO 2カラム・見開き一覧・ソフトパステル配色） | PC / iPad / タブレット |

---

## 🚀 GitHub Pages での公開手順（スマホからアクセスする方法）

1. 本リポジトリの変更をコミットして GitHub にプッシュします：
   ```bash
   git add .
   git commit -m "Add DUO Français mobile and desktop web apps with full audio assets"
   git push origin main
   ```
2. GitHub のリポジトリ画面を開き、**「Settings」→「Pages」** に移動します。
3. **Build and deployment** の Source で **「Deploy from a branch」** を選択し、Branch を **`main` / `/(root)`** に設定して「Save」をクリックします。
4. 数分後、発行された公開URL（`https://<ユーザー名>.github.io/FrenchVocabulary-DUOconcept/mobile.html`）へスマホのブラウザ（Safari や Chrome）からアクセスするだけで、いつでも快適に学習いただけます。

※リポジトリ直下に `.nojekyll` を配置済みのため、GitHub Pages 上で全ファイルが正常に配信されます。
