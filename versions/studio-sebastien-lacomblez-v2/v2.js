(() => {
  const scrollButton = document.querySelector(".v2-scroll");
  const content = document.querySelector("#content");
  const heroVideo = document.querySelector(".v2-hero__video");

  if (scrollButton && content) {
    scrollButton.addEventListener("click", () => {
      content.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  if (heroVideo) {
    const attemptPlay = () => {
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

    heroVideo.addEventListener("loadedmetadata", attemptPlay);
    heroVideo.addEventListener("canplay", attemptPlay);
    window.addEventListener("pageshow", attemptPlay);
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "visible" && heroVideo.paused) {
        attemptPlay();
      }
    });

    const unlockAutoplay = () => {
      if (heroVideo.paused) {
        attemptPlay();
      }
    };

    window.addEventListener("touchstart", unlockAutoplay, { passive: true, once: true });
    window.addEventListener("pointerdown", unlockAutoplay, { passive: true, once: true });
    window.addEventListener("keydown", unlockAutoplay, { once: true });

    attemptPlay();
  }

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && window.parent !== window) {
      window.parent.postMessage({ type: "close-site-viewer" }, window.location.origin);
    }
  });
})();
