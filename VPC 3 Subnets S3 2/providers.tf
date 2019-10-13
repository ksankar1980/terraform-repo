provider "aws" {
  region = "${var.region}"
  version = "1.31"
  }
provider "template" {
  version = "2.0.0"
  }
terraform {
  required_version = ">= 0.11.7"
   backend "s3" {
    bucket = "kartcncptest"
    key    = "VPC 3 Subnets S3/terraform.tfstate"
    region = "ap-southeast-2"
  }
}  
