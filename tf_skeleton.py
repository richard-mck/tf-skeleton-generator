"""A generator to create a Terraform project, reducing startup time"""

import os
import sys

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


def write_content_to_file(file_name: str, content: str):
    with open(file_name, "w") as f:
        f.write(content)


if __name__ == "__main__":
    project_name = sys.argv[1]
    os.mkdir(project_name)
    os.chdir(project_name)
    tf_files = [BACKEND_TF, MAIN_TF, OUTPUTS_TF, VARIABLES_TF]
    for title in tf_files:
        print(title)
        write_content_to_file(title[0], title[1])
