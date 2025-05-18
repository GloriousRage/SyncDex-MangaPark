;(function() {
  const SERVICE_KEY = "mp";
  const API = {
    fetchFollows: async () => {
      // MangaPark keeps your follows at /profile/<user>/follows
      const resp = await fetch(location.origin + "/profile/me/follows");
      const txt  = await resp.text();
      const dom  = new DOMParser().parseFromString(txt, "text/html");
      // selector for each followed manga—adjust to MP’s markup:
      return [...dom.querySelectorAll(".follow-list .item a")]
        .map(a => ({ title: a.textContent.trim(), url: a.href }));
    },

    setFollow: async (mangaUrl, shouldFollow) => {
      // MP uses an AJAX endpoint to (un)bookmark:
      // e.g. POST to /ajax/bookmark with { id: <mangaId>, action: "add"|"remove" }
      const idMatch = mangaUrl.match(/\/manga\/(\d+)/);
      if (!idMatch) throw new Error("Can't extract manga ID from " + mangaUrl);
      const form = new URLSearchParams();
      form.append("id", idMatch[1]);
      form.append("action", shouldFollow ? "add" : "remove");
      await fetch(location.origin + "/ajax/bookmark", {
        method:  "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body:    form.toString()
      });
    }
  };

  // Register with SyncDex’s loader:
  window.SyncDex.services.register({
    key:      SERVICE_KEY,
    name:     "MangaPark",
    fetch:    API.fetchFollows,
    update:   API.setFollow,
    iconPath: browser.runtime.getURL("icons/mp.png")
  });
})();
