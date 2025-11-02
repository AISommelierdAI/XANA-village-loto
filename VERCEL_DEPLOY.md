# Vercelへのデプロイ手順

このExpoアプリをVercelでWeb公開する手順です。

## 前提条件

- Vercelアカウント（[vercel.com](https://vercel.com)で無料登録可能）
- GitHubアカウント（推奨）

## デプロイ方法

### 方法1: GitHub経由で自動デプロイ（推奨）

1. **GitHubにリポジトリをプッシュ**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <あなたのGitHubリポジトリURL>
   git push -u origin main
   ```

2. **Vercelでプロジェクトをインポート**
   - [Vercel Dashboard](https://vercel.com/dashboard)にログイン
   - 「Add New...」→「Project」をクリック
   - GitHubリポジトリを選択
   - プロジェクト設定：
     - **Framework Preset**: Other
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
     - **Install Command**: `npm install`
   - 「Deploy」をクリック

3. **自動デプロイ**
   - GitHubにプッシュするたびに自動でデプロイされます

### 方法2: Vercel CLIを使用

1. **Vercel CLIをインストール**
   ```bash
   npm install -g vercel
   ```

2. **ログイン**
   ```bash
   vercel login
   ```

3. **デプロイ**
   ```bash
   vercel
   ```
   
   初回は設定を聞かれます：
   - Link to existing project? → `No`
   - Project name → 任意の名前
   - Directory → `./dist`
   - Override settings? → `No`

4. **本番デプロイ**
   ```bash
   vercel --prod
   ```

## ローカルでのビルドテスト

Vercelにデプロイする前に、ローカルでビルドが成功するか確認できます：

```bash
npm run build
```

ビルドされたファイルは `dist` ディレクトリに生成されます。

## 注意事項

- `background.png`ファイルが正しく含まれているか確認してください
- 初回デプロイ時は数分かかる場合があります
- ビルドエラーが発生した場合は、Vercelのログを確認してください

## トラブルシューティング

### ビルドエラーが発生する場合

1. `package.json`の依存関係が最新か確認
2. Node.jsのバージョンが18以上か確認（Vercelのデフォルトは18）
3. `.gitignore`に`node_modules`と`dist`が含まれているか確認

### 画像が表示されない場合

- `background.png`がプロジェクトルートに存在するか確認
- `app.json`の`assetBundlePatterns`に`**/*`が設定されているか確認

## カスタムドメインの設定

1. Vercelダッシュボードでプロジェクトを開く
2. 「Settings」→「Domains」をクリック
3. ドメインを追加

---

デプロイが完了すると、Vercelが自動でURLを生成します（例：`your-project.vercel.app`）

