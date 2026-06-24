const API_BASE = "http://localhost:5000/api";

let savedAds = JSON.parse(localStorage.getItem("savedAds") || "[]");

document.addEventListener("DOMContentLoaded", () => {
    loadTonesPlatformsAndAuthenticity();
    renderSavedAds();

    document.getElementById("adForm").addEventListener("submit", handleGenerate);
    document.getElementById("regenerateBtn").addEventListener("click", handleGenerate);
    document.getElementById("saveBtn").addEventListener("click", saveCurrentAd);
});

async function loadTonesPlatformsAndAuthenticity() {
    try {
        const [tonesRes, platformsRes, authRes] = await Promise.all([
            fetch(`${API_BASE}/tones`),
            fetch(`${API_BASE}/platforms`),
            fetch(`${API_BASE}/authenticity`),
        ]);
        const tonesData = await tonesRes.json();
        const platformsData = await platformsRes.json();
        const authData = await authRes.json();

        const toneSelect = document.getElementById("tone");
        tonesData.tones.forEach((tone) => {
            const opt = document.createElement("option");
            opt.value = tone;
            opt.textContent = tone.charAt(0).toUpperCase() + tone.slice(1);
            toneSelect.appendChild(opt);
        });

        const platformSelect = document.getElementById("platform");
        platformsData.platforms.forEach((platform) => {
            const opt = document.createElement("option");
            opt.value = platform;
            opt.textContent = platform.charAt(0).toUpperCase() + platform.slice(1);
            platformSelect.appendChild(opt);
        });

        const authSelect = document.getElementById("authenticity");
        authData.authenticity.forEach((level) => {
            const opt = document.createElement("option");
            opt.value = level;
            opt.textContent = level.charAt(0).toUpperCase() + level.slice(1);
            authSelect.appendChild(opt);
        });
    } catch (err) {
        console.warn("Could not load tones/platforms/authenticity from backend, using defaults.");
    }
}

async function handleGenerate(e) {
    if (e) e.preventDefault();

    const productName = document.getElementById("productName").value.trim();
    const productDesc = document.getElementById("productDesc").value.trim();
    const targetAudience = document.getElementById("targetAudience").value.trim();
    const tone = document.getElementById("tone").value;
    const platform = document.getElementById("platform").value;
    const authenticity = document.getElementById("authenticity").value;
    const errorEl = document.getElementById("errorMessage");
    const spinner = document.getElementById("spinner");
    const outputSection = document.getElementById("outputSection");
    const generateBtn = document.getElementById("generateBtn");
    const regenerateBtn = document.getElementById("regenerateBtn");

    errorEl.classList.remove("visible");
    errorEl.textContent = "";

    if (!productName || !productDesc || !targetAudience) {
        errorEl.textContent = "Please fill in all required fields (Product Name, Description, and Target Audience).";
        errorEl.classList.add("visible");
        return;
    }

    spinner.classList.add("active");
    outputSection.classList.remove("visible");
    generateBtn.disabled = true;
    regenerateBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                product_name: productName,
                product_desc: productDesc,
                target_audience: targetAudience,
                tone: tone,
                platform: platform,
                authenticity: authenticity,
            }),
        });

        const data = await response.json();

        if (!data.success) {
            errorEl.textContent = data.errors ? data.errors.join(" ") : "Failed to generate ad copy.";
            errorEl.classList.add("visible");
            return;
        }

        if (data.warning) {
            console.warn(data.warning);
        }

        displayAd(data.ad);
    } catch (err) {
        errorEl.textContent = "Could not connect to the server. Make sure the backend is running.";
        errorEl.classList.add("visible");
    } finally {
        spinner.classList.remove("active");
        generateBtn.disabled = false;
        regenerateBtn.disabled = false;
    }
}

function displayAd(ad) {
    document.getElementById("adHeadline").textContent = ad.headline || "";
    document.getElementById("adDescription").textContent = ad.description || "";
    document.getElementById("adCta").textContent = ad.cta || "";

    const hashtagsContainer = document.getElementById("adHashtags");
    hashtagsContainer.innerHTML = "";
    if (ad.hashtags && Array.isArray(ad.hashtags)) {
        ad.hashtags.forEach((tag) => {
            const span = document.createElement("span");
            span.textContent = tag.startsWith("#") ? tag : `#${tag}`;
            hashtagsContainer.appendChild(span);
        });
    }

    document.getElementById("outputSection").classList.add("visible");

    window.currentAd = ad;
}

function saveCurrentAd() {
    if (!window.currentAd) return;

    const ad = {
        ...window.currentAd,
        id: Date.now(),
        savedAt: new Date().toLocaleString(),
    };

    savedAds.unshift(ad);
    if (savedAds.length > 20) savedAds.pop();
    localStorage.setItem("savedAds", JSON.stringify(savedAds));
    renderSavedAds();
}

function renderSavedAds() {
    const container = document.getElementById("savedAdsList");
    container.innerHTML = "";

    if (savedAds.length === 0) {
        container.innerHTML = '<p style="color: #999;">No saved ads yet.</p>';
        return;
    }

    savedAds.forEach((ad) => {
        const div = document.createElement("div");
        div.className = "saved-ad-item";
        div.innerHTML = `
            <div class="ad-preview">
                <strong>${escapeHtml(ad.headline || "")}</strong>
                <span style="color: #888; font-size: 0.85em; display: block;">${escapeHtml(ad.savedAt || "")}</span>
            </div>
            <button class="delete-btn" data-id="${ad.id}">&times;</button>
        `;
        div.querySelector(".delete-btn").addEventListener("click", () => {
            savedAds = savedAds.filter((a) => a.id !== ad.id);
            localStorage.setItem("savedAds", JSON.stringify(savedAds));
            renderSavedAds();
        });
        container.appendChild(div);
    });
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
