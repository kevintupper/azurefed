# Create a new development application by copying the starter application

# Run from root directory, not from scripts directory

param (
    [string]$appName
)



#********************************************************************************************************************
# Function to update the content of a file by replacing specified text
#********************************************************************************************************************
function Update-Starter-FileContent {
    param (
        [string]$FilePath,
        [string]$ReplaceTextLower
    )

    # Define the search text
    $SearchTextInitCap = "Starter"
    $SearchTextLower = "starter"

    Write-Host "Updating text: $ReplaceTextLower"

    # Capitalize the first letter of ReplaceTextLower for "Starter" replacement
    $ReplaceTextInitCap = $ReplaceTextLower.Substring(0,1).ToUpper() + $ReplaceTextLower.Substring(1)

    # Read the file contents
    $fileContent = Get-Content -Path $FilePath -Raw

    # Replace 'SearchTextInitCap' with 'ReplaceTextInitCap' respecting case for 'Starter'
    # Then replace 'SearchTextLower' with 'ReplaceTextLower' respecting case for 'starter'
    $modifiedContent = $fileContent -creplace $SearchTextInitCap, $ReplaceTextInitCap -replace $SearchTextLower, $ReplaceTextLower

    # Write the modified content back to the file
    Set-Content -Path $FilePath -Value $modifiedContent

    Write-Output "$FilePath has been updated to replace 'Starter' with '$ReplaceTextInitCap' and 'starter' with '$ReplaceTextLower'."
}



#********************************************************************************************************************
# Main script logic
#********************************************************************************************************************

# Convert to lowercase 
$appName = $appName.ToLower()

# Define source and destination paths
$sourcePath = "./apps/starter"
$destPath = "./apps/$appName"

# Check if the destination directory already exists
if (Test-Path $destPath) {
    Write-Output "The application '$appName' already exists."
} else {
    try {
        # Copy the directory and its contents
        Copy-Item -Path $sourcePath -Destination $destPath -Recurse
        Write-Output "The application '$appName' has been successfully created."

        # Rename starter.py to <appName>.py
        $oldFilePath = Join-Path -Path $destPath -ChildPath "starter.py"
        $newFileName = "$appName.py"

        # Check if the starter.py file exists in the new application directory
        if (Test-Path $oldFilePath) {
            Rename-Item -Path $oldFilePath -NewName $newFileName
            Write-Output "starter.py has been renamed to $newFileName"
        } else {
            Write-Output "starter.py was not found in the new application directory."
        }

        #********************************************************************************************************************
        # Update the Dockerfile to use the new Python file
        #********************************************************************************************************************

        # Define the path to the Dockerfile in the new application directory
        $dockerfilePath = Join-Path -Path $destPath -ChildPath "Dockerfile"
        Update-Starter-FileContent $dockerfilePath $appName


        #********************************************************************************************************************
        # Update the Python file to with the new application name
        #********************************************************************************************************************

        # Define the path to the renamed Python file in the new application directory
        $appPythonFilePath = Join-Path -Path $destPath -ChildPath "$appName.py"
        Update-Starter-FileContent $appPythonFilePath $appName


        #********************************************************************************************************************
        # Update the deploy_params.json file to replace 'starter' with the new application name
        #********************************************************************************************************************

        # Define the path to the renamed Python file in the new application directory
        $appDeployParamsPath = Join-Path -Path $destPath -ChildPath "deploy_params.json"
        Update-Starter-FileContent $appDeployParamsPath $appName

    } catch {
        Write-Error "An error occurred during the script execution: $_"
    }
}