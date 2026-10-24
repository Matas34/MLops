# Vykdymo palyginimas (benchmark) --- 7 savaite

## Aplinka
- GPU: NVIDIA Tesla V100-SXM2 32GB (VU HPC, SLURM, node-39). A100/T4 nebuvo naudotas.
- Modelis: TinyLlama-1.1B-Chat-v1.0
- Promptai: 50 fiksuotu, max_tokens=64

## Rezultatai
| Precizija | p50 (ms) | p95 (ms) | tok/s | VRAM (GB) | cost/1K tok |
|-----------|----------|----------|-------|-----------|-------------|
| FP16 | 196.9 | 336.3 | 218.6 | 2.05 (svoriai) | 0.00024$ |
| INT4 AWQ | - | - | - | - | - |

## Pastabos
- cost/1K tok. metrikai apskaičiuoti naudota Tesla V100 GPU valandinė kaina = 0.19$ (https://computeprices.com/providers/runpod/gpus/v100)
- AWQ nepavyko paleisti: reikalingas compute capability >= 7.5, o V100 turi 7.0 ("Minimum capability: 75. Current capability: 70").

## Sprendimas
Produkcijoje renkames FP16, nes: veikia produkcinėje aplinkoje, o INT4 AWQ - ne.

## 7.x Vykdymo NFR (v1.6)
| ID | Reikalavimas | KPI |
|--------|---------------------------|-----------------------------|
| NFR-27 | Fraud API p95 vėlinimas | <= 80 ms (KServe ONNX) |
| NFR-28 | LLM pralaidumas | >= 150 tok/s (7B AWQ HPC) |
| NFR-29 | Kaina / 1K tokenų | <= 0.002 USD |
| NFR-30 | Registry promocija | Staging->Prod su tvirtinimu |