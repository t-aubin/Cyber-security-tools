# Path to the CSV file containing hostnames
$csvPath = "C:\path\to\your\file.csv"

# Import the CSV file
$hostnames = Import-Csv $csvPath

# Iterate through each hostname and ping it
foreach ($hostname in $hostnames) {
    $response = Test-Connection -ComputerName $hostname.Name -Count 4 -Quiet
    if (-not $response) {
        Write-Output "$($hostname.Name) is offline"
    }
}
