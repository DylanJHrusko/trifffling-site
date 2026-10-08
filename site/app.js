// Same image runs in both environments; the hostname tells them apart.
const env = location.hostname.startsWith("qa.") ? "QA" : "Production";
document.getElementById("env").textContent = "Environment: " + env;
document.body.dataset.env = env.toLowerCase();

fetch("/version.json", { cache: "no-store" })
  .then((response) => response.json())
  .then((version) => {
    document.getElementById("commit").textContent =
      version.commit.slice(0, 7) + " (built " + version.built_at + ")";
  })
  .catch(() => {
    document.getElementById("commit").textContent = "unknown";
  });
