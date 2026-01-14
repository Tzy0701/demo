from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pathlib import Path
import time
import json

app = FastAPI()

BASE_DIR = Path("results/captures")

# -------- 手机拍照页面 --------
@app.get("/capture/{username}/{finger_key}")
def capture_page(username: str, finger_key: str):
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Touchless Capture</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="text-align:center;font-family:Arial;">
        <h2>Capture Finger: {finger_key}</h2>
        
        <input 
            type="file" 
            accept="image/*" 
            capture="environment"
            id="cameraInput"
            style="font-size:20px;"
        >
        
        <p id="status"></p>

        <script>
        const input = document.getElementById("cameraInput");
        const status = document.getElementById("status");

        input.addEventListener("change", async () => {{
            const file = input.files[0];
            if (!file) return;

            status.innerText = "Uploading...";

            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch("/upload/{username}/{finger_key}", {{
                method: "POST",
                body: formData
            }});

            const result = await response.json();

            if (result.success) {{
                status.innerText = "✅ Upload successful. You may close this page.";
            }} else {{
                status.innerText = "❌ Upload failed.";
            }}
        }});
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)


# -------- 接收上传图片 --------
@app.post("/upload/{username}/{finger_key}")
async def upload_image(username: str, finger_key: str, file: UploadFile = File(...)):

    username = username.replace(" ", "_")
    folder = BASE_DIR / username / finger_key
    folder.mkdir(parents=True, exist_ok=True)

    img_path = folder / "touchless_capture.jpg"

    contents = await file.read()
    with open(img_path, "wb") as f:
        f.write(contents)

    # 保存简单 metadata
    metadata = {
        "username": username,
        "finger_key": finger_key,
        "timestamp": time.time(),
        "image_path": str(img_path),
        "mode": "touchless"
    }

    with open(folder / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    return {"success": True}
