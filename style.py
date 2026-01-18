custom_css = """
<style>
    /* 全体の背景と基本フォント */
    .stApp {
        background-color: #f8fafc;
    }

    /* デフォルトヘッダーを非表示 */
    header { visibility: hidden; height: 0px; }
    .block-container { padding-top: 100px !important; }

    /* --- 固定ヘッダー & プログレスバー --- */
    .brand-header {
        position: fixed;
        top: 0; left: 0; width: 100%;
        background-color: #008080; /* ブランドカラー */
        color: white;
        padding: 15px 30px;
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 900;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* プログレスバー・コンテナ */
    .progress-wrapper {
        position: fixed;
        top: 60px; left: 0; width: 100%;
        background-color: white;
        padding: 15px 50px;
        z-index: 999;
        border-bottom: 1px solid #e2e8f0;
    }

    /* --- カード型UIコンポーネント --- */
    .card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        border: 2px solid #008080;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 16px;
        transition: transform 0.2s;
    }
    .card:hover { transform: translateY(-2px); border-color: #008080; }

    /* 回答ボタンのカスタマイズ */
    div[data-testid="stHorizontalBlock"] button {
        height: 60px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
    }

    /* --- フッターナビゲーション --- */
    .footer-nav {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: white;
        padding: 15px 50px;
        border-top: 1px solid #008080;
        display: flex;
        justify-content: space-between;
        z-index: 1000;
    }
    
    /* 質問カード全体のコンテナ */
    .question-card {
        background-color: white;
        border-radius: 20px;
        padding: 25px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* 質問テキスト */
    .question-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #334155;
        margin-bottom: 5px;
    }

    /* サブタイトル（関連不良など） */
    .question-sub {
        font-size: 0.9rem;
        color: #37b7c4;
        font-weight: bold;
        border-left: 3px solid #37b7c4;
        padding-left: 10px;
        margin-bottom: 15px;
        font-style: italic;
    }

    /* ラジオボタンタイルのデザイン上書き */
    /* 状況確認ページの特定のラジオボタンをターゲットにします */
    div[data-testid="stRadio"] > div[data-testid="stWidgetStack"] {
        flex-direction: row !important;
        justify-content: flex-end !important; /* ボタンを右寄せ */
        gap: 10px !important;
    }

    div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        padding: 10px 25px !important;
        border-radius: 12px !important;
        min-width: 80px !important;
        justify-content: center !important;
        transition: all 0.2s;
    }

    /* 選択時の色設定 */
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        border-color: #37b7c4 !important;
        background-color: #f0fdfa !important;
        color: #37b7c4 !important;
        box-shadow: 0 2px 4px rgba(55, 183, 196, 0.1) !important;
    }

    /* 文字を中央揃え・太字 */
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
        font-weight: bold !important;
        font-size: 1rem !important;
    }

    /* デフォルトの丸を隠す */
    div[data-testid="stRadio"] input { display: none !important; }
    
    /* ラジオボタン全体のコンテナを横幅いっぱいに */
    div[data-testid="stRadio"] {
        width: 100% !important;
    }

    /* ラベル（「不良名を選択してください」）のデザイン */
    div[data-testid="stRadio"] > label {
        background-color: transparent !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        color: #334155 !important;
        padding-bottom: 15px !important;
    }

    /* ボタンを包むスタックを横並びにする */
    div[data-testid="stRadio"] > div[data-testid="stWidgetStack"] {
        flex-direction: row !important;
        flex-wrap: wrap !important; /* ボタンが多い場合に折り返す */
        gap: 15px !important;
        width: 100% !important;
        display: flex !important;
    }

    /* 各選択肢（タイルボタン）の基本デザイン */
    div[data-testid="stRadio"] label[data-baseweb="radio"] {
        flex: 1 1 calc(20% - 15px) !important; /* 5列並べる設定 */
        min-width: 150px !important;
        background-color: white !important;
        padding: 25px 10px !important;
        border-radius: 15px !important;
        border: 2px solid #f1f5f9 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        justify-content: center !important;
        margin: 0 !important;
        transition: all 0.2s ease-in-out;
    }

    /* ホバー時の効果 */
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        border-color: #37b7c4 !important;
        transform: translateY(-2px);
    }

    /* 選択された状態のデザイン */
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #f0fdfa !important; /* 非常に薄い青緑 */
        border-color: #37b7c4 !important;
        color: #37b7c4 !important;
    }

    /* 文字のデザインを中央揃えに */
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        text-align: center !important;
    }

    /* デフォルトの丸いチェックボックスを隠す */
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }
</style>
"""