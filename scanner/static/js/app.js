document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("wasteImage");
  const captureButton = document.getElementById('captureWaste');
  const cameraInput = document.getElementById('cameraInput');
  const uploadZone = document.getElementById("uploadZone");
  const uploadContent = document.getElementById("uploadContent");
  const previewImage = document.getElementById("previewImage");
  const clearButton = document.getElementById("clearImage");
  const form = document.getElementById("classifierForm");
  const resultPanel = document.getElementById("resultPanel");

  if (!fileInput) return;

  captureButton.addEventListener('click', () => {
    cameraInput.click();
});

cameraInput.addEventListener('change', () => {
    const file = cameraInput.files[0];

    if (!file) return;

    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;

    showPreview(file);
});

  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (!file) return;
    showPreview(file);
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    uploadZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      uploadZone.classList.add("dragging");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    uploadZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      uploadZone.classList.remove("dragging");
    });
  });

  uploadZone.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files[0];
    if (!file || !file.type.startsWith("image/")) return;
    fileInput.files = e.dataTransfer.files;
    showPreview(file);
  });

  clearButton.addEventListener("click", () => {
    fileInput.value = "";
    previewImage.src = "";
    previewImage.classList.add("d-none");
    uploadContent.classList.remove("d-none");
    resultPanel.innerHTML = `<div class="result-placeholder"><i class="fa-solid fa-chart-simple"></i><div><strong>Awaiting image</strong><span>Classification result will appear here.</span></div></div>`;
  });

 form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const file = fileInput.files[0];

    if (!file) {
        resultPanel.innerHTML = `
            <div class="result-placeholder">
                <i class="fa-solid fa-circle-exclamation"></i>
                <div>
                    <strong>Select an image first</strong>
                    <span>Upload a waste image before running classification.</span>
                </div>
            </div>
        `;
        return;
    }

    resultPanel.innerHTML = `
        <div class="result-placeholder">
            <i class="fa-solid fa-spinner fa-spin"></i>
            <div>
                <strong>Analyzing waste...</strong>
                <span>AI model is classifying your image.</span>
            </div>
        </div>
    `;

    const formData = new FormData(form);

    try {
        const response = await fetch("", {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        const html = await response.text();

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        const newResult = doc.querySelector("#resultPanel");

        if (newResult) {
            resultPanel.innerHTML = newResult.innerHTML;
        } else {
            resultPanel.innerHTML = `
                <div class="result-placeholder">
                    <i class="fa-solid fa-circle-exclamation"></i>
                    <div>
                        <strong>Something went wrong</strong>
                        <span>Could not read the classification result.</span>
                    </div>
                </div>
            `;
        }

    } catch (error) {
        console.error(error);

        resultPanel.innerHTML = `
            <div class="result-placeholder">
                <i class="fa-solid fa-circle-exclamation"></i>
                <div>
                    <strong>Classification failed</strong>
                    <span>Please try again.</span>
                </div>
            </div>
        `;
    }
});

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      previewImage.classList.remove("d-none");
      uploadContent.classList.add("d-none");
    };
    reader.readAsDataURL(file);
  }

  // Smoothly close the Bootstrap mobile menu after a navigation click.
  document.querySelectorAll(".mobile-link").forEach((link) => {
    link.addEventListener("click", () => {
      const canvas = bootstrap.Offcanvas.getInstance(
        document.getElementById("mobileMenu"),
      );
      if (canvas) canvas.hide();
    });
  });
});
