

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

$fileTypes = @("*.png", "*.jpg", "*.jpeg", "*.webp", "*.gif", "*.mp4", "*.avi", "*.mkv")
$fileCounts = @{}

foreach ($fileType in $fileTypes) {
    $fileCounts[$fileType] = 0
}

$totalFiles = (Get-ChildItem -Path $folderPath -File -Recurse | Measure-Object).Count
Write-Output "Total files: $totalFiles"

$totalFolders = (Get-ChildItem -Path $folderPath -Directory -Recurse | Measure-Object).Count

if ($totalFolders -ne 0) {
    Write-Output "Total folders: $totalFolders"
}


foreach ($fileType in $fileTypes) {
    $count = (Get-ChildItem -Path $folderPath -Filter $fileType -File -Recurse | Measure-Object).Count
    $fileCounts[$fileType] = $count

    if ($fileCounts[$fileType] -ne 0) {
        $extension = $fileType.TrimStart("*.")
        Write-Output "$extension $($fileCounts[$fileType])"
    }
}
