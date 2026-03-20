function scrapePage() {
  const cards = document.querySelectorAll('.dna_match_card');
  const results = [];

  cards.forEach(card => {
    const nameEl = card.querySelector('a.profile_name');
    const name = nameEl ? nameEl.textContent.trim() : null;

    let age = null;
    let from = null;
    const detailProps = card.querySelectorAll('.default_profile_details_properties .detail_property');
    detailProps.forEach(prop => {
      const field = prop.querySelector('.detail_field');
      const value = prop.querySelector('.detail_value');
      if (!field || !value) return;
      const label = field.textContent.trim();
      const valText = value.textContent.trim();
      if (label.startsWith('Age')) age = valText;
      if (label.startsWith('From')) from = valText;
    });

    const relBtn = card.querySelector('.possible_relationships_text button');
    const relationship = relBtn ? relBtn.textContent.trim() : null;

    const sharedPercentEl = card.querySelector('[data-automations="QualitySharedDnaPer"]');
    const sharedCmEl = card.querySelector('[data-automations="QualitySharedDnaTotal"]');
    const segmentsEl = card.querySelector('[data-automations="QualitySharedSegmentsTotal"]');
    const largestSegEl = card.querySelector('[data-automations="QualityLargestSegmentTotal"]');

    const sharedPercent = sharedPercentEl ? sharedPercentEl.textContent.trim() : null;
    const sharedCm = sharedCmEl ? sharedCmEl.textContent.trim() : null;
    const sharedSegments = segmentsEl ? segmentsEl.textContent.trim() : null;
    const largestSegmentCm = largestSegEl ? largestSegEl.textContent.trim() : null;

    const reviewLink = card.querySelector('a[href*="#dnamatch-"]');
    const reviewHref = reviewLink ? reviewLink.getAttribute('href') : null;

    results.push({
      name,
      age,
      from,
      relationship,
      sharedPercent,
      sharedCm,
      sharedSegments,
      largestSegmentCm,
      reviewHref
    });
  });

  return results;
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "scrape") {
    const matches = scrapePage();
    sendResponse({ matches });
  }
});
