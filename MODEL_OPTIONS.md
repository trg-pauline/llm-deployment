# Options de Modèles Multimodaux

Le modèle `RedHatAI/LLaVaOLMoBitnet1B` n'existe pas ou n'est pas accessible.

## Modèles Multimodaux Recommandés

### Option 1: LLaVA (Microsoft)
- `llava-hf/llava-1.5-7b-hf` - Modèle LLaVA 1.5 (7B)
- `llava-hf/llava-1.6-vicuna-7b-hf` - Modèle LLaVA 1.6 (7B)
- `llava-hf/llava-1.6-mistral-7b-hf` - Modèle LLaVA 1.6 avec Mistral (7B)

### Option 2: Modèles RedHatAI
Vérifiez les modèles disponibles sur: https://huggingface.co/RedHatAI

### Option 3: Autres Modèles Multimodaux
- `microsoft/kosmos-2-patch14-224` - KOSMOS-2
- `Salesforce/blip2-opt-2.7b` - BLIP-2

## Comment Changer le Modèle

1. Éditez `job.yaml`
2. Changez la ligne:
   ```python
   model_id = "RedHatAI/LLaVaOLMoBitnet1B"
   ```
3. Remplacez par le nom du modèle souhaité, par exemple:
   ```python
   model_id = "llava-hf/llava-1.5-7b-hf"
   ```
4. Redéployez le Job:
   ```bash
   oc delete job download-llava-model -n multimodal-demo
   oc apply -f examples/multimodal-deployment/job.yaml
   ```

## Vérification

Pour vérifier qu'un modèle existe:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://huggingface.co/api/models/MODEL_NAME
```

