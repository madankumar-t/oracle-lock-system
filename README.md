# 🔐 Oracle Lock System

This project is an **AWS Lambda-based locking system for Oracle resources**, triggered by **API Gateway** and deployed using the **AWS Serverless Application Model (SAM)**.

---

## 🧭 Overview

The system exposes HTTP endpoints that allow clients to lock and unlock Oracle system resources. The underlying logic is encapsulated in a Lambda function (`lambda_handler.py`) and deployed using SAM with a declarative `template.yaml`.

---

## 📂 Project Structure


---

## 🚀 Features

- ✅ API Gateway trigger (HTTP-based)
- ✅ Lock/Unlock operations
- ✅ Python Lambda function
- ✅ SAM for infrastructure-as-code deployment
- ✅ Dependency management via `requirements.txt`

---

## ⚙️ Prerequisites

- AWS CLI configured with permissions
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3.8+ installed

---

## 🔧 Installation & Deployment

### 1. Build the application

```bash
sam build

2. Deploy to AWS
```
sam deploy --guided
```

You’ll be prompted for:

Stack name

AWS region

IAM permissions

API Gateway setup (yes)

Test Locally
You can invoke the Lambda function locally with:
sam local invoke --event event.json

Or test the API Gateway locally with:

sam local start-api

Then access it at:
http://127.0.0.1:3000/lock or .../unlock

SAM Template Reference (template.yaml)
Ensure your template.yaml includes:

```

Resources:
  OracleLockFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: lambda/
      Handler: lambda_handler.lambda_handler
      Runtime: python3.8
      Events:
        LockAPI:
          Type: Api
          Properties:
            Path: /lock
            Method: post
```
