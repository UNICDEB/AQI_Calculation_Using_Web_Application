const form = document.getElementById("uploadForm");
const status = document.getElementById("status");
const downloadBtn = document.getElementById("downloadBtn");

form.onsubmit = async (e) => {
    e.preventDefault();
    status.innerText = "Processing...";
    downloadBtn.style.display = "none";

    const res = await fetch("/process/", {
        method: "POST",
        body: new FormData(form)
    });

    const data = await res.json();

    if (data.status === "success") {
        status.innerText = "Processing completed ✔";
        downloadBtn.style.display = "block";
    } else {
        status.innerText = "Processing failed ❌";
    }
};

downloadBtn.onclick = () => {
    window.location.href = "/download/";
};
