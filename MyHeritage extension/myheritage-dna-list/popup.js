const status = document.getElementById("status");

function setStatus(msg) {
  status.textContent = msg;
}

document.getElementById("reset").onclick = async () => {
  await chrome.storage.local.set({ allMatches: [] });
  setStatus("Reset complete.");
};

document.getElementById("scrape").onclick = async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  const result = await chrome.tabs.sendMessage(tab.id, { action: "scrape" });

  if (result && result.matches) {
    const stored = (await chrome.storage.local.get("allMatches")).allMatches || [];
    const updated = stored.concat(result.matches);
    await chrome.storage.local.set({ allMatches: updated });
    setStatus(`Added ${result.matches.length}. Total: ${updated.length}`);
  } else {
    setStatus("No matches found on this page.");
  }
};

document.getElementById("download").onclick = async () => {
  const stored = (await chrome.storage.local.get("allMatches")).allMatches || [];
  const blob = new Blob([JSON.stringify(stored, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "myheritage_all_matches.json";
  a.click();

  URL.revokeObjectURL(url);
  setStatus(`Downloaded ${stored.length} matches.`);
};
