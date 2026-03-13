---
name: context-hub-openclaw
description: 使用 Context Hub（chub CLI）為 OpenClaw 的開發任務提供最新、可追溯的第三方 API/SDK 文件來源，降低 API 幻覺與版本誤用。當使用者要求「串接某 API/SDK」、「依官方文件實作」、「修正因文件落差造成的錯誤」、或提到 Context Hub/chub 時使用。也用於把踩坑經驗以 annotate 持久化，讓後續 session 更快更準。
---

# Context Hub × OpenClaw（繁中）

使用 `chub` 先取文件，再寫程式；不要憑記憶猜 API。

## 核心目標

1. 以 `chub` 取得**當前版本**文件，避免過期知識。
2. 以 doc ID / 語言 / 版本建立**可追溯依據**。
3. 任務完成後把關鍵坑點寫入 `annotate`，形成可重用經驗。

## 標準流程（每次外部 API 任務都走）

### Step 1：搜尋正確文件 ID

```bash
chub search "<服務名或 SDK 名>" --json
```

執行要點：
- 優先選最貼近任務範圍的 ID（例如 `openai/chat-api`、`stripe/api`）。
- 若查無精準結果，先放寬關鍵字再搜一次。

### Step 2：抓取文件（語言優先與專案一致）

```bash
chub get <id> --lang <js|ts|py>
```

執行要點：
- 專案是 TS/JS 就優先 `--lang ts/js`；Python 專案用 `--lang py`。
- 若文件多檔案，先最小抓取；需要時再用：

```bash
chub get <id> --file <path>
chub get <id> --full
```

### Step 3：依文件實作或回覆

執行要點：
- 回答與程式碼都以 `chub get` 結果為準。
- 若文件與既有程式衝突，先指出差異，再提出遷移/修補方案。
- 需要範例時，優先使用文件中的參數名稱與錯誤處理模式。

### Step 4：任務收尾寫入註記（可選但強烈建議）

```bash
chub annotate <id> "<精簡且可行動的坑點/修正建議>"
```

註記規範：
- 一條只寫一個洞見，短而明確。
- 聚焦「容易踩坑且能直接避免失敗」的資訊。
- 不要重複文件已清楚說明的內容。

## 常用指令速查

```bash
chub search "stripe"
chub get stripe/api --lang ts
chub get openai/chat-api --lang py
chub annotate stripe/api "Webhook 驗簽需保留 raw body，不可先 JSON parse"
chub annotate --list
```

## 品質門檻（完成定義）

完成此技能流程時，應同時滿足：

1. 已明確引用 doc ID（必要時含語言/版本）。
2. 實作/建議可對應到文件內容，而非模型記憶。
3. 若本次有新坑點，已寫入 `annotate`（或明確說明無新增）。

## 邊界與安全

- `chub` 提供的是高品質來源，不等於絕對正確；關鍵改動仍需在專案內驗證。
- 不在未確認情況下自動送出 `chub feedback ...`；需先取得使用者同意。
- 不把敏感資訊（token、密碼、私有 URL）寫進註記文字。