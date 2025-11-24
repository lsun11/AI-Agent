// static/main.ts
import { DROPDOWN_OPTIONS_BY_ID } from "./configs.js";
class ChatUI {
    constructor() {
        this.currentTopicKey = null;
        this.isThinking = false;
        this.language = "Chn";
        const formEl = document.getElementById("chat-form");
        const inputEl = document.getElementById("chat-input");
        const messagesEl = document.getElementById("messages");
        if (!(formEl instanceof HTMLFormElement)) {
            throw new Error("chat-form element not found or not a form");
        }
        if (!(inputEl instanceof HTMLInputElement)) {
            throw new Error("chat-input element not found or not an input");
        }
        if (!(messagesEl instanceof HTMLDivElement)) {
            throw new Error("messages element not found or not a div");
        }
        this.form = formEl;
        this.input = inputEl;
        this.messagesEl = messagesEl;
        const button = this.form.querySelector("button");
        if (!(button instanceof HTMLButtonElement)) {
            throw new Error("Submit button not found");
        }
        this.submitButton = button;
        this.attachListeners();
        const languageSelectEl = this.addDropDown("language-select");
        if (!languageSelectEl) {
            throw new Error("Failed to create Language Select");
        }
        const modelSelectEl = this.addDropDown("model-select");
        if (!modelSelectEl) {
            throw new Error("Failed to create model-select dropdown");
        }
        const humanizationSelectEl = this.addDropDown("humanization");
        if (!humanizationSelectEl) {
            throw new Error("Failed to create humanization dropdown");
        }
        this.languageSelect = languageSelectEl;
        this.modelSelect = modelSelectEl;
        this.humanizationSelect = humanizationSelectEl;
        this.language = this.mapLanguageValue(this.languageSelect.value);
        this.updateInterfaceLanguage();
        this.addGreeting(this.language);
        this.languageSelect.addEventListener("change", () => {
            this.language = this.mapLanguageValue(this.languageSelect.value);
            console.log("!!!!", this.languageSelect.value);
            this.updateInterfaceLanguage();
            this.refreshDropdownLabels();
            const switchedMsg = this.language === "Chn"
                ? "🌐 已切换到中文界面"
                : "🌐 Switched to English interface";
            this.addMessage(switchedMsg, "greeting");
            this.addGreeting(this.language);
        });
    }
    mapLanguageValue(value) {
        // You can adjust this mapping to your actual config values
        if (value === "Chn" || value === "zh-CN" || value === "zh") {
            return "Chn";
        }
        return "Eng";
    }
    refreshDropdownLabels() {
        const ids = ["model-select", "humanization"]; // add "language-select" if you want to translate that too
        for (const id of ids) {
            const select = document.getElementById(id);
            if (!select)
                continue;
            for (const option of Array.from(select.options)) {
                const key = option.dataset.labelKey;
                if (key) {
                    option.textContent = this.translateLabel(key);
                }
            }
        }
    }
    translateLabel(key) {
        const translations = {
            "Choose AI model…": {
                Eng: "Choose AI model…",
                Chn: "选择 AI 模型…",
            },
            "Humanization Level...": {
                Eng: "Humanization Level...",
                Chn: "人性化程度…",
            },
            // you can add more later if needed
        };
        const langMap = translations[key];
        if (langMap && langMap[this.language]) {
            // @ts-ignore
            return langMap[this.language];
        }
        return key; // fallback
    }
    updateInterfaceLanguage() {
        if (this.language === "Chn") {
            // Input placeholder
            this.input.placeholder = "请输入你的问题…";
            // Submit button text
            this.submitButton.textContent = "发送";
            // Page title
            const titleEl = document.getElementById("app-title");
            if (titleEl) {
                titleEl.textContent = "AI 研究助手 — 开发者";
            }
            document.title = "AI 研究助手";
        }
        else {
            // English
            this.input.placeholder = "Ask me anything about dev tools, careers, etc…";
            this.submitButton.textContent = "Send";
            const titleEl = document.getElementById("app-title");
            if (titleEl) {
                titleEl.textContent = "AI Research Assistant — Developer Topics";
            }
            document.title = "AI Research Assistant";
        }
    }
    addGreeting(language) {
        const greeting_eng = "🤘Hello! I'm your AI Research Assistant for computer developing.\n\n" +
            "Ask me anything about: \n " +
            "📦 developer tools and software,\n " +
            "🏢 career as a developer,\n " +
            "💻 and any other dev related topics!\n\n" +
            "Just type your question below to get started.";
        const greeting_chn = "🤘你好\n\n" +
            "可以咨询我任何关于: \n " +
            "📦 开发者工具和软件,\n " +
            "🏢 程序员职业发展,\n " +
            "💻 和其他任何计算机相关的问题\n\n" +
            "请在下面输入你的问题";
        const target_greeting = language === "Eng" ? greeting_eng : greeting_chn;
        this.addMessage(target_greeting, "greeting");
    }
    addFollowupMsg() {
        const followupEng = "🤘Please let me know if you need anything else.";
        const followupChn = "🤘如果还有其他问题，欢迎继续提问。";
        const followup = this.language === "Chn" ? followupChn : followupEng;
        this.addMessage(followup, "greeting");
    }
    attachListeners() {
        this.form.addEventListener("submit", (event) => {
            event.preventDefault();
            this.handleSubmit();
        });
    }
    extractWebsiteUrl(text) {
        const lines = text.split("\n");
        for (const line of lines) {
            // English: "Website: https://..."
            const m1 = line.match(/Website[:：]\s*(https?:\/\/\S+)/i);
            // Chinese: "网站：https://..."
            const m2 = line.match(/网站[:：]\s*(https?:\/\/\S+)/i);
            const m = m1 || m2;
            if (m) {
                // @ts-ignore
                return m[1].trim().replace(/[)\]]+$/, "");
            }
        }
        return undefined;
    }
    addMessage(text, sender, url) {
        const div = document.createElement("div");
        div.className = `message ${sender}`;
        div.textContent = text;
        // Convert markdown --> HTML & sanitize it
        div.innerHTML = this.markdownToHtml(text);
        if (sender === "bot" && url) {
            div.classList.add("clickable");
            div.addEventListener("click", () => {
                window.open(url, "_blank");
            });
        }
        this.messagesEl.appendChild(div);
        this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
    }
    addDownloadButton(url) {
        const container = document.createElement("div");
        container.className = "download-container";
        const button = document.createElement("button");
        button.type = "button";
        button.className = "download-button";
        button.textContent = "Download summary";
        button.addEventListener("click", () => {
            window.open(url, "_blank");
        });
        container.appendChild(button);
        this.messagesEl.appendChild(container);
        this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
    }
    addDropDown(selectId) {
        const dropdownContainer = document.getElementById("dropdown-container");
        if (!dropdownContainer) {
            console.error("dropdown-container not found");
            return null;
        }
        const options = DROPDOWN_OPTIONS_BY_ID[selectId];
        if (!options) {
            console.warn(`No dropdown options configured for selectId="${selectId}"`);
            return null;
        }
        const select = document.createElement("select");
        select.id = selectId;
        select.className = selectId;
        for (const opt of options) {
            const optionEl = document.createElement("option");
            optionEl.value = opt.value;
            // store canonical label key (English)
            optionEl.dataset.labelKey = opt.label;
            // show translated label based on current language
            optionEl.textContent = this.translateLabel(opt.label);
            if (opt.disabled)
                optionEl.disabled = true;
            if (opt.selected)
                optionEl.selected = true;
            select.appendChild(optionEl);
        }
        dropdownContainer.appendChild(select);
        return select;
    }
    startThinking() {
        if (this.isThinking)
            return;
        this.isThinking = true;
        document.body.classList.add("thinking");
    }
    stopThinking() {
        if (!this.isThinking)
            return;
        this.isThinking = false;
        document.body.classList.remove("thinking");
    }
    updateTitle(topicLabel) {
        const titleEl = document.getElementById("app-title");
        if (titleEl) {
            titleEl.textContent = `AI Research Assistant — ${topicLabel}`;
        }
        document.title = `AI Research: ${topicLabel}`;
    }
    updateBackground(topicKey) {
        // Remove previous topic background, keep default if none yet
        if (this.currentTopicKey) {
            document.body.classList.remove(`topic-bg-${this.currentTopicKey}`);
        }
        document.body.classList.add(`topic-bg-${topicKey}`);
        this.currentTopicKey = topicKey;
    }
    splitReplyIntoBubbles(reply) {
        const lines = reply.split(/\r?\n/);
        const bubbles = [];
        let current = [];
        const flush = () => {
            const text = current.join("\n").trim();
            if (text) {
                bubbles.push(text);
            }
            current = [];
        };
        for (const rawLine of lines) {
            const line = rawLine; // keep original spacing
            const trimmed = rawLine.trim(); // for checks
            // Skip leading empty lines
            if (!trimmed && current.length === 0) {
                continue;
            }
            // 1) Top header bubble: "📊 Results for: ..."
            if (trimmed.startsWith("📊 Results for:")) {
                flush();
                current.push(line);
                continue;
            }
            // 2) New company bubble: "N. 🏢 ..."
            if (/^\d+\.\s*🏢/.test(trimmed)) {
                flush();
                current.push(line);
                continue;
            }
            // 3) Recommendations / Analysis bubble
            if (trimmed.startsWith("**Recommendations") ||
                trimmed.startsWith("**推荐")) {
                flush(); // finish the previous company bubble
                current.push(line); // start a new bubble with the recommendations header
                continue;
            }
            // 4) Everything else is part of the current bubble
            current.push(line);
        }
        flush();
        return bubbles;
    }
    markdownToHtml(text) {
        // Convert **bold** to <strong>bold</strong>
        const boldConverted = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
        // Convert bullet points `- something` → <li>
        const htmlWithBullets = boldConverted
            .replace(/^- (.*)/gm, "<li>$1</li>") // Convert lines starting with "- "
            .replace(/(<li>.*<\/li>)/g, "<ul>$1</ul>"); // Wrap consecutive li in <ul>
        return htmlWithBullets;
    }
    async handleSubmit() {
        const text = this.input.value.trim();
        if (!text)
            return;
        this.addMessage(text, "user");
        this.input.value = "";
        this.input.focus();
        this.submitButton.disabled = true;
        try {
            const model = this.modelSelect.value || "gpt-4o-mini"; // default if none chosen
            const temperature = this.humanizationSelect.value || "0.1";
            const language = this.languageSelect.value || "en-US";
            const params = new URLSearchParams({ message: text, model, temperature });
            const es = new EventSource(`/chat_stream?${params.toString()}`);
            // @ts-ignore store if you want to close later
            const thinkingMsg = this.language === "Chn"
                ? "🤔 正在思考，请稍候…"
                : "🤔 Start thinking, please wait...";
            this.addMessage(thinkingMsg, "greeting");
            //this.addMessage("🤔Start thinking, please wait...", "greeting");
            this.currentEventSource = es;
            es.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.type === "topic") {
                        // ✅ Update title & maybe background immediately
                        const topicLabel = data.topic_label;
                        const topicKey = data.topic_key;
                        this.updateTitle(topicLabel);
                        // Optionally defer background switch until you get final
                        this.updateBackground(topicKey);
                        this.startThinking();
                        return;
                    }
                    if (data.type === "log") {
                        // ✅ Streaming thinking messages
                        this.addMessage(data.message, "thinking");
                        return;
                    }
                    if (data.type === "final") {
                        // ✅ Final answer
                        const bubbles = this.splitReplyIntoBubbles(data.reply);
                        for (let i = 0; i < bubbles.length; i++) {
                            const style = i === 0 ? "bot-first" :
                                i === bubbles.length - 1 ? "bot-first" : "bot";
                            // @ts-ignore
                            const url = this.extractWebsiteUrl(bubbles[i]);
                            // @ts-ignore
                            this.addMessage(bubbles[i], style, url);
                        }
                        if (data.download_url) {
                            this.addDownloadButton(data.download_url);
                        }
                        if (data.topic_used) {
                            // Optionally update title again or background:
                            // this.updateTitle(data.topic_used);
                        }
                        // We're done, close stream:
                        es.close();
                        this.stopThinking();
                        this.addFollowupMsg();
                        this.submitButton.disabled = false;
                    }
                }
                catch (e) {
                    console.error("Error parsing SSE data", e, event.data);
                }
            };
            es.onerror = (err) => {
                console.error("SSE error:", err);
                this.addMessage("Error: connection lost.", "bot");
                es.close();
                this.submitButton.disabled = false;
            };
        }
        catch (error) {
            console.error(error);
            const msg = error instanceof Error ? error.message : String(error);
            this.addMessage(`Network error: ${msg}`, "bot");
            this.submitButton.disabled = false;
        }
    }
}
document.addEventListener("DOMContentLoaded", () => {
    new ChatUI();
});
//# sourceMappingURL=main_old.js.map