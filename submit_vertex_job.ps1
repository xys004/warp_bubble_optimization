$JOB = "warp-hires-d2-" + (Get-Date -Format "MMddHHmm")
Write-Host "Submitting job: $JOB"

# CPU-only (no GPU quota needed). n1-highcpu-32 = 32 vCPUs, TF parallelises well.
$workerSpec = "machine-type=n1-highcpu-32,replica-count=1,container-image-uri=us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-12.py310:latest"

$cmd = "gsutil -m cp gs://warpopt-data/code/*.py . && python vertex_compute_maps.py --domain 2 --plane-n 2000 --input-gcs gs://warpopt-data/golden_dataset --output-gcs gs://warpopt-data/hires_maps/domain2 --input-dir /tmp/input --output-dir /tmp/output"

gcloud ai custom-jobs create `
    --project=warpopt `
    --region=us-central1 `
    --display-name=$JOB `
    --worker-pool-spec=$workerSpec `
    --command="bash,-c" `
    --args=$cmd

Write-Host ""
Write-Host "Monitor at: https://console.cloud.google.com/vertex-ai/training/custom-jobs?project=warpopt"
Write-Host "Download results when done:"
Write-Host "  gsutil -m cp -r gs://warpopt-data/hires_maps/domain2/ .\hires_maps\"
