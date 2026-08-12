import sys
from src.customer_churn_prediction.pipelines.training_pipeline import TrainingPipeline

def main():
    try:
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
    except Exception as e:
        print(f"Error executing pipeline: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
