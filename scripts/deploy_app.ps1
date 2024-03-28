# Description: This script is used to deploy a containerized application to Azure Container Apps.

# Run from root directory, not from scripts directory
# Make sure you've run az login before running this script

# Import the required modules
param (
    [Parameter(Mandatory=$true)]
    [string]$appName
)

# Retrieve the registry password from the .env file, handling potential quotes
$envLine = Get-Content .\.env | Where-Object { $_ -match "REGISTRY_PASSWORD=" }
$registryPassword = $envLine -split "=" | Select-Object -Last 1 | ForEach-Object { $_.Trim().Trim('"') }


# Construct the path to the deploy_params.json file based on the app name
$paramsFilePath = "apps/$appName/deploy_params.json"

# Verify that the params file exists
if (-Not (Test-Path $paramsFilePath)) {
    Write-Error "The parameters file was not found: $paramsFilePath"
    exit
}

# Load parameters from the JSON file
$params = Get-Content $paramsFilePath | ConvertFrom-Json

# Ensure registry password is not empty or null
if ([string]::IsNullOrEmpty($registryPassword)) {
    Write-Error "Registry password environment variable is not set."
    exit
}

# Construct the Azure CLI command with the --build-env-vars parameter included
$azCommand = "az containerapp up " +
             "-n $($params.appName) " +
             "-g demo_infrastructure " +
             "--environment managed-container-environment " +
             "--target-port 8501 " +
             "--image ktcontainers.azurecr.io/$($params.appName):latest " +
             "--source $($params.source) " +
             "--registry-server ktcontainers.azurecr.io " +
             "--registry-username ktcontainers " +
             "--registry-password $registryPassword " 

# Execute the command
Invoke-Expression $azCommand
