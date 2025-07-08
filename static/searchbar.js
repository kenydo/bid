document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("auctionSearch");
  if (!searchInput) return;
  searchInput.addEventListener("input", function () {
    const filter = this.value.toLowerCase();
    const items = document.querySelectorAll("#auctionList li");
    items.forEach((item) => {
      const text =
        item.querySelector(".auction-title")?.textContent.toLowerCase() || "";
      if (text.includes(filter) || filter === "") {
        item.style.display = "";
      } else {
        item.style.display = "none";
      }
    });
  });
});