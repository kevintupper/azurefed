# Script to copy the helpers folder to all app directories

# Run from the root directory, not from the scripts directory

# Define the paths to the helpers and apps folders
$HELPERS_FOLDER = "./helpers"
$APPS_FOLDER = "./apps"

# Get all the directories in the apps folder
$directories = Get-ChildItem -Path $APPS_FOLDER -Directory

foreach ($dir in $directories) {
    $helperPath = Join-Path -Path $dir.FullName -ChildPath $HELPERS_FOLDER
    
    # Check if the helpers subdirectory exists and remove it if it does
    if (Test-Path $helperPath) {
        Remove-Item -Path $helperPath -Recurse -Force
    }
    
    # Copy the helpers folder to the current directory in the loop
    Copy-Item -Path $HELPERS_FOLDER -Destination $dir.FullName -Recurse -Force

    # Copy the requirements.txt file to the current directory in the loop
    # WE NO LONGER DO THIS SINCE THE LOCAL REQUIREMENTS.TXT FILE HAS ITS OWN LOCAL APP SPECIFIC REQUIREMENTS
    # $requirementsDestPath = Join-Path -Path $dir.FullName -ChildPath "requirements.txt"
    # Copy-Item -Path "requirements.txt" -Destination $requirementsDestPath -Force
}

Write-Output "Helpers folder copied to all app directories."
