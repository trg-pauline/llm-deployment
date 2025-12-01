# Multimodal Model Deployment on OpenShift

Simple deployment of multimodal AI models (vision-language) on OpenShift/OpenShift AI using KServe and vLLM.

## Overview

This project provides a straightforward way to deploy multimodal models from Hugging Face to OpenShift AI. It includes:

- **Namespace**: Isolated namespace for the deployment
- **PVC**: Persistent storage for model files
- **DataConnection**: OpenDataHub connection for the PVC
- **Job**: Kubernetes Job to download models from Hugging Face
- **ServingRuntime**: vLLM runtime configuration for multimodal models
- **InferenceService**: KServe InferenceService for serving the model

## Model

**LLaVA 1.5 7B** - Multimodal vision-language model
- Repository: `llava-hf/llava-1.5-7b-hf`
- Type: Vision + Language
- Size: ~7B parameters

See `MODEL_OPTIONS.md` for other model options.

## Prerequisites

- OpenShift/OpenShift AI cluster
- KServe/OpenDataHub installed
- GPU nodes available (NVIDIA L40 or compatible)
- Storage class configured (e.g., `gp3-csi` or `gp2-csi`)
- Hugging Face account with access token

## Quick Start

### 1. Configure Hugging Face Token

Edit `secret.yaml` and replace `YOUR_HUGGINGFACE_TOKEN_HERE` with your actual Hugging Face token:

```bash
# Edit the secret
vim secret.yaml
# Or use sed
sed -i '' 's/YOUR_HUGGINGFACE_TOKEN_HERE/your-actual-token-here/' secret.yaml
```

### 2. Deploy Base Resources

Deploy namespace, PVC, secret, and data connection:

```bash
oc apply -f namespace.yaml
oc apply -f pvc.yaml
oc apply -f secret.yaml
oc apply -f data-connection.yaml
```

Or all at once:

```bash
oc apply -f namespace.yaml -f pvc.yaml -f secret.yaml -f data-connection.yaml
```

### 3. Download the Model

Launch the download job:

```bash
oc apply -f job.yaml
```

Monitor the download:

```bash
# Check job status
oc get job download-llava-model -n multimodal-demo

# Follow logs
oc logs -f job/download-llava-model -n multimodal-demo

# Check pods
oc get pods -n multimodal-demo
```

### 4. Verify Model Download

Once the job completes, verify the model is downloaded:

```bash
# Check PVC size
oc get pvc pvc-multimodal -n multimodal-demo

# Check model files (using a temporary pod)
oc run model-checker --image=busybox -n multimodal-demo --rm -it --restart=Never -- \
  sh -c "ls -lah /mnt/models && du -sh /mnt/models" \
  --overrides='
{
  "spec": {
    "containers": [{
      "name": "model-checker",
      "volumeMounts": [{
        "mountPath": "/mnt/models",
        "name": "model-storage"
      }]
    }],
    "volumes": [{
      "name": "model-storage",
      "persistentVolumeClaim": {
        "claimName": "pvc-multimodal"
      }
    }]
  }
}'
```

### 5. Deploy Inference Service

Once the model is downloaded, deploy the serving runtime and inference service:

```bash
oc apply -f serving-runtime.yaml
oc apply -f inference-service.yaml
```

### 6. Verify Deployment

Check the inference service status:

```bash
# Check InferenceService
oc get inferenceservice llava-multimodal -n multimodal-demo

# Check pods
oc get pods -n multimodal-demo

# Get service URL
oc get inferenceservice llava-multimodal -n multimodal-demo -o jsonpath='{.status.url}'
echo ""
```

The service will be available at the URL shown above once it becomes `Ready`.

## Configuration

### Storage

Edit `pvc.yaml` to adjust:
- **Size**: Change `storage: 50Gi` to your desired size
- **Storage Class**: Change `storageClassName: gp3-csi` to match your cluster

### Model Selection

To use a different model, edit `job.yaml` and change the `model_id`:

```yaml
model_id = "llava-hf/llava-1.5-7b-hf"  # Change this
```

### Resources

Adjust CPU/memory in:
- `job.yaml`: For the download job
- `inference-service.yaml`: For the inference service

### GPU Configuration

The inference service is configured for:
- **GPU Type**: NVIDIA L40
- **GPU Count**: 1
- **Toleration**: `NVIDIA-L40-PRIVATE`

Adjust these in `inference-service.yaml` if needed.

## Troubleshooting

### Job Fails with Permission Errors

If you see `Permission denied` errors, ensure the SCC (Security Context Constraint) allows the user ID. The job uses `runAsUser: 1000990000` which should work with `restricted-v2` SCC.

### PVC Zone Mismatch

If pods can't schedule due to PVC zone mismatch:
1. Delete the PVC: `oc delete pvc pvc-multimodal -n multimodal-demo`
2. Recreate it: `oc apply -f pvc.yaml`
3. The PVC will be created in the zone of the node that first uses it

### GPU Not Available

If you see `Insufficient nvidia.com/gpu`:
- Check available GPUs: `oc describe node <gpu-node> | grep nvidia.com/gpu`
- Free up a GPU by deleting another InferenceService
- Wait for a GPU to become available

### Model Download Fails

- Verify your Hugging Face token is correct
- Check if the model repository is accessible
- Review job logs: `oc logs job/download-llava-model -n multimodal-demo`

## Cleanup

To remove all resources:

```bash
# Delete inference service and serving runtime
oc delete inferenceservice llava-multimodal -n multimodal-demo
oc delete servingruntime llava-multimodal -n multimodal-demo

# Delete job (if still present)
oc delete job download-llava-model -n multimodal-demo

# Delete base resources
oc delete -f data-connection.yaml
oc delete -f secret.yaml
oc delete -f pvc.yaml
oc delete -f namespace.yaml
```

## Files

- `namespace.yaml`: Namespace definition
- `pvc.yaml`: PersistentVolumeClaim for model storage
- `secret.yaml`: Hugging Face token secret (⚠️ **Replace token before committing!**)
- `data-connection.yaml`: OpenDataHub DataConnection for PVC
- `job.yaml`: Kubernetes Job to download model from Hugging Face
- `serving-runtime.yaml`: vLLM ServingRuntime configuration
- `inference-service.yaml`: KServe InferenceService definition
- `MODEL_OPTIONS.md`: Alternative model options and configurations

## License

See LICENSE file for details.
