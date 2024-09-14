from kfp import dsl, compiler
from kfp.client import Client
from codeflare_sdk import Cluster, Job

@dsl.component
def prepare_dataset() -> str:
    import json
    from datasets import Dataset

    fhir_tasks = [
        {
            "instruction": "Extract the patient's name from this FHIR Patient resource.",
            "input": '''
            {
              "resourceType": "Patient",
              "id": "example",
              "name": [
                {
                  "use": "official",
                  "family": "Chalmers",
                  "given": ["Peter", "James"]
                }
              ],
              "gender": "male",
              "birthDate": "1974-12-25"
            }
            ''',
            "output": "The patient's name is Peter James Chalmers."
        },
        {
            "instruction": "Identify the medication name and dosage from this FHIR MedicationRequest resource.",
            "input": '''
            {
              "resourceType": "MedicationRequest",
              "id": "medrx0301",
              "status": "active",
              "medicationCodeableConcept": {
                "coding": [
                  {
                    "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                    "code": "1000097",
                    "display": "Amoxicillin 500mg Oral Tablet"
                  }
                ]
              },
              "dosageInstruction": [
                {
                  "text": "One tablet every 8 hours"
                }
              ]
            }
            ''',
            "output": "The medication is Amoxicillin with a dosage of 500mg, to be taken as one tablet every 8 hours."
        }
    ]

    dataset = Dataset.from_dict({
        "instruction": [item["instruction"] for item in fhir_tasks],
        "input": [item["input"] for item in fhir_tasks],
        "output": [item["output"] for item in fhir_tasks]
    })

    dataset.save_to_disk("/tmp/fhir_dataset")
    return "/tmp/fhir_dataset"

@dsl.component
def fine_tune_model(dataset_path: str) -> str:
    from codeflare_sdk import Cluster, Job
    
    # Initialize the cluster
    cluster = Cluster()
    cluster.create(name="finetuning-cluster", size=1, namespace="defualt",  )
    cluster.cluster_dashboard_uri

    # Define the fine-tuning job
    job = Job()
    job.name = "fhir-finetuning"
    job.image = "quay.io/project-codeflare/ray-ml:latest"  # Adjust this to your specific image
    job.working_dir = "/app"
    job.command = [
        "python", "-c",
        f"""
import json
from unsloth import FastLanguageModel
import torch
from datasets import load_from_disk
from transformers import TrainingArguments, Trainer

# Load the dataset
dataset = load_from_disk('{dataset_path}')

# Load the model and tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

# Prepare the model for training
FastLanguageModel.for_inference(model)

# Set up training arguments
training_args = TrainingArguments(
    output_dir="/tmp/results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="/tmp/logs",
    save_strategy="epoch",
)

# Create Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Start training
trainer.train()

# Save the fine-tuned model
model.save_pretrained("/tmp/fine_tuned_model")
tokenizer.save_pretrained("/tmp/fine_tuned_model")
        """
    ]

    # Submit the job
    job.submit(cluster)

    # Wait for the job to complete
    job.wait_for_completion()

    # Get the results
    #results = job.get_results()
    
    # Clean up the cluster
    cluster.delete()

    return "/tmp/fine_tuned_model"  # This path should match where the model is saved in the job

@dsl.component
def deploy_model(model_path: str, bucket_name: str, folder_name: str) -> str:
    import boto3
    import os
    from botocore.client import Config

    # S3 client setup
    s3_endpoint_url = os.environ.get('https://s3.tebi.io')
    s3_access_key = os.environ.get('sdIZ2HOKWWsDRpib')
    s3_secret_key = os.environ.get('MOuF1S7je2UzF12zl3xDuOMCDTKvE3IS9v0La3UE')

    s3 = boto3.client('s3',
                      endpoint_url=s3_endpoint_url,
                      aws_access_key_id=s3_access_key,
                      aws_secret_access_key=s3_secret_key,
                      config=Config(signature_version='s3v4'))

    # Upload model files to S3
    for root, dirs, files in os.walk(model_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, model_path)
            s3_path = os.path.join(folder_name, relative_path)
            
            print(f"Uploading {local_path} to s3://{'fhir-model'}/{s3_path}")
            s3.upload_file(local_path, 'fhir-model', s3_path)

    print(f"Model deployed to s3://{bucket_name}/{folder_name}")
    return f"Model deployed to s3://{bucket_name}/{folder_name}"
@dsl.pipeline(
    name="FHIR Model Pipeline",
    description="Prepares FHIR dataset, fine-tunes Llama 3.1 model using CodeFlare SDK, and deploys it."
)
def fhir_model_pipeline():
    dataset_task = prepare_dataset()
    fine_tune_task = fine_tune_model(dataset_task.output)
    deploy_task = deploy_model(fine_tune_task.output)

# Compile the pipeline
compiler.Compiler().compile(fhir_model_pipeline, 'fhir_model_pipeline.yaml')

# Submit the pipeline for execution
