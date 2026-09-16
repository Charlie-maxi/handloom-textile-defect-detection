# Shared dark theme for Fabric Detect

DARK_CSS = r"""
:root {
    color-scheme: dark;
}

html, body, .gradio-container {
    background: #0b1110 !important;
    color: #e8f1ed !important;
}

.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
}

/* Main panels and cards */
.gradio-container .block,
.gradio-container .panel,
.gradio-container .form,
.gradio-container .wrap,
.gradio-container .table-wrap {
    background: #111a18 !important;
    border-color: #263a34 !important;
}

/* Text */
.gradio-container h1,
.gradio-container h2,
.gradio-container h3,
.gradio-container h4,
.gradio-container p,
.gradio-container label,
.gradio-container span,
.gradio-container .markdown {
    color: #e8f1ed !important;
}

/* Inputs */
.gradio-container input,
.gradio-container textarea,
.gradio-container select,
.gradio-container .input-container,
.gradio-container .wrap.svelte-1w9m6k0 {
    background: #0f1715 !important;
    color: #f2f7f5 !important;
    border-color: #355149 !important;
}

.gradio-container input::placeholder,
.gradio-container textarea::placeholder {
    color: #8ea39b !important;
}

/* Buttons */
.gradio-container button {
    border-color: #355149 !important;
}

.gradio-container button.secondary,
.gradio-container button[variant="secondary"] {
    background: #18231f !important;
    color: #e8f1ed !important;
}

.gradio-container button.primary,
.gradio-container button[variant="primary"] {
    background: #15803d !important;
    color: white !important;
}

/* Tables */
.gradio-container table,
.gradio-container thead,
.gradio-container tbody,
.gradio-container tr,
.gradio-container th,
.gradio-container td {
    background: #111a18 !important;
    color: #e8f1ed !important;
    border-color: #2b413a !important;
}

/* Dropdowns / radios / checkboxes */
.gradio-container [role="listbox"],
.gradio-container [role="option"],
.gradio-container .options,
.gradio-container .choice {
    background: #111a18 !important;
    color: #e8f1ed !important;
}

/* File upload / webcam area */
.gradio-container .upload-container,
.gradio-container .image-container,
.gradio-container video {
    background: #0a100f !important;
    border-color: #355149 !important;
}

/* Links */
.gradio-container a {
    color: #6ee7a0 !important;
}

/* Horizontal separators */
.gradio-container hr {
    border-color: #2b413a !important;
}

/* Navigation HTML links already have inline colors; keep their text readable */
.gradio-container a[style] {
    color: white !important;
}
"""
