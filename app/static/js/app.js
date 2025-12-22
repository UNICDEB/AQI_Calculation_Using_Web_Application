// const form = document.getElementById("uploadForm");
// const status = document.getElementById("status");
// const downloadBtn = document.getElementById("downloadBtn");

// form.onsubmit = async (e) => {
//     e.preventDefault();
//     status.innerText = "Processing...";
//     downloadBtn.style.display = "none";

//     const res = await fetch("/process/", {
//         method: "POST",
//         body: new FormData(form)
//     });

//     const data = await res.json();

//     if (data.status === "success") {
//         status.innerText = "Processing completed ✔";
//         downloadBtn.style.display = "block";
//     } else {
//         status.innerText = "Processing failed ❌";
//     }
// };

// downloadBtn.onclick = () => {
//     window.location.href = "/download/";
// };
const form = document.getElementById("uploadForm");
const statusText = document.getElementById("status");
const downloadBtn = document.getElementById("downloadBtn");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    statusText.innerHTML = "<span class='text-primary'>Processing data, please wait...</span>";
    downloadBtn.style.display = "none";

    const formData = new FormData(form);

    try {
        const response = await fetch("/process/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.status === "success") {
            statusText.innerHTML =
                "<span class='text-success'>Processing completed successfully.</span>";
            downloadBtn.style.display = "block";
        } else {
            statusText.innerHTML =
                "<span class='text-danger'>Processing failed. Please check files.</span>";
        }

    } catch (error) {
        statusText.innerHTML =
            "<span class='text-danger'>Server error occurred.</span>";
    }
});

downloadBtn.addEventListener("click", () => {
    window.location.href = "/download/";
});
