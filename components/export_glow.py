import json

import streamlit.components.v1 as components


def render_download_button_glow(labels: list[str]) -> None:
    labels_json = json.dumps(labels)
    components.html(
        f"""
        <script>
        (function () {{
            const parentDoc = window.parent.document;
            const labels = new Set({labels_json});
            const styleId = "cogniloop-download-glow-style";

            let style = parentDoc.getElementById(styleId);
            if (!style) {{
                style = parentDoc.createElement("style");
                style.id = styleId;
                parentDoc.head.appendChild(style);
            }}
            style.textContent = `
                .cogniloop-download-glow {{
                    border-color: rgba(46, 160, 67, 0.78) !important;
                    box-shadow:
                        0 0 0 1px rgba(46, 160, 67, 0.18),
                        0 0 18px rgba(46, 160, 67, 0.26) !important;
                    animation: cogniloopDownloadGlow 1.9s ease-in-out infinite;
                }}
                .cogniloop-download-glow:hover {{
                    border-color: rgba(63, 185, 80, 0.96) !important;
                    box-shadow:
                        0 0 0 1px rgba(63, 185, 80, 0.28),
                        0 0 24px rgba(63, 185, 80, 0.34) !important;
                }}
                @keyframes cogniloopDownloadGlow {{
                    0%, 100% {{
                        box-shadow:
                            0 0 0 1px rgba(46, 160, 67, 0.12),
                            0 0 12px rgba(46, 160, 67, 0.18);
                    }}
                    50% {{
                        box-shadow:
                            0 0 0 1px rgba(46, 160, 67, 0.26),
                            0 0 23px rgba(46, 160, 67, 0.35);
                    }}
                }}
            `;

            function applyGlow() {{
                parentDoc.querySelectorAll("button").forEach((button) => {{
                    const text = (button.innerText || button.textContent || "").trim();
                    if (labels.has(text)) {{
                        button.classList.add("cogniloop-download-glow");
                    }}
                }});
            }}

            applyGlow();
            setTimeout(applyGlow, 120);
            setTimeout(applyGlow, 450);
            const observer = new MutationObserver(applyGlow);
            observer.observe(parentDoc.body, {{ childList: true, subtree: true }});
            setTimeout(() => observer.disconnect(), 3500);
        }})();
        </script>
        """,
        height=0,
    )
