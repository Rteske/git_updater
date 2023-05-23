import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
import os


class GitUpdater(QWidget):
    def __init__(self, repository_path):
        super().__init__()
        self.repository_path = repository_path
        self.setWindowTitle("Git Updater")
        self.layout = QVBoxLayout()
        self.label = QLabel("Click 'Check for Updates' to check if there are new changes in the repository.")
        self.check_button = QPushButton("Check for Updates")
        self.check_button.clicked.connect(self.check_repository_updates)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.check_button)
        self.setLayout(self.layout)

    def check_repository_updates(self):
        self.label.setText("Checking for updates...")
        process = subprocess.Popen(["git", "-C", self.repository_path, "fetch"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode == 0:
            local_branch = subprocess.check_output(
                ["git", "-C", self.repository_path, "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
            remote_branch = subprocess.check_output(
                ["git", "-C", self.repository_path, "rev-parse", "--abbrev-ref", "@{u}"]).decode("utf-8").strip()
            if local_branch == "master" and remote_branch == "origin/master":
                local_commit = subprocess.check_output(
                    ["git", "-C", self.repository_path, "rev-parse", "master"]).decode("utf-8").strip()
                remote_commit = subprocess.check_output(
                    ["git", "-C", self.repository_path, "rev-parse", "origin/master"]).decode("utf-8").strip()
                if local_commit == remote_commit:
                    self.label.setText("Repository is up to date.")
                else:
                    self.update_repository()
            else:
                self.label.setText("Please ensure the repository has a 'master' branch.")
        else:
            self.label.setText(f"Error checking for updates:\n{error.decode('utf-8')}")

    def update_repository(self):
        self.label.setText("Updating repository...")
        process = subprocess.Popen(["git", "-C", self.repository_path, "pull"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode == 0:
            self.label.setText("Repository successfully updated.")
        else:
            self.label.setText(f"Error updating repository:\n{error.decode('utf-8')}")


if __name__ == '__main__':
    repository_path = os.path.expanduser("~/AUTOTEST")
      # Replace with the actual path to your repository
    app = QApplication(sys.argv)
    window = GitUpdater(repository_path)
    window.show()
    sys.exit(app.exec_())
