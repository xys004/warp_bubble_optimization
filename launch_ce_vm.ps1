$PROJECT  = "warpopt"
$ZONE     = "us-central1-a"
$VM_NAME  = "warp-compute-" + (Get-Date -Format "MMddHHmm")
$STARTUP  = "C:\Users\Nelson\Downloads\warp_optimization\warp_startup.sh"

Write-Host "Creating VM: $VM_NAME"

gcloud compute instances create $VM_NAME `
    --project=$PROJECT `
    --zone=$ZONE `
    --machine-type=n2-highcpu-32 `
    --image-family=debian-12 `
    --image-project=debian-cloud `
    --boot-disk-size=50GB `
    --scopes=cloud-platform `
    --metadata-from-file=startup-script=$STARTUP

Write-Host ""
Write-Host "VM running. Check completion with:"
Write-Host "  gsutil cat gs://warpopt-data/hires_maps/DONE.txt"
Write-Host ""
Write-Host "Then download:"
Write-Host "  gsutil -m cp -r gs://warpopt-data/hires_maps/ hires_maps/"
