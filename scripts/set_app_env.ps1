# Description: 
#   1. Read the .env file in the root of the project
#   2. Process the environment variables, excluding blank lines, comments, and the REGISTRY_PASSWORD variable
#   3. Update the MSAL_REDIRECT_URI environment variable with the Azure Container Apps instance URL
#   4. Concatenate the environment variables into a single string for the --set-env-var parameter
#   5. Set the environment variables for the specified application in Azure Container Apps

# Run from the root directory, not from the scripts directory
# Make sure you've run az login before running this script

param (
    [Parameter(Mandatory=$true)]
    [string]$appName
)

# Retrieve and process environment variables from the .env file, excluding blank lines, comments, and the REGISTRY_PASSWORD variable
$envVars = Get-Content .\.env | Where-Object { 
    $_.Trim() -ne "" -and 
    $_.TrimStart() -notmatch "^#" -and 
    $_ -notmatch "^REGISTRY_PASSWORD=" 
} | ForEach-Object {
    $parts = $_ -split "=", 2
    $key = $parts[0].Trim()
    $value = $parts[1].Trim().Trim('"') # Remove surrounding quotes if present
    
    # Check if the key is MSAL_REDIRECT_URI and replace its value accordingly
    if ($key -eq "MSAL_REDIRECT_URI") {
        if ($appName -eq "main") {
            $value = "https://azurefed.com"
        } else {
            $value = "https://$appName.azurefed.com"
        }
    }
    
    # Enclose the entire key=value pair in quotes
    "`"$key=$value`""
}

# Concatenate all environment variables into a single string for the --set-env-var parameter, with each pair quoted
$setEnvVars = $envVars -join " "

# Construct the path to the deploy_params.json file based on the app name
$paramsFilePath = "apps/$appName/deploy_params.json"

# Verify that the params file exists
if (-Not (Test-Path $paramsFilePath)) {
    Write-Error "The parameters file was not found: $paramsFilePath"
    exit
}

# Load parameters from the JSON file
$params = Get-Content $paramsFilePath | ConvertFrom-Json

# Construct the Azure CLI command to construct the environment variables
$azCommand = "az containerapp update " +
             "-n $($params.appName) " +
             "-g demo_infrastructure " +
             "--set-env-var $setEnvVars"

# Execute the command
Invoke-Expression $azCommand
