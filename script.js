(() => {
  const DEV_OPEN_CLASS = "dev-open";
  const HERO_WEIGHT_VAR = "--hero-title-weight";
  const DEFAULT_FONT_STACK = '"SangBleuOGSerifBody", "Times New Roman", serif';
  const FONT_STORAGE_KEY = "dev_font_variant";
  const FONT_FAVORITES_KEY = "dev_font_favorites";

  const scrollCue = document.querySelector(".scroll-cue");
  const content = document.querySelector("#content");
  const heroVideo = document.querySelector(".hero-video");
  const heroContent = document.querySelector(".hero-content");
  const heroTitle = document.querySelector(".hero-title");
  const heroTitleLines = document.querySelectorAll(".hero-title span");
  const reveals = document.querySelectorAll(".reveal");
  const devCorner = document.querySelector(".dev-corner");

  const heroWeightSlider = document.querySelector("#hero-title-weight");
  const heroWeightOutput = document.querySelector("#hero-title-weight-value");

  const fontPrevButton = document.querySelector("#font-variant-prev");
  const fontNextButton = document.querySelector("#font-variant-next");
  const fontFavoriteButton = document.querySelector("#font-variant-favorite");
  const fontLabel = document.querySelector("#font-variant-label");
  const favoritesContainer = document.querySelector("#font-favorites");

  const rootStyle = document.documentElement.style;
  const toggleDevTools = () => {
    const nowOpen = document.body.classList.toggle(DEV_OPEN_CLASS);
    if (devCorner) {
      devCorner.setAttribute("aria-expanded", String(nowOpen));
    }
  };

  const DEV_FONT_FILES = [
    "SB2_SangBleuEmpire-Black.otf",
    "SB2_SangBleuEmpire-BlackItalic.otf",
    "SB2_SangBleuEmpire-Bold.otf",
    "SB2_SangBleuEmpire-BoldItalic.otf",
    "SB2_SangBleuEmpire-Medium.otf",
    "SB2_SangBleuEmpire-MediumItalic.otf",
    "SB2_SangBleuEmpire-Regular.otf",
    "SB2_SangBleuEmpire-RegularItalic.otf",
    "SB2_SangBleuKingdom-Air.otf",
    "SB2_SangBleuKingdom-AirItalic.otf",
    "SB2_SangBleuKingdom-Bold.otf",
    "SB2_SangBleuKingdom-BoldItalic.otf",
    "SB2_SangBleuKingdom-Light.otf",
    "SB2_SangBleuKingdom-LightItalic.otf",
    "SB2_SangBleuKingdom-Medium.otf",
    "SB2_SangBleuKingdom-MediumItalic.otf",
    "SB2_SangBleuKingdom-Regular.otf",
    "SB2_SangBleuKingdom-RegularItalic.otf",
    "SB2_SangBleuRepublic-Bold.otf",
    "SB2_SangBleuRepublic-BoldItalic.otf",
    "SB2_SangBleuRepublic-Book.otf",
    "SB2_SangBleuRepublic-BookItalic.otf",
    "SB2_SangBleuRepublic-Medium.otf",
    "SB2_SangBleuRepublic-MediumItalic.otf",
    "SB2_SangBleuRepublic-Regular.otf",
    "SB2_SangBleuRepublic-RegularItalic.otf",
    "SB2_SangBleuSunrise-Air.otf",
    "SB2_SangBleuSunrise-AirItalic.otf",
    "SB2_SangBleuSunrise-Bold.otf",
    "SB2_SangBleuSunrise-BoldItalic.otf",
    "SB2_SangBleuSunrise-Light.otf",
    "SB2_SangBleuSunrise-LightItalic.otf",
    "SB2_SangBleuSunrise-Livre.otf",
    "SB2_SangBleuSunrise-Medium.otf",
    "SB2_SangBleuSunrise-MediumItalic.otf",
    "SB2_SangBleuSunrise-Regular.otf",
    "SB2_SangBleuSunrise-RegularItalic.otf",
    "SB2_SangBleuVersailles-Bold.otf",
    "SB2_SangBleuVersailles-BoldItalic.otf",
    "SB2_SangBleuVersailles-Book.otf",
    "SB2_SangBleuVersailles-BookItalic.otf",
    "SB2_SangBleuVersailles-Medium.otf",
    "SB2_SangBleuVersailles-MediumItalic.otf",
    "SB2_SangBleuVersailles-Regular.otf",
    "SB2_SangBleuVersailles-RegularItalic.otf",
    "SBOG_SangBleuOGCond-Hairline.ttf",
    "SBOG_SangBleuOGSans-Black.ttf",
    "SBOG_SangBleuOGSans-BlackItalic.ttf",
    "SBOG_SangBleuOGSans-Bold.ttf",
    "SBOG_SangBleuOGSans-BoldItalic.ttf",
    "SBOG_SangBleuOGSans-Hairline.ttf",
    "SBOG_SangBleuOGSans-HairlineItalic.ttf",
    "SBOG_SangBleuOGSans-Light.ttf",
    "SBOG_SangBleuOGSans-LightItalic.ttf",
    "SBOG_SangBleuOGSans-Medium.ttf",
    "SBOG_SangBleuOGSans-MediumItalic.ttf",
    "SBOG_SangBleuOGSans-Regular.ttf",
    "SBOG_SangBleuOGSans-RegularItalic.ttf",
    "SBOG_SangBleuOGSerif-Black.ttf",
    "SBOG_SangBleuOGSerif-BlackItalic.ttf",
    "SBOG_SangBleuOGSerif-Bold.ttf",
    "SBOG_SangBleuOGSerif-BoldItalic.ttf",
    "SBOG_SangBleuOGSerif-Hairline.ttf",
    "SBOG_SangBleuOGSerif-HairlineItalic.ttf",
    "SBOG_SangBleuOGSerif-Light.ttf",
    "SBOG_SangBleuOGSerif-LightItalic.ttf",
    "SBOG_SangBleuOGSerif-Medium.ttf",
    "SBOG_SangBleuOGSerif-MediumItalic.ttf",
    "SBOG_SangBleuOGSerif-Regular.ttf",
    "SBOG_SangBleuOGSerif-RegularItalic.ttf",
  ];

  const FONT_VARIANTS = [
    {
      key: "default",
      label: "Default (SangBleuOGSerif-Regular)",
      source: "Base",
      url: "",
      format: "",
    },
    ...DEV_FONT_FILES.map((file) => {
      const source = file.startsWith("SB2_") ? "SangBleu 2.500" : "SangBleu OG 3.000";
      const format = file.endsWith(".otf") ? "opentype" : "truetype";
      const key = file.replace(/\.(otf|ttf)$/i, "");
      const label = key.replace(/^SB2_|^SBOG_/, "");
      return {
        key,
        label,
        source,
        url: `assets/fonts/variants/${file}`,
        format,
      };
    }),
  ];

  const fontIndexByKey = new Map(FONT_VARIANTS.map((variant, index) => [variant.key, index]));
  const loadedFontFamilies = new Map();
  let currentFontIndex = 0;
  let currentApplyToken = 0;

  const parseFavoriteKeys = () => {
    try {
      const raw = localStorage.getItem(FONT_FAVORITES_KEY);
      if (!raw) return new Set();
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) return new Set();
      return new Set(parsed.filter((key) => key !== "default" && fontIndexByKey.has(key)));
    } catch (_err) {
      return new Set();
    }
  };

  const favoriteKeys = parseFavoriteKeys();

  const saveFavorites = () => {
    localStorage.setItem(FONT_FAVORITES_KEY, JSON.stringify(Array.from(favoriteKeys)));
  };

  const fitHeroTitleToViewport = () => {
    if (!heroTitle || !heroContent || !heroTitleLines.length) return;

    heroTitle.style.fontSize = "";
    heroTitle.style.lineHeight = "";

    const contentRect = heroContent.getBoundingClientRect();
    const availableWidth = Math.max(1, contentRect.width * 0.92);
    const computedTitle = window.getComputedStyle(heroTitle);
    const baseFontSize = Number.parseFloat(computedTitle.fontSize) || 16;
    const baseLineHeight = Number.parseFloat(computedTitle.lineHeight) || baseFontSize;

    let maxLineWidth = 0;
    heroTitleLines.forEach((line) => {
      const width = line.getBoundingClientRect().width;
      if (width > maxLineWidth) maxLineWidth = width;
    });

    if (maxLineWidth > availableWidth) {
      const ratio = availableWidth / maxLineWidth;
      const fittedSize = Math.max(28, Math.floor(baseFontSize * ratio));
      const fittedLineHeight = Math.max(fittedSize * 0.9, Math.floor(baseLineHeight * ratio));
      heroTitle.style.fontSize = `${fittedSize}px`;
      heroTitle.style.lineHeight = `${fittedLineHeight}px`;
    }
  };

  const updateFavoriteButton = () => {
    if (!fontFavoriteButton) return;
    const key = FONT_VARIANTS[currentFontIndex]?.key;
    const starred = key && favoriteKeys.has(key);
    fontFavoriteButton.textContent = starred ? "★" : "☆";
    fontFavoriteButton.setAttribute("aria-label", starred ? "Remove from favorites" : "Add to favorites");
  };

  const renderFavorites = () => {
    if (!favoritesContainer) return;
    favoritesContainer.innerHTML = "";

    const favoritesInOrder = FONT_VARIANTS.filter((variant) => favoriteKeys.has(variant.key));
    if (!favoritesInOrder.length) {
      const empty = document.createElement("span");
      empty.className = "hero-dev-tools__favorites-empty";
      empty.textContent = "No favorites yet";
      favoritesContainer.append(empty);
      return;
    }

    favoritesInOrder.forEach((variant) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "hero-dev-tools__favorite-chip";
      chip.textContent = `★ ${variant.label}`;
      chip.title = `${variant.label} (${variant.source})`;
      chip.addEventListener("click", () => {
        void applyFontVariantByIndex(fontIndexByKey.get(variant.key) ?? 0, { persist: true });
      });
      favoritesContainer.append(chip);
    });
  };

  const updateFontVariantLabel = () => {
    if (!fontLabel) return;
    const variant = FONT_VARIANTS[currentFontIndex];
    fontLabel.textContent = `${variant.label} — ${variant.source}`;
    fontLabel.title = `${variant.label} (${variant.source})`;
    updateFavoriteButton();
  };

  const ensureFontLoaded = async (variant) => {
    if (variant.key === "default") return "default";
    const existing = loadedFontFamilies.get(variant.key);
    if (existing) return existing;

    const family = `DevSangBleu_${variant.key.replace(/[^a-z0-9_-]/gi, "_")}`;
    const face = new FontFace(
      family,
      `url("${variant.url}") format("${variant.format}")`
    );
    await face.load();
    document.fonts.add(face);
    loadedFontFamilies.set(variant.key, family);
    return family;
  };

  const applyFontVariantByIndex = async (index, { persist = true } = {}) => {
    const bounded = ((index % FONT_VARIANTS.length) + FONT_VARIANTS.length) % FONT_VARIANTS.length;
    currentFontIndex = bounded;
    updateFontVariantLabel();
    const variant = FONT_VARIANTS[currentFontIndex];
    const token = ++currentApplyToken;

    if (variant.key === "default") {
      rootStyle.setProperty("--font-main", DEFAULT_FONT_STACK);
      if (persist) localStorage.removeItem(FONT_STORAGE_KEY);
      fitHeroTitleToViewport();
      return;
    }

    try {
      const family = await ensureFontLoaded(variant);
      if (token !== currentApplyToken) return;
      rootStyle.setProperty("--font-main", `"${family}", "Times New Roman", serif`);
      if (persist) localStorage.setItem(FONT_STORAGE_KEY, variant.key);
      fitHeroTitleToViewport();
    } catch (error) {
      console.error("Unable to load font variant:", variant, error);
      if (token !== currentApplyToken) return;
      currentFontIndex = 0;
      rootStyle.setProperty("--font-main", DEFAULT_FONT_STACK);
      localStorage.removeItem(FONT_STORAGE_KEY);
      updateFontVariantLabel();
      fitHeroTitleToViewport();
    }
  };

  const setHeroWeight = (rawValue) => {
    const numeric = Number.parseInt(rawValue, 10);
    const safeValue = Number.isFinite(numeric) ? Math.min(700, Math.max(200, numeric)) : 400;
    rootStyle.setProperty(HERO_WEIGHT_VAR, String(safeValue));
    if (heroWeightSlider) heroWeightSlider.value = String(safeValue);
    if (heroWeightOutput) heroWeightOutput.textContent = String(safeValue);
    if (heroTitle) heroTitle.style.fontWeight = String(safeValue);
    fitHeroTitleToViewport();
    return safeValue;
  };

  if (scrollCue && content) {
    scrollCue.addEventListener("click", () => {
      content.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  setHeroWeight(heroWeightSlider?.value || "400");

  if (heroWeightSlider) {
    heroWeightSlider.addEventListener("input", (event) => {
      const target = event.target;
      if (target instanceof HTMLInputElement) {
        setHeroWeight(target.value);
      }
    });
  }

  renderFavorites();
  updateFontVariantLabel();

  if (fontPrevButton) {
    fontPrevButton.addEventListener("click", () => {
      void applyFontVariantByIndex(currentFontIndex - 1, { persist: true });
    });
  }

  if (fontNextButton) {
    fontNextButton.addEventListener("click", () => {
      void applyFontVariantByIndex(currentFontIndex + 1, { persist: true });
    });
  }

  if (fontFavoriteButton) {
    fontFavoriteButton.addEventListener("click", () => {
      const key = FONT_VARIANTS[currentFontIndex]?.key;
      if (!key || key === "default") return;
      if (favoriteKeys.has(key)) {
        favoriteKeys.delete(key);
      } else {
        favoriteKeys.add(key);
      }
      saveFavorites();
      updateFavoriteButton();
      renderFavorites();
    });
  }

  void applyFontVariantByIndex(0, { persist: false });

  if (devCorner) {
    devCorner.addEventListener("click", () => {
      toggleDevTools();
    });
  }

  window.addEventListener("keydown", (event) => {
    const key = typeof event.key === "string" ? event.key.toLowerCase() : "";
    if (event.ctrlKey && event.shiftKey && key === "d") {
      event.preventDefault();
      toggleDevTools();
    }
  });

  if (heroVideo) {
    const attemptHeroVideoPlay = () => {
      if (document.visibilityState === "hidden") return;
      const playPromise = heroVideo.play();
      if (playPromise && typeof playPromise.catch === "function") {
        playPromise.catch(() => {});
      }
    };

    heroVideo.muted = true;
    heroVideo.defaultMuted = true;
    heroVideo.autoplay = true;
    heroVideo.loop = true;
    heroVideo.playsInline = true;
    heroVideo.setAttribute("muted", "");
    heroVideo.setAttribute("autoplay", "");
    heroVideo.setAttribute("loop", "");
    heroVideo.setAttribute("playsinline", "");
    heroVideo.setAttribute("webkit-playsinline", "");

    heroVideo.addEventListener("loadedmetadata", attemptHeroVideoPlay);
    heroVideo.addEventListener("canplay", attemptHeroVideoPlay);
    window.addEventListener("pageshow", attemptHeroVideoPlay);
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "visible" && heroVideo.paused) {
        attemptHeroVideoPlay();
      }
    });

    const unlockAutoplay = () => {
      if (heroVideo.paused) {
        attemptHeroVideoPlay();
      }
    };

    window.addEventListener("touchstart", unlockAutoplay, { passive: true, once: true });
    window.addEventListener("pointerdown", unlockAutoplay, { passive: true, once: true });
    window.addEventListener("keydown", unlockAutoplay, { once: true });

    attemptHeroVideoPlay();
  }

  const onViewportChange = () => {
    fitHeroTitleToViewport();
  };

  window.addEventListener("resize", onViewportChange, { passive: true });
  if ("ResizeObserver" in window && (heroContent || heroTitle)) {
    const ro = new ResizeObserver(onViewportChange);
    ro.observe(heroContent || heroTitle);
  }

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(onViewportChange).catch(() => {});
  }

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.14,
        rootMargin: "0px 0px -6% 0px",
      }
    );

    reveals.forEach((element) => observer.observe(element));
  } else {
    reveals.forEach((element) => element.classList.add("visible"));
  }
})();
