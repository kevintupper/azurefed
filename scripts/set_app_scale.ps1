# Set the scale of an application in Azure Container Apps

# Run from the root directory, not from the scripts directory
# Make sure you've run az login before running this script

param (
    [Parameter(Mandatory=$true)]
    [string]$appName,

    [Parameter(Mandatory=$false)]
    [double]$cpu = 0.5,

    [Parameter(Mandatory=$false)]
    [string]$memory = "1.0Gi"
)

# Construct the path to the deploy_params.json file based on the app name
$paramsFilePath = "apps/$appName/deploy_params.json"

# Verify that the params file exists
if (-Not (Test-Path $paramsFilePath)) {
    Write-Error "The parameters file was not found: $paramsFilePath"
    exit
}

# Load parameters from the JSON file
$params = Get-Content $paramsFilePath | ConvertFrom-Json

# Construct the Azure CLI command to update the container app with the specified CPU and memory
$azCommand = "az containerapp update " +
             "-n $($params.appName) " +
             "-g demo_infrastructure " +
             "--cpu $cpu --memory $memory "

# Print the Azure CLI command (for debugging purposes or manual inspection)
Write-Output "Executing Azure CLI command: $azCommand"

# Execute the command
Invoke-Expression $azCommand
