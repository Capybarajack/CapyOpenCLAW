---
name: dogfood
description: 系統化探索並測試 Web 應用程式，以找出 bug、UX 問題與其他缺陷。當使用者要求「dogfood」、「QA」、「exploratory test」、「find issues」、「bug hunt」、「test this app/site/platform」或要你評估網站品質時使用。會產出可直接交付團隊的結構化報告，包含完整重現證據：逐步截圖、重現影片與詳細步驟。
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# Dogfood

系統化探索 Web 應用、找出問題，並為每個發現產生完整可重現證據的報告。

## 設定

只需要 **Target URL**。其他參數都有合理預設，除非使用者明確覆寫，否則使用預設。

| 參數 | 預設值 | 覆寫範例 |
|---|---|---|
| **Target URL** | _(required)_ | `vercel.com`, `http://localhost:3000` |
| **Session name** | 網域 slug（例：`vercel.com` -> `vercel-com`） | `--session my-session` |
| **Output directory** | `./dogfood-output/` | `Output directory: /tmp/qa` |
| **Scope** | 全站/整個應用 | `Focus on the billing page` |
| **Authentication** | None | `Sign in to user@example.com` |

若使用者說「dogfood vercel.com」這類指令，直接用預設啟動。只有在提到需要登入但未提供憑證時，才追問。

優先使用 `agent-browser` 直接執行，不要用 `npx agent-browser`。直接 binary 會走 Rust client，`npx` 會經過 Node.js，速度較慢。

## 工作流程

```
1. Initialize    建立 session、輸出目錄、報告檔
2. Authenticate  需要時登入並儲存狀態
3. Orient        到起始頁並做初始快照
4. Explore       系統化走訪頁面與功能
5. Document      發現 issue 當下立刻截圖/錄影/寫報告
6. Wrap up       更新統計、關閉 session
```

### 1. Initialize

```bash
mkdir -p {OUTPUT_DIR}/screenshots {OUTPUT_DIR}/videos
```

複製報告模板到輸出目錄並填寫 header：

```bash
cp {SKILL_DIR}/templates/dogfood-report-template.md {OUTPUT_DIR}/report.md
```

啟動命名 session：

```bash
agent-browser --session {SESSION} open {TARGET_URL}
agent-browser --session {SESSION} wait --load networkidle
```

### 2. Authenticate

若應用需要登入：

```bash
agent-browser --session {SESSION} snapshot -i
# 找到登入欄位 refs，填入憑證
agent-browser --session {SESSION} fill @e1 "{EMAIL}"
agent-browser --session {SESSION} fill @e2 "{PASSWORD}"
agent-browser --session {SESSION} click @e3
agent-browser --session {SESSION} wait --load networkidle
```

若有 OTP / email code：向使用者索取，取得後再輸入。

登入成功後儲存狀態：

```bash
agent-browser --session {SESSION} state save {OUTPUT_DIR}/auth-state.json
```

### 3. Orient

先做標註截圖與快照，理解應用結構：

```bash
agent-browser --session {SESSION} screenshot --annotate {OUTPUT_DIR}/screenshots/initial.png
agent-browser --session {SESSION} snapshot -i
```

辨識主導覽並規劃走訪區域。

### 4. Explore

先讀 [references/issue-taxonomy.md](references/issue-taxonomy.md) 來校準分類、嚴重度與檢查清單。

**策略（系統化探索）：**

- 從主導覽開始，走訪每個第一層區塊。
- 在每個區塊測互動元件：按鈕、表單、下拉、modal。
- 測邊界情境：empty/error/boundary inputs。
- 走真實 end-to-end 流程（create/edit/delete）。
- 定期檢查 console errors。

**每頁建議動作：**

```bash
agent-browser --session {SESSION} snapshot -i
agent-browser --session {SESSION} screenshot --annotate {OUTPUT_DIR}/screenshots/{page-name}.png
agent-browser --session {SESSION} errors
agent-browser --session {SESSION} console
```

把時間集中在核心流程；邊角頁面可較淺探索。若某區塊問題密集，往下深挖。

### 5. Document Issues（以可重現為核心）

第 4 步與第 5 步要同步：找到問題就立刻記錄，不要最後一次補寫。

每個 issue 都要可重現。不是「有看到就記」，而是要能「讓他人看證據就能重跑」。

#### A) 互動/行為型問題（functional/ux/動作後錯誤）

需要完整重現：影片 + 逐步截圖。

1. 重現前先開始錄影：

```bash
agent-browser --session {SESSION} record start {OUTPUT_DIR}/videos/issue-{NNN}-repro.webm
```

2. 以人類可讀節奏操作，步驟間停 1–2 秒，且每步截圖：

```bash
agent-browser --session {SESSION} screenshot {OUTPUT_DIR}/screenshots/issue-{NNN}-step-1.png
sleep 1
# Perform action
sleep 1
agent-browser --session {SESSION} screenshot {OUTPUT_DIR}/screenshots/issue-{NNN}-step-2.png
sleep 1
```

3. 出錯狀態停留一下，再做標註截圖：

```bash
sleep 2
agent-browser --session {SESSION} screenshot --annotate {OUTPUT_DIR}/screenshots/issue-{NNN}-result.png
```

4. 結束錄影：

```bash
agent-browser --session {SESSION} record stop
```

5. 在報告中寫可對應截圖的編號步驟。

#### B) 靜態可見問題（typo、版面裁切、載入即錯）

單張標註截圖即可，不需要影片：

```bash
agent-browser --session {SESSION} screenshot --annotate {OUTPUT_DIR}/screenshots/issue-{NNN}.png
```

報告內描述問題，`Repro Video` 填 `N/A`。

---

**所有 issue 都必須做到：**

1. 立刻 append 到 report（避免中斷遺失）。
2. 立刻遞增 issue 編號（ISSUE-001, ISSUE-002...）。

### 6. Wrap Up

目標是 **5–10 個高品質 issue**。證據深度比數量重要。

結束前：

1. 重讀報告，校正 severity 統計要與 `### ISSUE-` 區塊一致。
2. 關閉 session：

```bash
agent-browser --session {SESSION} close
```

3. 回覆使用者：報告已完成，附總數、嚴重度分佈與最關鍵項目。

## 執行指引

- **重現是核心**：互動問題要影片+步驟截圖；靜態問題單張標註即可。
- **先確認可重現，再蒐證**：至少重試一次；不可穩定重現就不算有效 issue。
- **靜態問題不要硬錄影**：節省時間，聚焦高價值證據。
- **互動問題每一步都要圖**：before/action/after 缺一不可。
- **步驟需能對圖**：讀者不開瀏覽器也看得懂發生什麼事。
- **snapshot 指令用對**：
  - `snapshot -i`：找互動元素（button/input/link）
  - `snapshot`：讀頁面內容（文字/標題/資料）
- **完整但有判斷力**：不是跑死腳本，而是像真實使用者探索。
- **增量記錄，不要最後一次補寫**。
- **不要刪除輸出檔**：不 `rm` 截圖/影片/報告，不重開 session 回頭重做。
- **不要讀被測 App 原始碼**：以使用者視角驗證，不做原始碼審計。
- **定期看 console**：很多問題 UI 看不出來。
- **像人一樣操作**：走完整流程，輸入合理資料。
- **錄影時打字用 `type`**：`fill` 只在非錄影時追求速度。
- **影片要能被人看懂**：動作間 `sleep 1`，結果前 `sleep 2`。
- **命令效率**：能合併就合併；捲動用 `agent-browser --session {SESSION} scroll down 300`，不要用 `key`/`evaluate` 捲動。

## 參考資料

| Reference | 使用時機 |
|---|---|
| [references/issue-taxonomy.md](references/issue-taxonomy.md) | 開始測試前，校準檢查維度與嚴重度 |

## 模板

| Template | 用途 |
|---|---|
| [templates/dogfood-report-template.md](templates/dogfood-report-template.md) | 複製到輸出目錄作為報告起始檔 |
