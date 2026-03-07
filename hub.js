(() => {
  const cards = Array.from(document.querySelectorAll(".site-card"));
  const viewer = document.querySelector(".site-viewer");
  const frame = document.querySelector(".site-viewer__frame");
  const viewerName = document.querySelector("[data-viewer-name]");
  const closeButton = document.querySelector(".site-viewer__close");
  const HASH_PREFIX = "#site=";

  if (!viewer || !frame || !cards.length) return;

  const cardById = new Map(cards.map((card) => [card.dataset.siteId, card]));

  const getIdFromHash = () => {
    if (!window.location.hash.startsWith(HASH_PREFIX)) return "";
    return decodeURIComponent(window.location.hash.slice(HASH_PREFIX.length));
  };

  const openSite = (card, { pushHash = true } = {}) => {
    const siteId = card.dataset.siteId || "";
    const siteUrl = card.dataset.siteUrl || "";
    const siteTitle = card.querySelector(".site-card__title")?.textContent?.trim() || "Version";
    if (!siteUrl) return;

    frame.src = siteUrl;
    if (viewerName) viewerName.textContent = siteTitle;
    viewer.hidden = false;
    viewer.setAttribute("aria-hidden", "false");
    document.body.classList.add("viewer-open");

    if (pushHash) {
      window.location.hash = `${HASH_PREFIX}${encodeURIComponent(siteId)}`;
    }
  };

  const closeSite = ({ clearHash = true } = {}) => {
    viewer.hidden = true;
    viewer.setAttribute("aria-hidden", "true");
    frame.src = "about:blank";
    document.body.classList.remove("viewer-open");

    if (clearHash && window.location.hash.startsWith(HASH_PREFIX)) {
      history.pushState("", document.title, window.location.pathname + window.location.search);
    }
  };

  cards.forEach((card) => {
    card.addEventListener("click", () => openSite(card));
  });

  closeButton?.addEventListener("click", () => closeSite());

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !viewer.hidden) {
      event.preventDefault();
      closeSite();
    }
  });

  window.addEventListener("message", (event) => {
    if (event.origin !== window.location.origin) return;
    if (event.data && event.data.type === "close-site-viewer") {
      closeSite();
    }
  });

  window.addEventListener("hashchange", () => {
    const siteId = getIdFromHash();
    if (!siteId) {
      closeSite({ clearHash: false });
      return;
    }

    const card = cardById.get(siteId);
    if (card) {
      openSite(card, { pushHash: false });
    }
  });

  const initialSiteId = getIdFromHash();
  if (initialSiteId) {
    const card = cardById.get(initialSiteId);
    if (card) openSite(card, { pushHash: false });
  }
})();
