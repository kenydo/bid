document.addEventListener("DOMContentLoaded", function() {
  const mainImage = document.getElementById("mainImage");
  const thumbnails = document.querySelectorAll("#thumbnails .thumbnail-img");

  thumbnails.forEach(function(thumb) {
    thumb.addEventListener("click", function() {
      // Schimbă poza principală
      mainImage.src = this.src;

      // Scoate clasa activă de pe toate
      thumbnails.forEach(t => t.classList.remove("thumb-active"));
      // Pune clasa activă pe thumbnail-ul selectat
      this.classList.add("thumb-active");
    });
  });
});