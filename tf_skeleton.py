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
        self.module_file_list = [i for i in self.file_list if i != BACKEND_TF]
        self.environments = ["dev", "staging", "prod"]
        self.region = "us-west-2"

    @staticmethod
    def _create_directory(dir_name: str, make_cwd=False):
        """Create a dir at a given path, skip if dir already exists. Optionally, move to dir for subsequent actions"""
        try:
            os.makedirs(dir_name)
        except OSError:
            print(f"Directory {dir_name} already exists, skipping")
        if make_cwd:
            os.chdir(dir_name)

    def setup_project_working_directory(self):
        self._create_directory(project_name, make_cwd=True)

    def create_environments(self):
        """Create one directory and necessary files per environment and region"""
        for env in self.environments:
            env_path = f"{env}/{self.region}"
            self._create_directory(env_path)
            env_files = [
                TFFile(f"{env_path}/{item.file_name}", item.file_content)
                for item in self.file_list
            ]
            module_instance = TFFile(
                f"{env_path}/{self.project_name}.tf",
                f"""
module "{self.project_name}" {{
  source       = "../../modules/{self.project_name}"
  required_var = "This one is required!"
}}
            """,
            )
            env_files.append(module_instance)
            write_content_to_file(
                module_instance.file_name, module_instance.file_content
            )
            self.create_tf_files(env_files)

    def create_module_directory(self, module_name: str):
        """Create a new directory for our primary module"""
        self._create_directory(f"modules/{module_name}", make_cwd=True)

    @staticmethod
    def create_tf_files(file_list: list[TFFile]):
        """Iterate over a list of files, creating new instances of each"""
        for title in file_list:
            print(f"Creating {title.file_name}")
            write_content_to_file(title.file_name, title.file_content)

    def generate_project(self):
        """The main function of the module"""
        self.setup_project_working_directory()
        self.create_environments()
        self.create_module_directory(self.project_name)
        self.create_tf_files(self.module_file_list)


def write_content_to_file(file_name: str, content: str):
    """Given a filename and a string, write this data to a new file"""
    with open(file_name, "w") as f:
        f.write(content)


if __name__ == "__main__":
    project_name = sys.argv[1]
    tf_gen = SkeletonGenerator(project_name)
    tf_gen.generate_project()
