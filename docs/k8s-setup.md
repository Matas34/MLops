# Kubernetes Setup - Week 5

## Clusters

| Environment | Platform           | Purpose          |
|-------------|--------------------|------------------|
| Dev         | Minikube           | CPU inference    |
| Cloud       | GKE Autopilot      | CPU inference    |
| HPC         | VU MIF HPC (Slurm) | GPU DDP training |

## Deploy inference

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment-cpu.yaml
kubectl apply -f k8s/service-cpu.yaml
```

## Deploy GPU training (HPC, Slurm)

> The VU MIF HPC does not provide Kubernetes. GPU training was run as a
> Slurm job in a Singularity container instead.

`train-ddp.sh`:

```bash
#!/bin/bash
#SBATCH -p gpu
#SBATCH --gres gpu:2
#SBATCH -c 8
#SBATCH --time=00:20:00
#SBATCH -o ddp-training-%j.out

cd /scratch/lustre/home/$USER/mlops
SIF=/apps/local/nvidia/pytorch-21.11-py3.sif

nvidia-smi --query-gpu=timestamp,index,utilization.gpu,memory.used --format=csv -l 5 > docs/gpu-util.log &
SMI_PID=$!

export NCCL_DEBUG=INFO
singularity exec --nv $SIF \
  torchrun --standalone --nproc_per_node=2 src/train_ddp.py --epochs 5

kill $SMI_PID
```

Submit and monitor:

```bash
sbatch train-ddp.sh
squeue -u $USER
```

## Cleanup

```bash
kubectl delete namespace mlops
```