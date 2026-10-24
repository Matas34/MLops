"""Register fraud model from latest run or local artifact."""
import mlflow
from mlflow.tracking import MlflowClient
MODEL_NAME = "fraud-detector"
RUN_ID = "31603b4c1edd4936ba77622464418734" # or use runs:/ URI from mlflow ui
mlflow.set_tracking_uri("http://127.0.0.1:5000")
result = mlflow.register_model(f"runs:/{RUN_ID}/model", MODEL_NAME)
version = result.version
print(f"Registered {MODEL_NAME} v{version}")
client = MlflowClient()
client.transition_model_version_stage(MODEL_NAME, version, "Staging")
# After validation:
client.transition_model_version_stage(MODEL_NAME, version, "Production")
print(f"Promoted v{version} to Production")
