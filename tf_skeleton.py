"""A generator to create a Terraform project, reducing startup time"""

BACKEND_TF = (
    "backend.tf",
    """
terraform {
  required_version = ">= 1.3"
  required_providers {}
  backend "http" {}
  # Edit this to fit your environment
}
""",
)

MAIN_TF = (
    "main.tf",
    """
resource "random_id" "id" {
  byte_length = 8
}
""",
)

OUTPUTS_TF = (
    "outputs.tf",
    """
output "required" {
  description = "This prints the contents of a variable when Terraform is run"
  value       = var.required_var
}
""",
)

VARIABLES_TF = (
    "variables.tf",
    """
variable "required_var" {
  type        = string
  description = "This is a required variable"
}

variable "optional_var" {
  type        = string
  description = "This is an optional variable"
  default     = "Optional"
}
""",
)

if __name__ == "__main__":
    tf_files = [BACKEND_TF, MAIN_TF, OUTPUTS_TF, VARIABLES_TF]
    for title in tf_files:
        print(title)
        with open(title[0], "w") as f:
            f.write(title[1])
