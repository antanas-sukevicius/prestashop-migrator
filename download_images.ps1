$imageUrlsFile = "C:\mages.txt"
$outputFolder = "C:\images"

if (!(Test-Path -Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder | Out-Null
}

$imageUrls = Get-Content $imageUrlsFile

foreach ($imageUrl in $imageUrls) {
    # Extract credentials if present in the URL
    if ($imageUrl -match 'https://([^@]+)@(.+)') {
        $apiKey = $matches[1]
        $url = "https://$($matches[2])"
        $authValue = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${apiKey}:"))
        $headers = @{
            Authorization = "Basic $authValue"
        }
    } else {
        $url = $imageUrl
        $headers = @{}
    }

    $fileName = Split-Path $url -Leaf
    $productId = Split-Path (Split-Path $url -Parent) -Leaf
    $productFolder = Join-Path $outputFolder $productId
    if (!(Test-Path -Path $productFolder)) {
        New-Item -ItemType Directory -Path $productFolder | Out-Null
    }
    $outputPath = Join-Path $productFolder ($fileName + ".jpg")
    Write-Host "Downloading $url..."

    try {
        Invoke-WebRequest -Uri $url -Headers $headers -OutFile $outputPath -ErrorAction Stop
    } catch {
        Write-Host "Failed to download $url. Reason: $($_.Exception.Message)"
        Add-Content -Path (Join-Path $outputFolder "failed_images.log") -Value $url
        continue
    }
}

Write-Host "✅ All images downloaded to $outputFolder"