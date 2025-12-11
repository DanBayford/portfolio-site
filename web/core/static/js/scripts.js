document.addEventListener("DOMContentLoaded", function () {
  // Init syntax highlighter
  if (window.hljs) {
    window.hljs.highlightAll();
  } else {
    console.error("Highlight.js not loaded.");
  }
  // Add extra attributes to <a> tags in streamfields (ie external links)
  const streamFieldExternalLinks = document.querySelectorAll(".stream_field a");
  streamFieldExternalLinks.forEach((link) => {
    const isExternal =
      link.hostname && link.hostname !== window.location.hostname; // Check if external host
    if (isExternal) {
      link.target = "_blank";
      link.rel = "noopener norefferer";
    }
  });
});
