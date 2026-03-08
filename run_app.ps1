$python = "C:\Users\dell\AppData\Local\Programs\Python\Python312\python.exe"

if (!(Test-Path $python)) {
    Write-Error "Python not found at $python. Install Python first."
    exit 1
}

& $python -m pip install -r "$PSScriptRoot\requirements.txt"
& $python -m streamlit run "$PSScriptRoot\app.py"
