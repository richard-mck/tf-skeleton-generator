"""A generator to create a Terraform project, reducing startup time"""

import os
import sys
from collections import namedtuple

TFFile = namedtuple("TFFile", ["file_name", "file_content"])

BACKEND_TF = TFFile(
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

MAIN_TF = TFFile(
    "main.tf",
    """
resource "random_id" "id" {
  byte_length = 8
}
""",
)

OUTPUTS_TF = TFFile(
    "outputs.tf",
    """
output "required" {
  description = "This prints the contents of a variable when Terraform is run"
  value       = var.required_var
}
""",
)

VARIABLES_TF = TFFile(
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


class SkeletonGenerator:
    def __init__(self, project_name):
        self.project_name = project_name
        self.file_list = [BACKEND_TF, MAIN_TF, OUTPUTS_TF, VARIABLES_TF]

    def setup_project_working_directory(self):
        os.mkdir(self.project_name)
        os.chdir(self.project_name)

    def create_tf_files(self):
        for title in self.file_list:
            print(title)
            write_content_to_file(title.file_name, title.file_content)

    def generate_project(self):
        self.setup_project_working_directory()
        self.create_tf_files()


def write_content_to_file(file_name: str, content: str):
    with open(file_name, "w") as f:
        f.write(content)


if __name__ == "__main__":
    project_name = sys.argv[1]
    tf_gen = SkeletonGenerator(project_name)
    tf_gen.generate_project()
