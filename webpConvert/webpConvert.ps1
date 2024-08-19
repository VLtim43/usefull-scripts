

#read .env
# Get-Content .env | ForEach-Object {
#     $name, $value = $_.split('=')
#     if ([string]::IsNullOrWhiteSpace($name) -or $name.Contains('#')) {
#         continue
#     }
#     Set-Content env:\$name $value
# }

#set input folder
# $folderPath = $env:PATH


$folderPath = Read-Host 'Enter the path'


if (-not (Get-Command magick -ErrorAction SilentlyContinue)) {
    Write-Error "ImageMagick is not installed or not in the system PATH."
    exit
}

$webpFiles = Get-ChildItem -Path $folderPath -Filter *.webp
Write-Output "[$($webpFiles.Count)] webp files found"

$gifs = 0
$images = 0
$totalFiles = $webpFiles.Count
$currentFile = 0

$startTime = Get-Date

foreach ($webpFile in $webpFiles) {
    $currentFile++
    $isAnimated = & magick identify -format "%n" $webpFile.FullName

    $percentComplete = ($currentFile / $totalFiles) * 100

    Write-Progress -Activity "Processing WebP Files" -Status "$currentFile of $totalFiles files processed..." -PercentComplete $percentComplete

    if ($isAnimated -gt 1) {
        $gifs += 1
        $outputFile = Join-Path $webpFile.DirectoryName ([System.IO.Path]::GetFileNameWithoutExtension($webpFile.Name) + ".gif")
        magick $webpFile.FullName $outputFile
    }
    else {
        $images += 1
        $outputFile = Join-Path $webpFile.DirectoryName ([System.IO.Path]::GetFileNameWithoutExtension($webpFile.Name) + ".png")
        magick $webpFile.FullName $outputFile
    }
}

Write-Host "[$gifs] gifs found"
Write-Host "[$images] images found"

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host "Total time taken: $($duration.Milliseconds) Milliseconds"
