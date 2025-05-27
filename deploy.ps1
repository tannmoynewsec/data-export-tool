# Azure deployment script for Streamlit app (PowerShell)
# 
# IMPORTANT: Resource group policy requirements:
# - Resource group must have tag "Environment" with value: 'Prod', 'Test' or 'Dev'
# - Resource group must have tag "Cost Center" with numeric value
# - If you don't know Cost Center number, use "Environment"= Dev
#
# Variables
$ResourceGroupName = "clientreporting-dev-rg"
$Location = "westeurope"
$AppServicePlanName = "dataexport1-app-plan"
$WebAppName = "dataexport1"
$AppServiceSku = "B1"

# Check if Resource Group exists
$groupExists = az group show --name $ResourceGroupName --output none 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Resource group '$ResourceGroupName' does not exist. Please create it first."
    exit 1
}

# Ensure App Service Plan exists
az appservice plan create --name $AppServicePlanName --resource-group $ResourceGroupName --sku $AppServiceSku --is-linux --output none
if ($LASTEXITCODE -ne 0) { exit 1 }

# Create Web App if it does not exist, otherwise settings will be updated on the existing app
$appExists = az webapp show --resource-group $ResourceGroupName --name $WebAppName --output none 2>$null
if ($LASTEXITCODE -ne 0) {
    az webapp create --resource-group $ResourceGroupName --plan $AppServicePlanName --name $WebAppName --runtime "PYTHON:3.12" --output none
    if ($LASTEXITCODE -ne 0) { exit 1 }
    Start-Sleep -Seconds 15
    az webapp show --resource-group $ResourceGroupName --name $WebAppName --output none
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

# Configure Python 3.12 runtime explicitly
az webapp config set --resource-group $ResourceGroupName --name $WebAppName --linux-fx-version "PYTHON:3.12" --output none
if ($LASTEXITCODE -ne 0) { exit 1 }

# Set Environment Variables
az webapp config appsettings set --resource-group $ResourceGroupName --name $WebAppName --settings SYNAPSE_SERVER="weu-ndw-dev-asa.sql.azuresynapse.net" SYNAPSE_DATABASE="weu_ndw_dev" SYNAPSE_USERNAME="NDWAdminASA" SYNAPSE_PASSWORD='X^Ly*Z85z%_GHk9b' SCM_DO_BUILD_DURING_DEPLOYMENT=true ENABLE_ORYX_BUILD=true ORYX_PLATFORM_NAME=python ORYX_PLATFORM_VERSION=3.12 --output none
if ($LASTEXITCODE -ne 0) { exit 1 }

# List current app settings for verification
az webapp config appsettings list --resource-group $ResourceGroupName --name $WebAppName --output table

# Restart to apply build settings
az webapp restart --resource-group $ResourceGroupName --name $WebAppName --output none
if ($LASTEXITCODE -ne 0) { exit 1 }

# Wait for restart to complete
Start-Sleep -Seconds 30

# Deploy code using az webapp up
Write-Output "Starting deployment with az webapp up..."
az webapp up --resource-group $ResourceGroupName --name $WebAppName --runtime "PYTHON:3.12" --sku $AppServiceSku --output table
if ($LASTEXITCODE -ne 0) { 
    Write-Output "Deployment failed."
    exit 1 
}

Write-Output "Deployment completed successfully."

# Ensure startup command is set after deployment
az webapp config set --resource-group $ResourceGroupName --name $WebAppName --startup-file "python -m streamlit run app/property_export_app_with_login.py --server.port 8000 --server.address 0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false" --output none
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Output "Script finished."
