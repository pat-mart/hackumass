# Provider
provider "aws" {
  region = "us-east-2"  # Update with the desired region
}
variable "region" {
  type    = string
  default = "us-east-2"  # Default region, update as needed
}
# Retrieve the current AWS account information
data "aws_caller_identity" "current" {}

# S3 Bucket for Image Uploads
resource "aws_s3_bucket" "image_bucket" {
  bucket = "hackumassbucket4"
}

# S3 Bucket Notification for Lambda Trigger
resource "aws_s3_bucket_notification" "image_upload_notification" {
  bucket = aws_s3_bucket.image_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.rekognition_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke_lambda]
}

# IAM Role for Lambda to access S3 and Rekognition
resource "aws_iam_role" "lambda_execution_role" {
  name = "rekognition_lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
      }
    ]
  })
}

# Attach Policy to allow Lambda to use S3 and Rekognition
resource "aws_iam_policy" "lambda_s3_rekognition_policy" {
  name        = "LambdaS3RekognitionPolicy"
  description = "IAM policy for S3 access and Rekognition for Lambda"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "rekognition:DetectFaces",
          "s3:GetObject",
          "rekognition:*"
        ]
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.image_bucket.bucket}/*",
          "arn:aws:rekognition:${var.region}:${data.aws_caller_identity.current.account_id}:*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = "logs:*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_execution_role_attach" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_s3_rekognition_policy.arn
}

# Lambda Function to Call Rekognition and Detect Emotions
resource "aws_lambda_function" "rekognition_lambda" {
  filename         = "lambda_function_payload.zip"  # Prepackaged Lambda code zip
  function_name    = "emotionDetectionLambda"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("lambda_function_payload.zip")

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.image_bucket.bucket
    }
  }
}

# Allow S3 to Invoke the Lambda Function
resource "aws_lambda_permission" "allow_s3_invoke_lambda" {
  statement_id  = "AllowS3InvokeLambda"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rekognition_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.image_bucket.arn
}

# Output S3 Bucket Name
output "s3_bucket_name" {
  value = aws_s3_bucket.image_bucket.bucket
}
