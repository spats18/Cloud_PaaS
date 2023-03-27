# Import the AWS PowerShell module
Import-Module AWSPowerShell

# Set the region and S3 bucket name
$region = "us-east-1"
$bucketName = "cse546-output"

# Get the list of CSV files in the bucket
$csvFiles = Get-S3Object -BucketName $bucketName -KeyPrefix "*.csv" -Region $region

# Count the number of CSV files
$csvCount = $csvFiles.Count

# Display the number of CSV files
Write-Host "There are $csvCount CSV files in $bucketName."

# Loop through each CSV file and display its contents
foreach ($csvFile in $csvFiles) {
    $csvContent = Get-S3ObjectContent -BucketName $bucketName -Key $csvFile.Key -Region $region
    Write-Host "Contents of $csvFile.Key:"
    $csvContent | ConvertFrom-Csv | Format-Table
}
