let mediaRecorder;
let audioChunks = [];
const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const uploadBtn = document.getElementById("uploadBtn");
const player = document.getElementById("player");
const resultEl = document.getElementById("result");

recordBtn.onclick = async () => {
  audioChunks = [];
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
  mediaRecorder.onstop = () => {
    const blob = new Blob(audioChunks, { type: "audio/webm" });
    const url = URL.createObjectURL(blob);
    player.src = url;
    uploadBtn.disabled = false;
    // store blob
    player._blob = blob;
  };
  mediaRecorder.start();
  recordBtn.disabled = true;
  stopBtn.disabled = false;
  resultEl.textContent = "Recording...";
};

stopBtn.onclick = () => {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
  recordBtn.disabled = false;
  stopBtn.disabled = true;
};

uploadBtn.onclick = async () => {
  const blob = player._blob;
  if (!blob) return;
  resultEl.textContent = "Uploading...";
  const form = new FormData();
  // backend expects file field named 'file'; convert webm to wav server-side if needed
  form.append("file", blob, "sample.webm");
  try {
    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: form
    });
    const data = await res.json();
    resultEl.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    resultEl.textContent = "Upload error: " + err;
  }
};
