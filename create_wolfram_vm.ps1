(Get-Content "C:\Users\Nelson\Downloads\warp_optimization\wolfram_startup.sh") `
    -replace "WOLFRAM_KEY_PLACEHOLDER", "9909-9194-T5PLE8" | `
    Set-Content "C:\Users\Nelson\AppData\Local\Temp\wolfram_ready.sh" -Encoding UTF8

$VM = "wolfram-warp-" + (Get-Date -Format "MMddHHmm")
Write-Host "Creating VM: $VM"

gcloud compute instances create $VM `
    --project=warpopt `
    --zone=us-central1-a `
    --machine-type=e2-highcpu-32 `
    --image-family=debian-12 `
    --image-project=debian-cloud `
    --boot-disk-size=50GB `
    --scopes=cloud-platform `
    --metadata-from-file=startup-script="C:\Users\Nelson\AppData\Local\Temp\wolfram_ready.sh"

Write-Host "VM created. Monitor:"
Write-Host "  gcloud compute ssh $VM --zone=us-central1-a --project=warpopt --strict-host-key-checking=no --command='tail -f /tmp/wolfram_run.log'"
Write-Host "Check done:"
Write-Host "  gsutil cat gs://warpopt-data/wolfram_figures/DONE.txt"
