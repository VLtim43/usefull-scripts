
#read .env
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=')
    if ([string]::IsNullOrWhiteSpace($name) -or $name.Contains('#')) {
        continue
    }
    Set-Content env:\$name $value
}

#set input folder
$folderPath = $env:PATH

Write-Output $folderPath