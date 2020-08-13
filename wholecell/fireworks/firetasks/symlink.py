import os
import time
import shutil

from fireworks import FireTaskBase, explicit_serialize


@explicit_serialize
class SymlinkTask(FireTaskBase):

    _fw_name = "SymlinkTask"
    required_params = ["to", "link"]
    optional_params = ["overwrite_if_exists"]

    def run_task(self, fw_spec):
        """
            @description: CANNOT create symlink in win10!
        """
        print("%s: Cannot creating symlink, file instead" % (time.ctime()))

        if self["overwrite_if_exists"]:
            if os.path.exists(self["link"]):
                os.remove(self["link"])

        path = os.path.split(self["link"])[0]
        shutil.copy(os.path.join(path, self["to"]), self["link"])
