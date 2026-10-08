const scanButton = document.getElementById("scanButton");
const targetUrl = document.getElementById("targetUrl");

const loading = document.getElementById("loading");
const results = document.getElementById("results");
const errorBox = document.getElementById("errorBox");

const findingsContainer = document.getElementById("findingsContainer");
const aiAnalysis = document.getElementById("aiAnalysis");
const targetDisplay = document.getElementById("targetDisplay");


scanButton.addEventListener("click", scanWebsite);


targetUrl.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        scanWebsite();
    }
});


async function scanWebsite() {

    const url = targetUrl.value.trim();

    if (!url) {
        showError("Please enter a website URL.");
        return;
    }

    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        showError("Please enter a valid HTTP or HTTPS URL.");
        return;
    }

    hideError();
    results.classList.add("hidden");
    loading.classList.remove("hidden");

    scanButton.disabled = true;
    scanButton.textContent = "Scanning...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/scan",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    url: url
                })
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "The security scan failed."
            );
        }

        if (result.status !== "success") {
            throw new Error(
                "The security scan was not successful."
            );
        }

        displayResults(result.data);

    } catch (error) {

        showError(
            "Unable to complete the scan. " +
            error.message
        );

    } finally {

        loading.classList.add("hidden");

        scanButton.disabled = false;
        scanButton.textContent = "Scan Website";
    }
}


function displayResults(data) {

    results.classList.remove("hidden");

    targetDisplay.textContent =
        data.final_url || data.target || "";

    displayFindings(data.findings || []);

    aiAnalysis.textContent =
        data.ai_analysis ||
        "No AI analysis was returned.";
}


function displayFindings(findings) {

    findingsContainer.innerHTML = "";

    if (findings.length === 0) {

        findingsContainer.innerHTML = `
            <div class="finding-card">
                <div class="finding-header">
                    <h3>✓ No findings detected</h3>
                </div>

                <p>
                    No issues were detected by the current
                    WebSecAI security checks.
                </p>

                <p>
                    This does not mean the website is
                    completely secure.
                </p>
            </div>
        `;

        return;
    }


    findings.forEach(function (finding) {

        const severity =
            (finding.severity || "Info").toLowerCase();

        const severityClass =
            severity === "medium"
                ? "severity-medium"
                : severity === "low"
                    ? "severity-low"
                    : "";


        const card = document.createElement("div");

        card.className = "finding-card";


        card.innerHTML = `
            <div class="finding-header">

                <h3>
                    ${escapeHtml(
                        finding.header ||
                        finding.issue ||
                        finding.type ||
                        "Security Finding"
                    )}
                </h3>

                <span class="severity ${severityClass}">
                    ${escapeHtml(
                        finding.severity || "Info"
                    )}
                </span>

            </div>

            <p>
                ${escapeHtml(
                    finding.description ||
                    finding.issue ||
                    "Security issue detected."
                )}
            </p>

            <p class="recommendation">
                Recommendation:
                ${escapeHtml(
                    finding.recommendation ||
                    "Review the security configuration."
                )}
            </p>
        `;


        findingsContainer.appendChild(card);
    });
}


function showError(message) {

    errorBox.textContent = message;

    errorBox.classList.remove("hidden");

    results.classList.add("hidden");
}


function hideError() {

    errorBox.textContent = "";

    errorBox.classList.add("hidden");
}


function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}