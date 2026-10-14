// Al darle a un vídeo, se paran los demás.
document.addEventListener('play', (evento) => {
  for (const video of document.querySelectorAll('video')) {
    if (video !== evento.target) video.pause();
  }
}, true);
