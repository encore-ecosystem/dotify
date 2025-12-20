from dotify_lib.namespace import Namespace
from dotify_lib.plugin.procedure import PluginProcedure
from dotify_lib.shell import Shell
from git import Repo


class GitClone(PluginProcedure):
    url: str

    def run(self, shell: Shell, namespace: Namespace):
        _, user_repo = self.url.removesuffix(".git").split("/")[-2:]
        to_path = shell.cwd / user_repo
        if not to_path.exists():
            repo = Repo.clone_from(self.url, to_path)
        repo = Repo(to_path)
        repo.remotes.origin.pull()
        return to_path
