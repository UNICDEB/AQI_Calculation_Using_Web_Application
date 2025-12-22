document.getElementById("uploadForm").onsubmit = async (e) => {
    e.preventDefault();
    document.getElementById("status").innerText = "Processing...";

    const formData = new FormData(e.target);
    const response = await fetch("/process/", {
        method: "POST",
        body: formData
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = response.headers.get("content-disposition")
        ?.split("filename=")[1];
    a.click();

    document.getElementById("status").innerText = "Download complete";
};
