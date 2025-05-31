const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let image = new Image();
let titik = [];

document.getElementById('fileInput').addEventListener('change', function (e) {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.onload = function (event) {
    image.onload = function () {
      canvas.width = image.width;
      canvas.height = image.height;
      ctx.drawImage(image, 0, 0);
      titik = [];
    };
    image.src = event.target.result;
  };
  reader.readAsDataURL(file);
});

canvas.addEventListener('click', function (e) {
  if (titik.length < 4) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    titik.push([x, y]);

    ctx.fillStyle = 'red';
    ctx.fillRect(x - 3, y - 3, 6, 6);

    if (titik.length === 4) {
      alert('4 titik sudah ditandai!');
    }
  }
});

function kirimData() {
  if (titik.length !== 4) {
    alert("Harus tandai 4 titik dulu!");
    return;
  }

  const kunci = document.getElementById('kunciJawaban').value;
  const file = document.getElementById('fileInput').files[0];
  const formData = new FormData();
  formData.append('gambar', file);
  formData.append('titik', JSON.stringify(titik));
  formData.append('kunci', kunci);

  fetch('/proses/', {
    method: 'POST',
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById('hasil').innerText = `Benar: ${data.benar}, Salah: ${data.salah}, Skor: ${data.skor}`;
    });
}
