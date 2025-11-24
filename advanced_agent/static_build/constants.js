// Models dropdown options
export const MODEL_OPTIONS = [
    { value: "", label: "Choose AI model…", disabled: true, selected: true },
    { value: "gpt-4o-mini", label: "GPT 4o Mini" },
    { value: "gpt-4o", label: "GPT 4o" },
    { value: "gpt-4.1-mini", label: "GPT 4.1 Mini" },
    { value: "gpt-4.1", label: "GPT 4.1" },
    { value: "gpt-5", label: "GPT 5" },
    { value: "gpt-5-mini", label: "GPT 5 Mini" },
    { value: "gpt-5.1", label: "GPT 5.1" },
    { value: "deepseek-chat", label: "Deepseek V3" },
];
// Humanization dropdown options
export const HUMANIZATION_OPTIONS = [
    { value: "", label: "Humanization Level...", disabled: true, selected: true },
    { value: "0.1", label: "Somewhat Robotic (Default)" },
    { value: "0.01", label: "Very Robotic" },
    { value: "0.3", label: "Human-ish" },
    { value: "0.5", label: "Very Human" },
];
// Map select.id -> option list
export const DROPDOWN_OPTIONS_BY_ID = {
    "model-select": MODEL_OPTIONS,
    humanization: HUMANIZATION_OPTIONS,
};
//# sourceMappingURL=constants.js.map