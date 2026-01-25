variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
}
variable "project" {
  description = "Project"
  default     = "ardent-particle-485105-j0"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}
variable "location" {
  description = "Project location"
  default     = "US"

}
variable "bq_dataset_name" {
  description = "My Big query Dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket name"
  default     = "ardent-particle-485105-j0-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"

}
